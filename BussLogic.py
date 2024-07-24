# from SignInWindow import Ui_Dialog as SignInWindow_Ui
import data_store
from SigninWindow import Ui_Dialog as SignInWindow_Ui
from MainWindow import Ui_MainWindow as MainWindow_Ui
from SubWindow import MyWidget as SubWindow_Ui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import sys

from mail_api import EmailClient
import traceback
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





class MailServer(Smtp, Pop3):
    def __init__(self):
        self.mail_server = " "
        self.username = " "
        self.password = " "
        self.smtp = None
        self.pop3 = None

    def info_init(self, mail_server, username, password):
        self.mail_server = mail_server
        self.username = username
        self.password = password
        try:
            self.smtp = Smtp(mailserver=mail_server, username=username, password=password)
            self.pop3 = Pop3(mailserver=mail_server, username=username, password=password)
        except Exception as e:
            print(e)
        else:
            print(mail_server, username, password)


class BussLogic:
    def __init__(self):
        self.sign_in_window = SignInWindowUi()
        self.main_window = MainWindowUi()

        self.client = EmailClient(
            "smtp-mail.outlook.com",  # SMTP 服务器地址
            587,  # SMTP 端口
            "outlook.office365.com",  # POP 服务器地址
            995,  # POP 端口
            data_store.USER_NAME,  # 用户名
            data_store.PASSWORD  # 密码
        )

        self.sub_window = SubWindow()

        # self.mail_server = MailServer()
        self.sender_proc = None
        self.sign_in_window.pushButtonSignin.clicked.connect(self.click_sign_in)
        self.main_window.pushButtonSend.clicked.connect(self.click_send)
        self.main_window.pushButtonSave.clicked.connect(self.click_save)
        self.main_window.Reflesh_Button.clicked.connect(self.refresh_recv)
        self.main_window.listWidget.itemClicked.connect(self.show_recv)
        self.main_window.listWidget_2.itemClicked.connect(self.show_mail)
        self.main_window.listWidget.itemClicked.connect(self.show_draft)
        self.main_window.listWidgetDrafts.itemClicked.connect(self.open_draft)
        self.main_window.pushButtonBackToInbox.clicked.connect(self.compose_to_inbox)
        self.main_window.pushButtonComposeAnotherEmail.clicked.connect(self.back_to_comp)
        self.main_window.Delete_Button.clicked.connect(self.delete_mail)
        self.main_window.Resend_button.clicked.connect(self.resend_butt)
        user = 'root'
        password = 'fy'
        host = 'localhost'
        database = 'mail'
        # 创建 EmailDatabase 实例
        self.email_db = EmailDatabase(user=user, password=password, host=host, database=database)

    # 获取草稿
    def get_draft_mail(self):
        # arr = self.email_db.get_draft_emails()
        arr = self.client.get_email_list(0,10)
        print(arr)
        for e in arr:
            if e.folder == 'draft':
                self.main_window.listWidgetDrafts.addItem(e.title)

    def resend_butt(self):
        print('111')

    def delete_mail(self):
        print(self)

    def show_draft(self, item):
        if item.text() == '草稿箱':
            self.main_window.listWidgetDrafts.clear()
            self.get_draft_mail()

    def open_draft(self, item):

        self.main_window.textBrowser_2.setText(msg)

    def compose_to_inbox(self):
        self.main_window.stacked_widget.setCurrentIndex(1)

    def back_to_comp(self):
        self.main_window.lineEditTo.clear()
        self.main_window.lineEditSubject.clear()
        self.main_window.textEdit.clear()
        self.main_window.stacked_widget.setCurrentIndex(0)

    def click_sign_in(self):
        self.mail_server = MailServer()
        mail_server_address, username, password = self.sign_in_window.fetch_info()
        if username == "" or password == "":
            return
        # print(f'{mail_server_address},{username},{password}')
        self.email_db.login(mail_server_address, username, password)
        self.mail_server.info_init(mail_server=mail_server_address, username=username, password=password)
        BussLogic.win_stage = 1
        self.sign_in_window.close()

    def click_send(self):
        print(self)

    def click_save(self):
        print(self)

    def refresh_recv(self):
        print(self)

    def show_recv(self, item):
        if item.text() == 'Inbox':
            print(item)

    def show_mail(self, item):
        print(item)


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
    buss.main_window.show()

    buss.sub_window.show()

    sys.exit(app.exec_())
