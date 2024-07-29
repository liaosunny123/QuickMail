from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QToolBar, QPushButton, QComboBox, QFontComboBox, QColorDialog, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QBrush, QColor, QIcon, QPixmap, QTextCharFormat

class RichTextWidget(QWidget):
    """富文本编辑控件"""
    FONT_SIZE = {
        '42.0': '初号', '36.0': '小初',
        '26.0': '一号', '24.0': '小一',
        '22.0': '二号', '18.0': '小二',
        '16.0': '三号', '15.0': '小三',
        '14.0': '四号', '12.0': '小四',
        '10.5': '五号', '9.0': '小五',
        '7.5': '六号', '6.5': '小六',
        '5.5': '七号', '5': '八号',
        '8': '8', '9': '9',
        '10': '10', '11': '11',
        '12': '12', '14': '14',
        '16': '16', '18': '18',
        '20': '20', '22': '22',
        '24': '24', '26': '26',
        '28': '28', '36': '36',
        '48': '48', '72': '72',
    }

    def __init__(self, *args, **kwargs):
        super(RichTextWidget, self).__init__(*args, **kwargs)
        self.current_font_size = 10.5
        self.current_font_family = 'Arial'
        self.recently_font_color = ['#000000', '#C00000', '#FFC000', '#FFFF00', '#92D050']
        self.recently_font_bg_color = ['#FFFFFF', '#C00000', '#FFC000', '#FFFF00', '#92D050']

        self.layout = QVBoxLayout(self)
        self.tool_bar = QToolBar(self)
        self.tool_bar.setMovable(False)
        self.layout.addWidget(self.tool_bar)

        self.font_bold_action = self.tool_bar.addAction(QIcon('icon/rich_text/bold.png'), '')
        self.font_bold_action.triggered.connect(self.change_font_bold)

        self.font_italic_action = self.tool_bar.addAction(QIcon('icon/rich_text/italic.png'), '')
        self.font_italic_action.triggered.connect(self.change_font_italic)

        self.font_underline_action = self.tool_bar.addAction(QIcon('icon/rich_text/underline.png'), '')
        self.font_underline_action.triggered.connect(self.change_font_underline)

        self.left_action = self.tool_bar.addAction(QIcon('icon/rich_text/left.png'), '')
        self.left_action.triggered.connect(lambda: self.change_row_alignment('left'))

        self.center_action = self.tool_bar.addAction(QIcon('icon/rich_text/center.png'), '')
        self.center_action.triggered.connect(lambda: self.change_row_alignment('center'))

        self.right_action = self.tool_bar.addAction(QIcon('icon/rich_text/right.png'), '')
        self.right_action.triggered.connect(lambda: self.change_row_alignment('right'))

        self.font_selector = QFontComboBox(self)
        self.font_selector.setMaximumWidth(120)
        self.tool_bar.addWidget(self.font_selector)

        self.font_size_selector = QComboBox(self)
        for key, value in self.FONT_SIZE.items():
            self.font_size_selector.addItem(value, key)
        self.font_size_selector.setCurrentText('五号')
        self.font_size_selector.currentIndexChanged.connect(self.change_font_size)
        self.tool_bar.addWidget(self.font_size_selector)

        self.font_color_selector = QPushButton('A', self)
        self.font_color_selector.setToolTip('字体颜色')
        self.font_color_selector.setFixedSize(30, 21)
        self.update_recently_colors(color_type='font_color')
        self.tool_bar.addWidget(self.font_color_selector)

        self.font_bg_color_selector = QPushButton('A', self)
        self.font_bg_color_selector.setToolTip('字体背景色')
        self.font_bg_color_selector.setFixedSize(30, 21)
        self.update_recently_colors(color_type='font_bg_color')
        self.tool_bar.addWidget(self.font_bg_color_selector)

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.tool_bar.setObjectName('toolBar')
        self.setStyleSheet("#toolBar{spacing:2px}")
        init_font = QFont()
        init_font.setPointSizeF(self.current_font_size)
        init_font.setFamily(self.current_font_family)
        self.text_edit.setFont(init_font)

        self.font_selector.activated.connect(self.change_font)

    def update_recently_colors(self, color_type):
        if color_type == 'font_color':
            colors = self.recently_font_color
            color_button = self.font_color_selector
            button_style = 'border:1px solid rgb(220,220,220);'
            if colors:
                button_style += f'color:{colors[0]};'
        elif color_type == 'font_bg_color':
            colors = self.recently_font_bg_color
            color_button = self.font_bg_color_selector
            button_style = 'border:1px solid rgb(220,220,220);'
            if colors:
                button_style += f'background-color:{colors[0]};'
        else:
            return

        old_menu = color_button.menu()
        if old_menu:
            old_menu.deleteLater()

        menu = QMenu()
        for color_item in colors:
            pix = QPixmap(20, 20)
            pix.fill(QColor(color_item))
            ico = QIcon(pix)
            action = menu.addAction(ico, color_item)
            action.setText(f'{color_item.upper()}')
            action.triggered.connect(lambda _, c=color_item: self.change_current_color(color_type, c))

        more_action = menu.addAction(QIcon('icon/rich_text/more.png'), '更多颜色')
        more_action.triggered.connect(lambda: self.select_more_color(color_type))
        color_button.setStyleSheet(button_style)
        color_button.setMenu(menu)

    def select_more_color(self, color_type):
        color = QColorDialog.getColor(parent=self, title='选择颜色')
        if color.isValid():
            color_str = color.name()
            self.set_current_color(color_str.upper(), color_type)

    def change_current_color(self, color_type, color):
        self.set_current_color(color, color_type)

    def set_current_color(self, color, color_type):
        if color_type == 'font_color':
            colors = self.recently_font_color
        elif color_type == 'font_bg_color':
            colors = self.recently_font_bg_color
        else:
            return

        if color in colors:
            colors.remove(color)
        colors.insert(0, color)
        if len(colors) > 5:
            colors.pop()

        self.update_recently_colors(color_type)

        if color_type == 'font_color':
            self.change_font_color(color)
        elif color_type == 'font_bg_color':
            self.change_font_bg_color(color)

    def change_font(self):
        self.current_font_family = self.font_selector.currentFont().family()
        self.update_font()

    def change_font_size(self):
        self.current_font_size = float(self.font_size_selector.currentData())
        self.update_font()

    def update_font(self):
        current_font = QFont()
        current_font.setFamily(self.current_font_family)
        current_font.setPointSizeF(self.current_font_size)
        tc = self.text_edit.textCursor()
        font_format = QTextCharFormat()
        font_format.setFont(current_font)
        tc.mergeCharFormat(font_format)

    def change_font_color(self, color):
        tc = self.text_edit.textCursor()
        font_format = self.text_edit.currentCharFormat()
        font_format.setForeground(QBrush(QColor(color)))
        tc.mergeCharFormat(font_format)

    def change_font_bg_color(self, color):
        tc = self.text_edit.textCursor()
        font_format = self.text_edit.currentCharFormat()
        font_format.setBackground(QBrush(QColor(color)))
        tc.mergeCharFormat(font_format)

    def change_font_italic(self):
        tc = self.text_edit.textCursor()
        font_format = self.text_edit.currentCharFormat()
        font_format.setFontItalic(not font_format.fontItalic())
        tc.mergeCharFormat(font_format)

    def change_font_bold(self):
        tc = self.text_edit.textCursor()
        font_format = self.text_edit.currentCharFormat()
        current_font = font_format.font()
        current_font.setBold(not current_font.bold())
        font_format.setFont(current_font)
        tc.mergeCharFormat(font_format)

    def change_font_underline(self):
        tc = self.text_edit.textCursor()
        font_format = self.text_edit.currentCharFormat()
        font_format.setFontUnderline(not font_format.fontUnderline())
        tc.mergeCharFormat(font_format)

    def change_row_alignment(self, alignment: str):
        if alignment == 'left':
            self.text_edit.setAlignment(Qt.AlignLeft)
        elif alignment == 'right':
            self.text_edit.setAlignment(Qt.AlignRight)
        elif alignment == 'center':
            self.text_edit.setAlignment(Qt.AlignHCenter)
        else:
            return

    def toHtml(self):
        return self.text_edit.toHtml()

    def toPlainText(self):
        return self.text_edit.toPlainText()

    def setHtml(self, html: str):
        return self.text_edit.setHtml(html)
