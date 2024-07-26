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
    def __init__(self, email_db:EmailDatabase):
        super(MainWindowUi, self).__init__()
        self.setupUi(self)
        self.list_widget = self.listWidget
        self.stacked_widget = self.stackedWidget
        self.listWidgetInbox = self.listWidgetInbox

        self.email_db = email_db

        # self.main_window.listWidgetInbox.addItem('111')
        # self.listWidgetInbox = CoverageListWidget()
        self.listWidgetInbox.setItemDelegate(EmailDelegate())

        self.listWidgetInbox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidgetInbox.customContextMenuRequested.connect(self.showListContextMenu)
        self.listWidgetInbox.itemClicked.connect(self.onItemClicked)

        self.change_stacked_widget()

    def showListContextMenu(self, pos: QPoint):
        contextMenu = QMenu(self)

        # newAct = QAction('New', self)
        # newAct.triggered.connect(self.addItem)
        # contextMenu.addAction(newAct)

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
        self.email_db.get_all_emails()

    def deleteItem(self):
        selectedItem = self.listWidgetInbox.currentItem()
        if selectedItem:
            self.listWidgetInbox.takeItem(self.listWidgetInbox.row(selectedItem))

    def onItemClicked(self, item: QListWidgetItem):
        # print(item)
        email: Email = item.data(Qt.UserRole)
        # print(email)
        if email:
            self.textBrowser.setHtml(f'<h1 style="color: blue;">{email.sender}</h1><p>{email.title}</p>')

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
                # self.main_win.listWidgetInbox.addItem(elem.title)
                list_item = QListWidgetItem()
                list_item.setData(Qt.UserRole, elem)
                self.main_win.listWidgetInbox.addItem(list_item)

            # 网络可用则再从网络获取邮件
            emails_from_net: List[Email] = self.main_win.client.get_email_list(0, 10)
            for elem in emails_from_net:
                if elem in emails_from_db:
                    continue

                # 新邮件加到数据库
                self.email_db.add_email(elem)

                # 加到列表中
                # self.main_win.listWidgetInbox.addItem(elem.title)
                # self.main_win.listWidgetInbox.setData(Qt.UserRole, elem)

        except Exception as e:
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


class CoverageListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.current_hover_index = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        index = self.indexAt(event.pos())
        if index != self.current_hover_index:
            self.current_hover_index = index
            self.viewport().update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.current_hover_index = None
        self.viewport().update()


class BussLogic(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.sign_in_window = SignInWindowUi()
        self.sign_in_window.pushButtonSignin.clicked.connect(self.click_sign_in)

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

        self.main_window = MainWindowUi(self.email_db)
        self.main_window.listWidget.itemClicked.connect(self.change_folder)
        # self.sub_window = SubWindow()

        self.inboxGetter = SimpleGetInbox(self.main_window, self.email_db)

    def change_folder(self, item):
        print(item.text())
        if item.text() == '收信箱':
            # 启动线程运行任务
            self.inboxGetter.start()

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


# class List_item(QtWidgets.QListWidgetItem):
#     def __init__(self, subject, sender, uid, index):
#         super().__init__()
#         self.uid = uid
#         self.index = index
#         self.widgit = QtWidgets.QWidget()
#         self.subject_label = QtWidgets.QLabel()
#         self.subject_label.setText(subject)
#         self.sender_label = QtWidgets.QLabel()
#         self.sender_label.setText(sender)
#         self.hbox = QtWidgets.QVBoxLayout()
#         self.hbox.addWidget(self.sender_label)
#         self.hbox.addWidget(self.subject_label)
#         self.widgit.setLayout(self.hbox)
#         self.setSizeHint(self.widgit.sizeHint())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    buss = BussLogic()
    buss.sign_in_window.paintEngine()
    buss.sign_in_window.exec()
    # if(BussLogic.win_stage==0):
    #     exit()

    # buss.sub_window.show()

    sys.exit(app.exec_())
