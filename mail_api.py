import base64
import datetime
import quopri
import re
import socket
import ssl
from datetime import datetime
from typing import Optional, Any


class Email:
    def __init__(self, sender: str, receiver: str, title: str, body: str, timestamp: datetime.time, offset_id: int = 0,
                 is_read: bool = False, is_deleted: bool = False, folder: str = 'inbox', obj_id="",
                 header_dict: Any = None):
        self.sender = sender
        self.receiver = receiver
        self.title = title
        self.body = body
        self.timestamp = timestamp
        self.is_read = is_read
        self.is_deleted = is_deleted
        self.folder = folder
        self.offset_id = offset_id
        self.obj_id = obj_id
        self.header_dict = header_dict

    def __repr__(self):
        return f"<Email(title={self.title}, sender={self.sender}, receiver={self.receiver}, folder={self.folder})>"


class EmailClient:
    def __init__(self, smtp_server, smtp_port, pop_server, pop_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.pop_server = pop_server
        self.pop_port = pop_port
        self.username = username
        self.password = password

        # POP Socket 初始化
        self.pop_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pop_sock.connect((self.pop_server, self.pop_port))
        self.pop_sock = ssl.wrap_socket(self.pop_sock)
        recv = self.pop_sock.recv(1024).decode()
        if not recv.startswith('+OK'):
            raise Exception("POP协议 连接失败: " + recv)
        # POP3 登录
        self._pop3_command('USER ' + self.username)
        self._pop3_command('PASS ' + self.password)

    def _smtp_command(self, command) -> str:
        self.smtp_socket.send((command + '\r\n').encode())
        recv = self.smtp_socket.recv(1024).decode()

        if not (recv.startswith('2') or recv.startswith('3')):
            raise Exception("SMTP command failed: " + command + ' Response: ' + recv)
        return recv[3:]

    def _pop3_command(self, command, bypass_ok=False) -> str:
        self.pop_sock.sendall((command + '\r\n').encode())
        response = self.pop_sock.recv(1024).decode()
        if not response.startswith('+OK'):
            raise Exception(f'POP3 命令失败: {command} - {response}')

        # 多行响应
        if not response.endswith('\r\n') or (bypass_ok and response == "+OK\r\n"):
            full_response = response
            while not full_response.endswith('\r\n.\r\n'):
                chunk = self.pop_sock.recv(1024).decode()
                full_response += chunk
            response = full_response

        if response.startswith("+OK\r\n"):
            return response[5:]
        elif response.startswith("+OK "):
            return response[4:]

    def _get_email_headers(self, email_id):
        response = self._pop3_command(f'TOP {email_id} 0', bypass_ok=True)
        headers = response.split('\r\n\r\n', 1)[0]
        email = self._parse_headers(headers)
        email.offset_id = email_id
        return email

    def _decode_mime_word(self, word):
        # Regular expression to match the pattern =?charset?encoding?encoded_text?=
        match = re.match(r'=\?(?P<charset>.*?)\?(?P<encoding>.*?)\?(?P<encoded_text>.*?)\?=', word)
        if not match:
            return word  # Return the word as is if it doesn't match the pattern

        charset = match.group('charset')
        encoding = match.group('encoding').lower()
        encoded_text = match.group('encoded_text')

        if encoding == 'b':  # Base64 encoded
            byte_string = base64.b64decode(encoded_text)
        elif encoding == 'q':  # Quoted-Printable encoded
            byte_string = quopri.decodestring(encoded_text.replace('_', ' '))
        else:
            raise ValueError(f"Unknown encoding: {encoding}")

        return byte_string.decode(charset)

    def _decode_mime_words(self, header):
        decoded_string = ''
        words = re.split(r'(\s+)', header)  # Split by spaces but keep them in the result
        for word in words:
            if word.startswith('=?') and word.endswith('?='):
                decoded_string += self._decode_mime_word(word)
            else:
                decoded_string += word
        return decoded_string

    def _parse_header_in_dict(self, headers):
        processed_headers = []
        for line in headers.split('\r\n'):
            if line.startswith(' ') or line.startswith('\t'):
                processed_headers[-1] += ' ' + line.strip()
            else:
                processed_headers.append(line)

        header_dict = {}
        for line in processed_headers:
            if ':' in line:
                key, value = line.split(':', 1)
                header_dict[key.strip()] = value.strip()

        return header_dict

    def _parse_headers(self, headers):
        header_dict = self._parse_header_in_dict(headers)

        email = Email(
            sender=self._decode_mime_words(header_dict.get('From', '').split(" ")[0].strip('"')) + ' ' +
                   header_dict.get('From', '').split(" ")[1] if len(
                header_dict.get('From', '').split(" ")) == 2 else header_dict.get('From', ''),
            receiver=self._decode_mime_words(header_dict.get('To', '').split(" ")[0].strip('"')) + ' ' +
                     header_dict.get('To', '').split(" ")[1] if len(
                header_dict.get('To', '').split(" ")) == 2 else header_dict.get('To', ''),
            title=self._decode_mime_words(header_dict.get('Subject', '')),
            body='',
            timestamp=datetime.strptime(header_dict.get('Date', '').split("+")[0].strip(), "%a, %d %b %Y %H:%M:%S"),
            offset_id=-1,
            header_dict=header_dict
        )
        return email

    def _parse_email(self, raw_email, fetch_html):
        headers, body = raw_email.split('\r\n\r\n', 1)
        email = self._parse_headers(headers)

        def decode_base64(encoded_text):
            return base64.b64decode(encoded_text).decode('utf-8')

        content_type: str = email.header_dict["Content-Type"]

        if "multipart/alternative" not in content_type and "boundary" not in content_type:
            # 那么就直接返回就好了
            email.body = body[:-5]
            return email

        boundary = "--" + content_type.split(";")[1].split('"')[1]
        body_parts: list[str] = body.split(boundary)
        for body_part in body_parts[1:-1]:
            body_seg = body_part.split("\r\n\r\n")
            header = body_seg[0].strip("\r\n")
            header_dict = self._parse_header_in_dict(header)
            body_part_content_type = header_dict["Content-Type"].strip().split(";")[0]
            if body_part_content_type == "text/plain" and not fetch_html:
                for seg in body_seg[1:]:
                    email.body += decode_base64(seg)
            elif body_part_content_type == "text/html" and fetch_html:
                for seg in body_seg[1:]:
                    email.body += decode_base64(seg)
                break

        email.body = email.body.strip()
        return email

    def send_email(self, to_address: str, subject: str, body: str, cc_addresses: list[str] = None,
                   is_html_body=False) -> bool:
        """
        向指定地址发送邮件
        :param to_address: 收件人地址
        :param subject: 邮件主题
        :param body: 邮件内容，提供一个纯文本内容
        :param cc_addresses: 提供一个字符串数组列表，抄送地址
        :return: 是否发送成功
        """

        # SMTP 初始化
        self.smtp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.smtp_socket.connect((self.smtp_server, self.smtp_port))

        recv = self.smtp_socket.recv(1024).decode()
        if not recv.startswith('220'):
            raise Exception("SMTP协议 链接失败: " + recv)

        try:
            # 发送 EHLO
            self._smtp_command('EHLO sorux.cn')
            self._smtp_command('STARTTLS')

            context = ssl.create_default_context()
            self.smtp_socket = context.wrap_socket(self.smtp_socket, server_hostname=self.smtp_server)

            self._smtp_command('EHLO sorux.cn')
            self._smtp_command("AUTH LOGIN")
            self._smtp_command(base64.b64encode(self.username.encode()).decode())
            self._smtp_command(base64.b64encode(self.password.encode()).decode())

            self._smtp_command(f"MAIL FROM:<{self.username}>")

            if cc_addresses:
                for cc in cc_addresses:
                    self._smtp_command(f"RCPT TO:<{cc}>")

            self._smtp_command("DATA")
            headers = f"To: {to_address}\r\n"
            headers += f"Subject: {subject}\r\n"
            headers += "MIME-Version: 1.0\r\n"
            if is_html_body:
                headers += "Content-Type: text/html; charset=utf-8\r\n"
            else:
                headers += "Content-Type: text/plain; charset=utf-8\r\n"
            if cc_addresses:
                headers += f"Cc: {', '.join(cc_addresses)}\r\n"
            message = f"{headers}\r\n{body}\r\n."
            self._smtp_command(message)
            self._smtp_command("QUIT")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            self.smtp_socket.close()

    def get_offset_id_by_obj_id(self, obj_id: str) -> str:
        """
        通过邮件的 obj_id 获取 offset_id
        :param obj_id:
        :return: 返回 offset_id，如果返回 "" 说明没有找到
        """
        response = self._pop3_command('LIST')
        lines = response.split('\r\n')[1:-2]
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                email_offset_id = parts[0]
                if obj_id == self._pop3_command("UIDL " + email_offset_id).split(" ")[1].strip():
                    return email_offset_id

        return ""

    def get_email_list(self, offset=0, limit=10) -> list[Email]:
        """
        获取邮件列表，返回一个包含邮件信息的列表
        :param offset: 偏移量
        :param limit: 获取邮件数量
        :return: 返回带有邮件基本信息的列表（Email 中只会含有 sender, receiver, title, timestamp, offset_id）
        """
        try:
            emails = []
            response = self._pop3_command('LIST')
            lines = response.split('\r\n')[1:-2]
            for line in lines[offset:offset + limit]:
                parts = line.split()
                if len(parts) >= 2:
                    email_offset_id = int(parts[0])
                    email = self._get_email_headers(email_offset_id)
                    email.offset_id = email_offset_id
                    email.obj_id = self._pop3_command("UIDL " + str(email_offset_id)).split(" ")[1].rstrip()
                    if email:
                        emails.append(email)
            return emails
        except Exception as e:
            raise Exception("获取邮件列表时出错:", e)

    def get_email_by_obj_id(self, obj_id: str, fetch_html: bool = True) -> Optional[Email]:
        """
        获取邮件内容
        :param fetch_html: 如果为 True，那么在邮件提供了 text/plain 和 text/html 两种方法的情况下，使用 text/html 作为 Body，否则使用 text/plain
        :param obj_id: 唯一 ID
        :return:
        """
        try:
            if obj_id == "":
                return None
            offset_id = self.get_offset_id_by_obj_id(obj_id)
            response = self._pop3_command(f'RETR {offset_id}', bypass_ok=True)
            return self._parse_email(response, fetch_html)
        except Exception as e:
            raise Exception("获取邮件内容时出错:", e)

    def delete_email(self, obj_id: str) -> bool:
        """
        删除邮件
        :param obj_id: 根据偏移量删除某个邮件
        :return:
        """
        try:
            if obj_id == "":
                return False
            offset_id = self.get_offset_id_by_obj_id(obj_id)
            self._pop3_command(f'DELE {offset_id}')
            return True
        except Exception as e:
            raise Exception("获取邮件内容时出错:", e)

    def quit(self):
        """
        调用本方法，使得修改被保存。例如删除的邮件被彻底删除
        :return:
        """
        self._pop3_command("QUIT")
