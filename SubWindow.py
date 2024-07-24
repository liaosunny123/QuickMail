import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QAction, QListWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QInputDialog

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Test Window')

        layout = QHBoxLayout()

        # 左侧列表
        self.listWidget = QListWidget()
        # self.listWidget.addItems(['Item 1', 'Item 2', 'Item 3', 'Item 4'])
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.showListContextMenu)

        # 右侧富文本编辑器
        self.textEdit = QTextEdit()
        self.textEdit.setAcceptRichText(True)

        layout.addWidget(self.listWidget)
        layout.addWidget(self.textEdit)

        self.setLayout(layout)

    def showListContextMenu(self, pos: QPoint):
        contextMenu = QMenu(self)

        # newAct = QAction('New', self)
        # newAct.triggered.connect(self.addItem)
        # contextMenu.addAction(newAct)

        # openAct = QAction('Open', self)
        # contextMenu.addAction(openAct)


        refreshAct = QAction('Refresh', self)
        contextMenu.addAction(refreshAct)

        selectedItem = self.listWidget.itemAt(pos)
        if selectedItem:
            deleteAct = QAction('Delete', self)
            deleteAct.triggered.connect(self.deleteItem)
            contextMenu.addAction(deleteAct)

        quitAct = QAction('Quit', self)
        contextMenu.addAction(quitAct)
        quitAct.triggered.connect(QApplication.quit)

        contextMenu.exec_(self.listWidget.mapToGlobal(pos))

    def deleteItem(self):
        selectedItem = self.listWidget.currentItem()
        if selectedItem:
            self.listWidget.takeItem(self.listWidget.row(selectedItem))

    # def addItem(self):
    #     text, ok = QInputDialog.getText(self, 'Add Item', 'Enter new item:')
    #     if ok and text:
    #         self.listWidget.addItem(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
