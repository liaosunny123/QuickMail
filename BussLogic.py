from typing import List

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox

import data_store
from SigninWindow import Ui_Dialog as SignInWindow_Ui
from MainWindow import Ui_MainWindow as MainWindow_Ui
from SubWindow import MyWidget as SubWindow_Ui
from PyQt5 import QtWidgets
import sys

from mail_api import EmailClient
from PyQt5.QtGui import QPixmap, QPainter
from emailDB import *


class SignInWindowUi(SignInWindow_Ui, QtWidgets.QDialog):
    def __init__(self):
        super(SignInWindowUi, self).__init__()
        BussLogic.win_stage = 0
        self.setupUi(self)
        self.mail_server_address = "smtp.qq.com"  # Default
        self.comboBoxServerAddress.activated.connect(self.select_server_address)

    def fetch_info(self):
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        return self.mail_server_address, username, password

    def paintEvent(self, event):  # set background_img
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap("icon\whu_login_background.jpeg")
        painter.drawPixmap(self.rect(), pixmap)

    def select_server_address(self):
        if self.comboBoxServerAddress.currentText() == "QQ Mail":
            self.mail_server_address = "smtp.qq.com"
        elif self.comboBoxServerAddress.currentText() == "WHU E-Mail":
            self.mail_server_address = "smtp.whu.edu.cn"
        elif self.comboBoxServerAddress.currentText() == "Gmail":
            self.mail_server_address = "smtp.google.com"
        elif self.comboBoxServerAddress.currentText() == "163 Mail":
            self.mail_server_address = "smtp.163.com"


class MainWindowUi(MainWindow_Ui, QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowUi, self).__init__()
        self.setupUi(self)
        self.list_widget = self.listWidget
        self.stacked_widget = self.stackedWidget
        self.change_stacked_widget()

    def change_stacked_widget(self):
        self.list_widget.currentRowChanged.connect(self.display_subpage)

    def display_subpage(self, i):
        self.stacked_widget.setCurrentIndex(i)

    def set_text_edit(self, mail_server, username, password):
        text = mail_server + username + password
        self.textEdit.setText(text)


class SubWindow(SubWindow_Ui, QtWidgets.QMainWindow):
    def __init__(self):
        super(SubWindow, self).__init__()
        client = EmailClient(
            "smtp-mail.outlook.com",  # SMTP 服务器地址
            587,  # SMTP 端口
            "outlook.office365.com",  # POP 服务器地址
            995,  # POP 端口
            data_store.USER_NAME,  # 用户名
            data_store.PASSWORD  # 密码
        )

        arr = client.get_email_list(0, 10)
        print(arr)

        for e in arr:
            self.listWidget.addItem(e.title)

        self.textEdit.setHtml(arr[0].title)

        # print(arr[0].title)
        # print(base64.b64decode(arr[0].title).decode("utf-8"))


class SimpleGetInbox(QThread):
    def __init__(self, main_win: MainWindowUi, email_db: EmailDatabase):
        super(SimpleGetInbox, self).__init__()
        self.main_win = main_win
        self.email_db = email_db


    def run(self):
        try:
            self.main_win.listWidgetInbox.clear()

            # 从数据库获取收件箱邮件
            emails_from_db = self.email_db.get_inbox()
            print(emails_from_db)
            for elem in emails_from_db:
                self.main_win.listWidgetInbox.addItem(elem.title)

            # 网络可用则再从网络获取邮件
            emails_from_net:List[Email] = self.main_win.client.get_email_list(0, 10)
            for elem in emails_from_net:
                if elem in emails_from_db:
                    continue

                # 新邮件加到数据库
                self.email_db.add_email(elem)

                # 加到列表中
                self.main_win.listWidgetInbox.addItem(elem.title)

        except Exception as e:
            print(e)


class BussLogic(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.sign_in_window = SignInWindowUi()
        self.sign_in_window.pushButtonSignin.clicked.connect(self.click_sign_in)

        self.main_window = MainWindowUi()
        self.main_window.listWidget.itemClicked.connect(self.change_folder)
        self.main_window.listWidgetInbox.addItem('111')

        # self.sub_window = SubWindow()

        # 默认账号密码
        self.main_window.client = EmailClient(
            "smtp-mail.outlook.com",  # SMTP 服务器地址
            587,  # SMTP 端口
            "outlook.office365.com",  # POP 服务器地址
            995,  # POP 端口
            data_store.USER_NAME,  # 用户名
            data_store.PASSWORD  # 密码
        )

        # 读取数据
        user = data_store.DatabaseConfig.USER
        password = data_store.DatabaseConfig.PASSWORD
        host = data_store.DatabaseConfig.HOST
        database = data_store.DatabaseConfig.DATABASE
        # 创建 EmailDatabase 实例
        self.email_db = EmailDatabase(user=user, password=password, host=host, database=database)

        self.inboxGetter = SimpleGetInbox(self.main_window, self.email_db)

    def change_folder(self, item):
        print(item.text())
        if item.text() == '收信箱':
            # 启动线程运行任务
            self.inboxGetter.start()

    def click_send(self):
        subject = self.lineEditSubject.text()
        to_address = self.lineEditTo.text()
        cc_addresses = self.lineEditTo_2.text().split(
            ',') if self.lineEditTo_2.text() else []  # Assuming comma separated CC addresses
        body = self.textEdit.toPlainText()

        if not to_address or not subject or not body:
            QMessageBox.warning(self, 'Error', '请填写完整的邮件信息')
            return

        try:
            success = self.main_window.client.send_email(to_address, subject, body, cc_addresses)
            if success:
                QMessageBox.information(self, 'Success', '邮件发送成功')
            else:
                QMessageBox.warning(self, 'Error', '邮件发送失败')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'邮件发送失败: {str(e)}')






    def click_sign_in(self):
        mail_server_address, username, password = self.sign_in_window.fetch_info()
        if username == "" or password == "":
            QMessageBox.warning(self, 'Error', '请输入用户名密码')
            return
        print(f'{mail_server_address},{username},{password}')

        try:
            self.email_db.login(mail_server_address, username, password)

            # 根据输入内容修改客户端
            # self.client = EmailClient(
            #     "smtp-mail.outlook.com",  # SMTP 服务器地址
            #     587,  # SMTP 端口
            #     "outlook.office365.com",  # POP 服务器地址
            #     995,  # POP 端口
            #     username,  # 用户名
            #     password  # 密码
            # )

            BussLogic.win_stage = 1
            self.sign_in_window.close()
            self.main_window.show()
        except Exception as e:
            print(f"Caught an exception: {e}")
            QMessageBox.warning(self, "提示", f"{e}")


class List_item(QtWidgets.QListWidgetItem):
    def __init__(self, subject, sender, uid, index):
        super().__init__()
        self.uid = uid
        self.index = index
        self.widgit = QtWidgets.QWidget()
        self.subject_label = QtWidgets.QLabel()
        self.subject_label.setText(subject)
        self.sender_label = QtWidgets.QLabel()
        self.sender_label.setText(sender)
        self.hbox = QtWidgets.QVBoxLayout()
        self.hbox.addWidget(self.sender_label)
        self.hbox.addWidget(self.subject_label)
        self.widgit.setLayout(self.hbox)
        self.setSizeHint(self.widgit.sizeHint())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    buss = BussLogic()
    buss.sign_in_window.paintEngine()
    buss.sign_in_window.exec()
    # if(BussLogic.win_stage==0):
    #     exit()

    # buss.sub_window.show()

    sys.exit(app.exec_())
