from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.Qt import Qt


class About(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        about_title = QLabel('kettle', self)

        layout = QVBoxLayout()
        layout.addWidget(about_title)
        layout.setAlignment(about_title, Qt.AlignHCenter|Qt.AlignTop)
        central_widget.setLayout(layout)
        self.setWindowTitle('Kettle - About')
