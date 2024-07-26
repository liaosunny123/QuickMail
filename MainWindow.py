# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from richText import RichTextWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1069, 711)
        MainWindow.setMinimumSize(QtCore.QSize(1069, 711))
        MainWindow.setMaximumSize(QtCore.QSize(106900, 71100))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("image/dove1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 181, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("image/pencil2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon1)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("image/sended.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon2)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        item.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("image/inbox.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon3)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("image/contacts.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon4)
        self.listWidget.addItem(item)
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(220, 20, 821, 671))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.horizontalLayoutWidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.pageCompose = QtWidgets.QWidget()
        self.pageCompose.setObjectName("pageCompose")
        self.labelNewMail = QtWidgets.QLabel(self.pageCompose)
        self.labelNewMail.setGeometry(QtCore.QRect(10, 0, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei Light")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelNewMail.setFont(font)
        self.labelNewMail.setObjectName("labelNewMail")
        self.labelTo = QtWidgets.QLabel(self.pageCompose)
        self.labelTo.setGeometry(QtCore.QRect(10, 40, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei Light")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelTo.setFont(font)
        self.labelTo.setObjectName("labelTo")
        self.lineEditTo = QtWidgets.QLineEdit(self.pageCompose)
        self.lineEditTo.setGeometry(QtCore.QRect(90, 40, 721, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.lineEditTo.setFont(font)
        self.lineEditTo.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEditTo.setText("")
        self.lineEditTo.setObjectName("lineEditTo")
        self.labelSubject = QtWidgets.QLabel(self.pageCompose)
        self.labelSubject.setGeometry(QtCore.QRect(20, 120, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei Light")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelSubject.setFont(font)
        self.labelSubject.setObjectName("labelSubject")
        self.lineEditSubject = QtWidgets.QLineEdit(self.pageCompose)
        self.lineEditSubject.setGeometry(QtCore.QRect(90, 120, 721, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.lineEditSubject.setFont(font)
        self.lineEditSubject.setText("")
        self.lineEditSubject.setObjectName("lineEditSubject")

        self.rich_text_widget = RichTextWidget(self.pageCompose)
        self.rich_text_widget.setGeometry(QtCore.QRect(10, 160, 801, 451))
        self.rich_text_widget.setObjectName("rich_text_widget")

        self.pushButtonSend = QtWidgets.QPushButton(self.pageCompose)
        self.pushButtonSend.setGeometry(QtCore.QRect(290, 620, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.pushButtonSend.setFont(font)
        self.pushButtonSend.setObjectName("pushButtonSend")
        self.pushButtonSave = QtWidgets.QPushButton(self.pageCompose)
        self.pushButtonSave.setGeometry(QtCore.QRect(450, 620, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.pushButtonSave.setFont(font)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.labelTo_2 = QtWidgets.QLabel(self.pageCompose)
        self.labelTo_2.setGeometry(QtCore.QRect(20, 80, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei Light")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelTo_2.setFont(font)
        self.labelTo_2.setObjectName("labelTo_2")
        self.lineEditTo_2 = QtWidgets.QLineEdit(self.pageCompose)
        self.lineEditTo_2.setGeometry(QtCore.QRect(90, 80, 721, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.lineEditTo_2.setFont(font)
        self.lineEditTo_2.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEditTo_2.setText("")
        self.lineEditTo_2.setObjectName("lineEditTo_2")
        self.stackedWidget.addWidget(self.pageCompose)
        self.pageSended = QtWidgets.QWidget()
        self.pageSended.setObjectName("pageSended")
        self.stackedWidget.addWidget(self.pageSended)
        self.pageInbox = QtWidgets.QWidget()
        self.pageInbox.setObjectName("pageInbox")
        self.listWidgetInbox = QtWidgets.QListWidget(self.pageInbox)
        self.listWidgetInbox.setGeometry(QtCore.QRect(0, 40, 281, 631))
        self.listWidgetInbox.setObjectName("listWidgetInbox")
        self.inboxTextBrowser = QtWidgets.QTextBrowser(self.pageInbox)
        self.inboxTextBrowser.setGeometry(QtCore.QRect(280, 0, 541, 671))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.inboxTextBrowser.setFont(font)
        self.inboxTextBrowser.setObjectName("inboxTextBrowser")
        self.Reflesh_Button = QtWidgets.QPushButton(self.pageInbox)
        self.Reflesh_Button.setGeometry(QtCore.QRect(240, 0, 40, 40))
        self.Reflesh_Button.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("image/refresh2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Reflesh_Button.setIcon(icon5)
        self.Reflesh_Button.setIconSize(QtCore.QSize(40, 40))
        self.Reflesh_Button.setObjectName("Reflesh_Button")
        self.Delete_Button = QtWidgets.QPushButton(self.pageInbox)
        self.Delete_Button.setGeometry(QtCore.QRect(770, 620, 40, 40))
        self.Delete_Button.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("image/TRASH BIN.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Delete_Button.setIcon(icon6)
        self.Delete_Button.setIconSize(QtCore.QSize(40, 40))
        self.Delete_Button.setObjectName("Delete_Button")
        self.listWidget_4 = QtWidgets.QListWidget(self.pageInbox)
        self.listWidget_4.setGeometry(QtCore.QRect(0, 0, 281, 40))
        self.listWidget_4.setObjectName("listWidget_4")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setIcon(icon3)
        self.listWidget_4.addItem(item)
        self.listWidgetInbox.raise_()
        self.inboxTextBrowser.raise_()
        self.Delete_Button.raise_()
        self.listWidget_4.raise_()
        self.Reflesh_Button.raise_()
        self.stackedWidget.addWidget(self.pageInbox)
        self.pageDrafts = QtWidgets.QWidget()
        self.pageDrafts.setObjectName("pageDrafts")
        self.listWidgetDrafts = QtWidgets.QListWidget(self.pageDrafts)
        self.listWidgetDrafts.setGeometry(QtCore.QRect(0, 40, 281, 631))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listWidgetDrafts.setFont(font)
        self.listWidgetDrafts.setObjectName("listWidgetDrafts")
        self.draftsTextBrowser = QtWidgets.QTextBrowser(self.pageDrafts)
        self.draftsTextBrowser.setGeometry(QtCore.QRect(281, 0, 541, 671))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.draftsTextBrowser.setFont(font)
        self.draftsTextBrowser.setObjectName("draftsTextBrowser")
        self.Resend_button = QtWidgets.QPushButton(self.pageDrafts)
        self.Resend_button.setGeometry(QtCore.QRect(740, 620, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Resend_button.setFont(font)
        self.Resend_button.setObjectName("Resend_button")
        self.listWidget_5 = QtWidgets.QListWidget(self.pageDrafts)
        self.listWidget_5.setGeometry(QtCore.QRect(0, 0, 281, 40))
        self.listWidget_5.setObjectName("listWidget_5")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setIcon(icon4)
        self.listWidget_5.addItem(item)
        self.stackedWidget.addWidget(self.pageDrafts)
        self.pageEmailSent = QtWidgets.QWidget()
        self.pageEmailSent.setObjectName("pageEmailSent")
        self.label = QtWidgets.QLabel(self.pageEmailSent)
        self.label.setGeometry(QtCore.QRect(320, 100, 111, 101))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("image/EmailSentIcon.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.pageEmailSent)
        self.label_2.setGeometry(QtCore.QRect(320, 200, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButtonBackToInbox = QtWidgets.QPushButton(self.pageEmailSent)
        self.pushButtonBackToInbox.setGeometry(QtCore.QRect(180, 300, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.pushButtonBackToInbox.setFont(font)
        self.pushButtonBackToInbox.setObjectName("pushButtonBackToInbox")
        self.pushButtonComposeAnotherEmail = QtWidgets.QPushButton(self.pageEmailSent)
        self.pushButtonComposeAnotherEmail.setGeometry(QtCore.QRect(360, 300, 221, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.pushButtonComposeAnotherEmail.setFont(font)
        self.pushButtonComposeAnotherEmail.setObjectName("pushButtonComposeAnotherEmail")
        self.stackedWidget.addWidget(self.pageEmailSent)
        self.horizontalLayout.addWidget(self.stackedWidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEditTo, self.lineEditSubject)
        MainWindow.setTabOrder(self.lineEditSubject, self.pushButtonSend)
        MainWindow.setTabOrder(self.pushButtonSend, self.pushButtonSave)
        MainWindow.setTabOrder(self.pushButtonSave, self.listWidget_4)
        MainWindow.setTabOrder(self.listWidget_4, self.Reflesh_Button)
        MainWindow.setTabOrder(self.Reflesh_Button, self.listWidgetInbox)
        MainWindow.setTabOrder(self.listWidgetInbox, self.inboxTextBrowser)
        MainWindow.setTabOrder(self.inboxTextBrowser, self.Delete_Button)
        MainWindow.setTabOrder(self.Delete_Button, self.listWidgetDrafts)
        MainWindow.setTabOrder(self.listWidgetDrafts, self.draftsTextBrowser)
        MainWindow.setTabOrder(self.draftsTextBrowser, self.Resend_button)
        MainWindow.setTabOrder(self.Resend_button, self.pushButtonBackToInbox)
        MainWindow.setTabOrder(self.pushButtonBackToInbox, self.pushButtonComposeAnotherEmail)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EasyMail"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "写信"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "已发送"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "收信箱"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "草稿箱"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.labelNewMail.setText(_translate("MainWindow", "新邮件"))
        self.labelTo.setText(_translate("MainWindow", "收件方"))
        self.labelSubject.setText(_translate("MainWindow", "主题"))
        self.pushButtonSend.setText(_translate("MainWindow", "发送"))
        self.pushButtonSave.setText(_translate("MainWindow", "保存"))
        self.labelTo_2.setText(_translate("MainWindow", "抄送"))
        self.inboxTextBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        __sortingEnabled = self.listWidget_4.isSortingEnabled()
        self.listWidget_4.setSortingEnabled(False)
        item = self.listWidget_4.item(0)
        item.setText(_translate("MainWindow", "Inbox"))
        self.listWidget_4.setSortingEnabled(__sortingEnabled)
        self.Resend_button.setText(_translate("MainWindow", "Send"))
        __sortingEnabled = self.listWidget_5.isSortingEnabled()
        self.listWidget_5.setSortingEnabled(False)
        item = self.listWidget_5.item(0)
        item.setText(_translate("MainWindow", "Drafts"))
        self.listWidget_5.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("MainWindow", "邮件成功发送"))
        self.pushButtonBackToInbox.setText(_translate("MainWindow", "回到收信箱"))
        self.pushButtonComposeAnotherEmail.setText(_translate("MainWindow", "编写另一封邮件"))
