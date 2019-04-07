from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QCheckBox


class Settings(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def save_settings(self):
        print("Save button clicked")

    def init_ui(self):
        self.resize(200, 200)
        show_statusbar = QCheckBox("Show statusbar", self)
        show_statusbar.setChecked(True)
        save_btn = QPushButton("Save", self)
        save_btn.move(0, 100)
        save_btn.setToolTip("Save settings")
        save_btn.clicked.connect(self.save_settings)
