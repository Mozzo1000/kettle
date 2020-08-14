from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


class HTMLPreview(QDockWidget):
    def __init__(self, url, text):
        super().__init__()
        self.setWindowTitle('HTML Preview')
        self.url = url
        self.text = text

        text.textChanged.connect(self.on_update)

        self.web = QWebEngineView()
        self.web.setHtml(text.toPlainText(), baseUrl=QUrl.fromLocalFile(url))
        self.web.loadFinished.connect(self.on_load_finished)

        self.setWidget(self.web)

    def on_load_finished(self):
        self.setWindowTitle(f'HTML Preview - {self.web.title()}')

    def on_update(self):
        self.web.setHtml(self.text.toPlainText(), baseUrl=QUrl.fromLocalFile(self.url))
