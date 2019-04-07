from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(SyntaxHighlighter, self).__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(255, 152, 0))
        keyword_format.setFontWeight(QFont.Bold)

        keyword_patterns = ["\\bclass\\b", "\\bprint\\b", "\\bif\\b", "\\belse\\b",
                            "\\bdef\\b", "\\bsuper\\b", "\\bself\\b", "\\bimport\\b",
                            "\\bTrue\\b", "\\bFalse\\b", "\\bfrom\\b"]

        self.highlightning_rules = [(QRegExp(pattern), keyword_format)
                                    for pattern in keyword_patterns]

        """class_format = QTextCharFormat()
        class_format.setForeground(Qt.darkGreen)
        class_format.setFontWeight(QFont.Bold)
        self.highlightning_rules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
                                         class_format))"""

        single_line_comment_format = QTextCharFormat()
        single_line_comment_format.setForeground(Qt.gray)
        self.highlightning_rules.append((QRegExp("#[^\n]*"),
                                         single_line_comment_format))

        self.multi_line_comment_format = QTextCharFormat()
        self.multi_line_comment_format.setForeground(Qt.red)

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(Qt.darkGreen)
        self.highlightning_rules.append((QRegExp("\".*\""), quotation_format))
        self.highlightning_rules.append((QRegExp("\'.*\'"), quotation_format))

        function_format = QTextCharFormat()
        function_format.setForeground(QColor(245, 254, 220))
        function_format.setFontItalic(True)
        self.highlightning_rules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                                         function_format))

        # TODO Change this to apply for python multi line comments
        self.comment_start_expression = QRegExp("/\\*")
        self.comment_end_expression = QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightning_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)

        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_start_expression.indexIn(text)

        while start_index >= 0:
            end_index = self.comment_end_expression.indexIn(text, start_index)

            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + \
                    self.comment_end_expression.matchedLength()

            self.setFormat(
                start_index,
                comment_length,
                self.multi_line_comment_format)
            start_index = self.comment_start_expression.indexIn(
                text, start_index + comment_length)
