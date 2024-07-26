from typing import List

from PyQt5.QtCore import QThread, Qt, QRect, QPoint
from PyQt5.QtWidgets import QMessageBox, QStyledItemDelegate, QStyle, QListWidget, QListWidgetItem, QMenu, QAction, \
    QApplication

import data_store
from SigninWindow import Ui_Dialog as SignInWindow_Ui
from MainWindow import Ui_MainWindow as MainWindow_Ui
from SubWindow import MyWidget as SubWindow_Ui
from PyQt5 import QtWidgets
import sys

from mail_api import EmailClient
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
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
    def __init__(self, email_db: EmailDatabase):
        super(MainWindowUi, self).__init__()
        self.setupUi(self)
        self.list_widget = self.listWidget
        self.stacked_widget = self.stackedWidget
        self.listWidgetInbox = self.listWidgetInbox

        self.email_db = email_db
        # self.sub_window = SubWindow()

        self.inboxGetter = SimpleGetInbox(self, self.email_db)
        self.draftsGetter = SimpleGetDrafts(self, self.email_db)

        self.listWidget.itemClicked.connect(self.change_folder)

        # self.main_window.listWidgetInbox.addItem('111')
        # self.listWidgetInbox = CoverageListWidget()
        self.listWidgetInbox.setItemDelegate(EmailDelegate())

        self.listWidgetInbox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidgetInbox.customContextMenuRequested.connect(self.showListContextMenu)
        self.listWidgetInbox.itemClicked.connect(self.onItemClicked)

        self.listWidgetDrafts.setItemDelegate(EmailDelegate())

        self.listWidgetDrafts.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidgetDrafts.customContextMenuRequested.connect(self.showListContextMenu)
        self.listWidgetDrafts.itemClicked.connect(self.onItemClicked)

        self.inboxTextBrowser.setHtml('<h1 style="color: green;">选一个邮件查看内容</h1>')
        self.draftsTextBrowser.setHtml('<h1 style="color: green;">选一个邮件查看内容</h1>')

        self.change_stacked_widget()

    def change_folder(self, item):
        print(item.text())
        if item.text() == '收信箱':
            # 启动线程运行任务
            self.inboxGetter.start()

    def showListContextMenu(self, pos: QPoint):
        contextMenu = QMenu(self)

        refresh_act = QAction('刷新', self)
        refresh_act.triggered.connect(self.refreshList)
        contextMenu.addAction(refresh_act)

        selectedItem = self.listWidgetInbox.itemAt(pos)
        if selectedItem:
            deleteAct = QAction('删除', self)
            deleteAct.triggered.connect(self.deleteItem)
            contextMenu.addAction(deleteAct)

        quitAct = QAction('退出', self)
        contextMenu.addAction(quitAct)
        quitAct.triggered.connect(QApplication.quit)

        contextMenu.exec_(self.listWidgetInbox.mapToGlobal(pos))

    def refreshList(self):
        if self.listWidget.currentItem().text() == '收件箱':
            self.inboxGetter.start()

        if self.listWidget.currentItem().text() == '草稿箱':
            self.draftsGetter.start()

    def deleteItem(self):
        if self.listWidget.currentItem().text() == '收件箱':
            selectedItem = self.listWidgetInbox.currentItem()
            if selectedItem:
                self.listWidgetInbox.takeItem(self.listWidgetInbox.row(selectedItem))
                email = selectedItem.data(Qt.UserRole)
                # 默认账号密码
                client = EmailClient(
                    data_store.EmailConfig.SMTP_SERVER,  # SMTP 服务器地址
                    data_store.EmailConfig.SMTP_PORT,  # SMTP 端口
                    data_store.EmailConfig.POP_SERVER,  # POP 服务器地址
                    data_store.EmailConfig.POP_PORT,  # POP 端口
                    data_store.USER_NAME,  # 用户名
                    data_store.PASSWORD  # 密码
                )

                client.delete_email(email.obj_id)
                self.email_db.delete_email(email.obj_id)

        if self.listWidget.currentItem().text() == '草稿箱':
            selectedItem = self.listWidgetDrafts.currentItem()
            if selectedItem:
                self.listWidgetDrafts.takeItem(self.listWidgetDrafts.row(selectedItem))
                email = selectedItem.data(Qt.UserRole)

                # 删除草稿箱？
                # client.delete_email(email.obj_id)

    def onItemClicked(self, item: QListWidgetItem):
        # print(item)
        email: Email = item.data(Qt.UserRole)
        # client = EmailClient(
        #     data_store.EmailConfig.SMTP_SERVER,  # SMTP 服务器地址
        #     data_store.EmailConfig.SMTP_PORT,  # SMTP 端口
        #     data_store.EmailConfig.POP_SERVER,  # POP 服务器地址
        #     data_store.EmailConfig.POP_PORT,  # POP 端口
        #     data_store.USER_NAME,  # 用户名
        #     data_store.PASSWORD  # 密码
        # )
        # print(email)
        if email:
            # TODO 这里一调用就报错，无法解析 body：UnicodeDecodeError('utf-8',xxx)
            # fullEmail = client.get_email_by_obj_id(email.obj_id)
            # self.inboxTextBrowser.setHtml(fullEmail)
            # self.draftsTextBrowser.setHtml(fullEmail)
            self.inboxTextBrowser.setHtml(f'<h1 style="color: blue;">{email.sender}</h1><p>{email.title}</p>')
            self.draftsTextBrowser.setHtml(f'<h1 style="color: blue;">{email.sender}</h1><p>{email.title}</p>')

    def change_stacked_widget(self):
        self.list_widget.currentRowChanged.connect(self.display_subpage)

    def display_subpage(self, i):
        self.stacked_widget.setCurrentIndex(i)


