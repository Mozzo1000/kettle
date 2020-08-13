from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


class HTMLPreview(QDockWidget):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle('HTML Preview')

        web = QWebEngineView()
        web.load(QUrl.fromLocalFile(url))

        self.setWidget(web)
