from PyQt5.QtWidgets import QDockWidget, QTextEdit


class MarkdownPreview(QDockWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.setWindowTitle('Markdown Preview')

        self.markdown = QTextEdit(self)
        self.markdown.setMarkdown(text.toPlainText())
        text.textChanged.connect(self.on_update)

        self.setWidget(self.markdown)

    def on_update(self):
        self.markdown.setMarkdown(self.text.toPlainText())