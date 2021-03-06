from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import markdown2


class MarkdownPreview(QDockWidget):
    def __init__(self, file, text):
        super().__init__()
        self.file = file
        self.text = text
        self.setWindowTitle('Markdown Preview')
        self.markdown_extras = ['tables', 'fenced-code-blocks', 'task-list']

        text.textChanged.connect(self.on_update)

        self.text.verticalScrollBar().valueChanged.connect(self.sync_scroll)

        self.web = QWebEngineView()
        self.web.setHtml(markdown2.markdown(self.text.toPlainText(), extras=self.markdown_extras), baseUrl=QUrl.fromLocalFile(file))
        self.web.loadFinished.connect(self.sync_scroll)
        self.setWidget(self.web)

    def sync_scroll(self):
        self.web.page().runJavaScript(f'scrollTo({self.text.horizontalScrollBar().value()}, document.body.scrollHeight * {self.text.verticalScrollBar().value()} / {self.text.verticalScrollBar().maximum()});')

    def on_update(self):
        self.web.page().setHtml(markdown2.markdown(self.text.toPlainText(), extras=self.markdown_extras), baseUrl=QUrl.fromLocalFile(self.file))
