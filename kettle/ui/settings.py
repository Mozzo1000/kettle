import config
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QCheckBox, QFontDialog, QMessageBox


class Settings(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def save_settings(self):
        print("Save button clicked")

    def open_fonts(self):
        font, ok = QFontDialog.getFont()
        if ok:
            print(font.toString().split(',')[0])
            config.update_config('General', 'font', font.toString().split(',')[0])
            QMessageBox.question(self, 'Info', 'Please restart the application for changes to take affect.', QMessageBox.Close)


    def init_ui(self):
        self.resize(200, 200)
        show_statusbar = QCheckBox("Show statusbar", self)
        show_statusbar.setChecked(True)
        save_btn = QPushButton("Save", self)
        save_btn.move(0, 100)
        save_btn.setToolTip("Save settings")
        save_btn.clicked.connect(self.save_settings)

        font_btn = QPushButton("Set font", self)
        font_btn.move(0, 150)
        font_btn.setToolTip("Set font")
        font_btn.clicked.connect(self.open_fonts)
