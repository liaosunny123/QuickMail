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

        self.pushButtonSend.clicked.connect(self.click_send)
        self.pushButtonSave.clicked.connect(self.click_save)



        self.list_widget.currentRowChanged.connect(self.display_subpage)


        self.sentGetter = SimpleGetSent(self, self.email_db)
        self.inboxGetter = SimpleGetInbox(self, self.email_db)
        self.draftsGetter = SimpleGetDrafts(self, self.email_db)

        self.listWidget.itemClicked.connect(self.change_folder)

        self.listWidgetSent.setItemDelegate(EmailDelegate())
        self.listWidgetSent.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidgetSent.customContextMenuRequested.connect(self.showListContextMenu)
        self.listWidgetSent.itemClicked.connect(self.onItemClicked)

        self.listWidgetInbox.setItemDelegate(EmailDelegate())
        self.listWidgetInbox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidgetInbox.customContextMenuRequested.connect(self.showListContextMenu)
        self.listWidgetInbox.itemClicked.connect(self.onItemClicked)

        self.listWidgetDrafts.setItemDelegate(EmailDelegate())
        self.listWidgetDrafts.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidgetDrafts.customContextMenuRequested.connect(self.showListContextMenu)
        self.listWidgetDrafts.itemClicked.connect(self.onItemClicked)




        self.client = EmailClient(
            "smtp-mail.outlook.com",  # SMTP 服务器地址
            587,  # SMTP 端口
            "outlook.office365.com",  # POP 服务器地址
            995,  # POP 端口,  # SMTP 服务器地址
            data_store.USER_NAME,  # 用户名
            data_store.PASSWORD  # 密码
        )


    def display_subpage(self, i):
        self.stacked_widget.setCurrentIndex(i)
        if (i == 0):
            self.DividingLine.show()
        else:
            self.DividingLine.hide()

    def change_folder(self, item):
        if item.text() == '已发送':
            self.sentGetter.start()
        if item.text() == '收信箱':
            self.inboxGetter.start()
        if item.text() == '草稿箱':
            self.draftsGetter.start()


    def click_send(self):
        recipient = self.lineEditTo.text().strip()
        cc = self.lineEditTo_2.text().split(';') if self.lineEditTo_2.text() else []
        cc = [email.strip() for email in cc if email.strip()]
        subject = self.lineEditSubject.text()
        body = self.rich_text_widget.toHtml()

        if not recipient or not subject or not body:
            QMessageBox.warning(self, 'Error', '请填写完整的邮件信息')
            return

        try:
            if cc:
                success = self.client.send_email(recipient, subject, body, cc)
            else:
                success = self.client.send_email(recipient, subject, body)
            if success:
                QMessageBox.information(self, 'Success', '邮件发送成功')

                # 创建 Email 对象
                email = Email(
                    sender=data_store.USER_NAME,  # 记得改回登录账号
                    receiver=recipient,
                    copy_for=';'.join(cc),
                    title=subject,
                    body=body,
                    timestamp=datetime.utcnow(),
                    folder="sent",
                )

                try:
                    self.email_db.add_email(email)
                except Exception as e:
                    QMessageBox.warning(self, 'Error', f'保存到数据库失败: {str(e)}')
                    return

                self.clear_input_fields()
                self.listWidget.setCurrentRow(1)
                self.sentGetter.start()
                #选中当前的

            else:
                QMessageBox.warning(self, 'Error', '邮件发送失败')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'邮件发送失败: {str(e)}')

    def click_save(self):
        recipient = self.lineEditTo.text()
        cc = self.lineEditTo_2.text()
        subject = self.lineEditSubject.text()
        body = self.rich_text_widget.toHtml()

        email = Email(
            sender=data_store.USER_NAME,  # 记得改回登录账号
            receiver=recipient,
            copy_for=';'.join(cc),
            title=subject,
            body=body,
            timestamp=datetime.utcnow(),
            folder="drafts"
        )

        try:
            self.email_db.add_email(email)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'保存到数据库失败: {str(e)}')
            return

        self.clear_input_fields()
        self.listWidget.setCurrentRow(3)
        self.draftsGetter.start()


    def clear_input_fields(self):
        self.lineEditTo.clear()
        self.lineEditTo_2.clear()
        self.lineEditSubject.clear()
        self.rich_text_widget.text_edit.clear()


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
        if self.listWidget.currentItem().text() == '已发送':
            self.sentGetter.start()

        if self.listWidget.currentItem().text() == '收件箱':
            self.inboxGetter.start()

        if self.listWidget.currentItem().text() == '草稿箱':
            self.draftsGetter.start()

    def onItemClicked(self, item: QListWidgetItem):
        # print(item)
        email: Email = item.data(Qt.UserRole)
        if email:
            if self.listWidget.currentItem().text() == '已发送':
                print(email)
                self.sentTextBrowser.setHtml(f"""
                   <h2 style="color: #0073e6; margin-bottom: 10px;">{email.title}</h2>
                   <p style="margin: 5px 3px;"><strong>发件人:</strong> {email.sender}</p>
                   <p style="margin: 5px 3px;"><strong>收件人:</strong> {email.receiver}</p>
                   <p style="margin: 5px 3px;"><strong>抄送人:</strong> {email.copy_for}</p>
                   <p style="margin: 5px 3px 2px 3px;"><strong>时间:</strong> {email.timestamp}</p>
                   <hr style="margin: 0;">
                   <p style="margin: 3px 3px;"><strong>正文:</strong></p>
                   <div style="margin: 3px 3px;">{email.body}</div>
                   """)

            if self.listWidget.currentItem().text() == '收信箱':
                self.inboxTextBrowser.setHtml(f"""
                   <h2 style="color: #0073e6; margin-bottom: 10px;">{email.title}</h2>
                   <p style="margin: 5px 3px;"><strong>发件人:</strong> {email.sender}</p>
                   <p style="margin: 5px 3px;"><strong>收件人:</strong> {email.receiver}</p>
                   <p style="margin: 5px 3px;"><strong>抄送人:</strong> {email.copy_for}</p>
                   <p style="margin: 5px 3px 2px 3px;"><strong>时间:</strong> {email.timestamp}</p>
                   <hr style="margin: 0;">
                   <p style="margin: 3px 3px;"><strong>正文:</strong></p>
                   <div style="margin: 3px 3px;">{email.body}</div>
                   """)

            if self.listWidget.currentItem().text() == '草稿箱':
                self.draftLineEditTo.setText(email.sender)
                self.draftLineEditCopyTo.setText(email.copy_for)
                self.draftLabelEditSubject.setText(email.title)
                self.draftsTextBrowser.setHtml(email.body)

    def clearDraftFields(self):
        self.draftLineEditTo.clear()
        self.draftLineEditCopyTo.clear()
        self.draftLabelEditSubject.clear()
        self.draftsTextBrowser.text_edit.clear()


    def deleteItem(self):

        if self.listWidget.currentItem().text() == '已发送':
            selectedItem = self.listWidgetSent.currentItem()
            if selectedItem:
                self.listWidgetSent.takeItem(self.listWidgetSent.row(selectedItem))
                email = selectedItem.data(Qt.UserRole)
                self.email_db.delete_email(email.obj_id, "sent")
                self.sentTextBrowser.clear()

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
                self.email_db.delete_email(email.obj_id, "inbox")
                self.inboxTextBrowser.clear()

        if self.listWidget.currentItem().text() == '草稿箱':
            selectedItem = self.listWidgetDrafts.currentItem()
            if selectedItem:
                self.listWidgetDrafts.takeItem(self.listWidgetDrafts.row(selectedItem))
                email = selectedItem.data(Qt.UserRole)
                self.email_db.delete_email(email.obj_id, "drafts")
                self.clearDraftFields()



