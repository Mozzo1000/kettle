from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QFont, QTextFormat, QColor
from syntax import SyntaxHighlighter


class CodeEditor(QPlainTextEdit):
    def __init__(self, config):
        super().__init__()
        self.config = config
        font = QFont()
        font.setFamily(config.get_setting('General', 'font'))
        font.setPointSize(22)
        self.setFont(font)
        self.setTabStopWidth(30)
        self.highlighter = SyntaxHighlighter(self.document())


        self.current_line_number = None
        self.current_line_color = QColor("#e8e8e8")
        self.cursorPositionChanged.connect(self.highlight_current_line)

    def highlight_current_line(self):
        new_current_line_number = self.textCursor().blockNumber()
        if new_current_line_number != self.current_line_number:
            self.current_line_number = new_current_line_number
            hi_selection = QTextEdit.ExtraSelection()
            hi_selection.format.setBackground(self.current_line_color)
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()
            self.setExtraSelections([hi_selection])