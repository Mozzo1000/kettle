from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown2


class MarkdownPreview(QDockWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.setWindowTitle('Markdown Preview')

        text.textChanged.connect(self.on_update)

        self.web = QWebEngineView()
        self.web.setHtml(markdown2.markdown(self.text.toPlainText(), extras=['tables']))
        self.setWidget(self.web)

    def on_update(self):
        self.web.page().setHtml(markdown2.markdown(self.text.toPlainText(), extras=['tables']))