class SimpleGetEmail(QThread):
    def __init__(self, main_win: MainWindowUi, email_db: EmailDatabase):
        super(SimpleGetEmail, self).__init__()
        self.main_win = main_win
        self.email_db = email_db

class SimpleGetSent(SimpleGetEmail):
    def run(self):
        try:
            self.main_win.listWidgetSent.clear()
            # 从数据库获取已发送邮件
            emails = self.email_db.get_sent_emails()
            print(emails)
            for email in emails:
                list_item = QListWidgetItem()
                list_item.setData(Qt.UserRole, email)
                self.main_win.listWidgetSent.addItem(list_item)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'获取数据库的邮件失败: {str(e)}')
            print(e)

class SimpleGetInbox(SimpleGetEmail):
    def run(self):
        try:
            self.main_win.listWidgetInbox.clear()

            # 从数据库获取收件箱邮件
            emails_from_db = self.email_db.get_inbox()
            print("inbox: ", emails_from_db)
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
            emails_from_net: List[Email] = client.get_email_list(offset=0, limit=9999)
            for elem in emails_from_net:
                if elem in emails_from_db:
                    continue

                # 新邮件加到数据库
                self.email_db.add_email(elem)


        except Exception as e:
            # QMessageBox.warning(self.main_win, "出错", f'出错了：{e}')
            print(e)


class SimpleGetDrafts(SimpleGetEmail):
    def run(self):
        try:
            self.main_win.listWidgetDrafts.clear()

            # 从数据库获取草稿
            drafts_from_db = self.email_db.get_draft_emails()
            print("drafts: ", drafts_from_db)

            # 展示到列表
            for elem in drafts_from_db:
                # self.main_win.listWidgetInbox.addItem(elem.title)
                list_item = QListWidgetItem()
                list_item.setData(Qt.UserRole, elem)
                self.main_win.listWidgetDrafts.addItem(list_item)

        except Exception as e:
            # QMessageBox.warning(self.main_win, "出错", f'出错了：{e}')
            print(e)


class EmailDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        email: [Email] = index.data(Qt.UserRole)
        if email:
            rect = option.rect
            sender = email.sender
            receiver=email.receiver
            subject = email.title
            type= email.folder

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
            if type=="inbox" :
                painter.drawText(inner_rect.adjusted(10, 5, -10, -inner_rect.height() // 2), Qt.AlignLeft, f"<{sender}>")
            else :
                painter.drawText(inner_rect.adjusted(10, 5, -10, -inner_rect.height() // 2), Qt.AlignLeft,
                                 f"<{receiver}>")
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
