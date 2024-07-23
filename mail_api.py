import base64
import datetime
import socket
import ssl
from datetime import datetime
from typing import Optional


class Email:
    def __init__(self, sender: str, receiver: str, title: str, body: str, timestamp: datetime.time, offset_id: int,
                 is_read: bool = False, is_deleted: bool = False, folder: str = 'inbox', obj_id=""):
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

    def _parse_headers(self, headers):
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

        email = Email(
            sender=header_dict.get('From', ''),
            receiver=header_dict.get('To', ''),
            title=header_dict.get('Subject', ''),
            body='',
            timestamp=datetime.strptime(header_dict.get('Date', ''), "%a, %d %b %Y %H:%M:%S +0000 (UTC)"),
            offset_id=-1
        )
        return email

    def _parse_email(self, raw_email):
        headers, body = raw_email.split('\r\n\r\n', 1)
        email = self._parse_headers(headers)
        email.body = body[:-5]
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

            # Add CC addresses if provided
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
                if obj_id == self._pop3_command("UIDL " + email_offset_id).split(" ")[1]:
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

    def get_email_by_obj_id(self, obj_id: str) -> Optional[Email]:
        """
        获取邮件内容
        :param obj_id: 唯一 ID
        :return:
        """
        try:
            if obj_id == "":
                return None
            offset_id = self.get_offset_id_by_obj_id(obj_id)
            response = self._pop3_command(f'RETR {offset_id}', bypass_ok=True)
            return self._parse_email(response)
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


# 使用示例
if __name__ == "__main__":
    client = EmailClient(
        "smtp-mail.outlook.com",  # SMTP 服务器地址
        587,  # SMTP 端口
        "outlook.office365.com",  # POP 服务器地址
        995,  # POP 端口
        "USERNAME",  # 用户名
        "PASSWORD"  # 密码
    )

    # 发送邮件
    client.send_email(
        "epicmo@whu.edu.cn",
        "Test Subject",
        "<b>This is a test email body.</b>",
        cc_addresses=["1728913755@qq.com"]
    )

    # 获取邮件列表
    email_list = client.get_email_list(offset=1, limit=11)
    print("服务端第1～11封邮件是:", email_list)

    # 获取特定邮件内容
    if email_list:
        email_entity = client.get_email_by_obj_id(email_list[0].obj_id)
        print("偏移量为 ", email_list[0].offset_id, " 的邮件内容是:", email_entity.body)
    # 删除特定邮件
    if email_list:
        delete_response = client.delete_email(email_list[0].obj_id)
        print("已删除邮件，是否成功:", delete_response)