class SimpleGetEmail(QThread):
    def __init__(self, main_win: MainWindowUi, email_db: EmailDatabase):
        super(SimpleGetEmail, self).__init__()
        self.main_win = main_win
        self.email_db = email_db


class SimpleGetInbox(SimpleGetEmail):
    def run(self):
        try:
            self.main_win.listWidgetInbox.clear()

            # 从数据库获取收件箱邮件
            emails_from_db = self.email_db.get_inbox()
            print(emails_from_db)
            for elem in emails_from_db:
                # self.main_win.listWidgetInbox.addItem(elem.title)
                list_item = QListWidgetItem()
                list_item.setData(Qt.UserRole, elem)
                self.main_win.listWidgetInbox.addItem(list_item)

            # 默认账号密码
            client = EmailClient(
                data_store.EmailConfig.SMTP_SERVER,  # SMTP 服务器地址
                data_store.EmailConfig.SMTP_PORT,  # SMTP 端口
                data_store.EmailConfig.POP_SERVER,  # POP 服务器地址
                data_store.EmailConfig.POP_PORT,  # POP 端口
                data_store.USER_NAME,  # 用户名
                data_store.PASSWORD  # 密码
            )
            # 网络可用则再从网络获取邮件
            emails_from_net: List[Email] = client.get_email_list(0, 10)
            for elem in emails_from_net:
                if elem in emails_from_db:
                    continue

                # 新邮件加到数据库
                self.email_db.add_email(elem)

                # 加到列表中
                # self.main_win.listWidgetInbox.addItem(elem.title)
                # self.main_win.listWidgetInbox.setData(Qt.UserRole, elem)
        except Exception as e:
            # QMessageBox.warning(self.main_win, "出错", f'出错了：{e}')
            print(e)


class SimpleGetDrafts(SimpleGetEmail):
    def run(self):
        try:
            self.main_win.listWidgetDrafts.clear()

            # 从数据库获取草稿
            drafts_from_db = self.email_db.get_draft_emails()
            print(drafts_from_db)

            # 展示到列表
            for elem in drafts_from_db:
                # self.main_win.listWidgetInbox.addItem(elem.title)
                list_item = QListWidgetItem()
                list_item.setData(Qt.UserRole, elem)
                self.main_win.listWidgetInbox.addItem(list_item)

        except Exception as e:
            # QMessageBox.warning(self.main_win, "出错", f'出错了：{e}')
            print(e)


class EmailDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        email: [Email] = index.data(Qt.UserRole)
        # print("133: ", email)
        if email:
            rect = option.rect
            sender = email.sender
            subject = email.title

            # Adjust rect to provide spacing between items
            margin = 2
            inner_rect = QRect(rect.left() + margin, rect.top() + margin, rect.width() - 2 * margin,
                               rect.height() - 2 * margin)

            # Set background color
            if option.state & QStyle.State_Selected:
                painter.fillRect(inner_rect, option.palette.highlight())
            elif option.state & QStyle.State_MouseOver:
                painter.fillRect(inner_rect, QColor("#AED6F1"))
            else:
                painter.fillRect(inner_rect, QColor("#D6EAF8"))

            # Draw sender
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            painter.setPen(Qt.black)
            painter.drawText(inner_rect.adjusted(10, 5, -10, -inner_rect.height() // 2), Qt.AlignLeft, f"<{sender}>")

            # Draw subject
            painter.setFont(QFont("Arial", 10))
            painter.setPen(Qt.black)
            painter.drawText(inner_rect.adjusted(10, inner_rect.height() // 2, -10, -5), Qt.AlignLeft, subject)

        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() + 50)
        return size


class BussLogic(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.sign_in_window = SignInWindowUi()
        self.sign_in_window.pushButtonSignin.clicked.connect(self.click_sign_in)

        # 读取数据
        user = data_store.DatabaseConfig.USER
        password = data_store.DatabaseConfig.PASSWORD
        host = data_store.DatabaseConfig.HOST
        database = data_store.DatabaseConfig.DATABASE
        # 创建 EmailDatabase 实例
        self.email_db = EmailDatabase(user=user, password=password, host=host, database=database)

        self.main_window = MainWindowUi(self.email_db)

    def click_sign_in(self):
        mail_server_address, username, password = self.sign_in_window.fetch_info()
        if username == "" or password == "":
            QMessageBox.warning(self, 'Error', '请输入用户名密码')
            return
        print(f'{mail_server_address},{username},{password}')

        try:
            self.email_db.login(mail_server_address, username, password)

            # 根据输入的用户名密码修改pop和smtp的用户名密码
            # data_store.USER_NAME = username
            # data_store.PASSWORD = password
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    buss = BussLogic()
    buss.sign_in_window.paintEngine()
    buss.sign_in_window.exec()
    # if(BussLogic.win_stage==0):
    #     exit()

    # buss.sub_window.show()

    sys.exit(app.exec_())
