import os
from utils import str2bool
from config import Config
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QCheckBox, QFontDialog, QMessageBox

config = Config(os.path.expanduser('~/.kettle/'), 'config.ini')


class Settings(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def save_settings(self):

        if self.show_statusbar.isChecked():
            config.update_config('General', 'view_statusbar', 'True')
        else:
            config.update_config('General', 'view_statusbar', 'False')
        self.close()

        QMessageBox.question(self, 'Info', 'Please restart the application for changes to take affect.',
                             QMessageBox.Close)

    def open_fonts(self):
        font, ok = QFontDialog.getFont()
        if ok:
            print(font.toString().split(',')[0])
            config.update_config('General', 'font', font.toString().split(',')[0])
            QMessageBox.question(self, 'Info', 'Please restart the application for changes to take affect.', QMessageBox.Close)

    def init_ui(self):
        self.resize(200, 200)
        self.show_statusbar = QCheckBox("Show statusbar", self)

        if str2bool(config.get_setting('General', 'view_statusbar')):
            self.show_statusbar.setChecked(True)
        save_btn = QPushButton("Save", self)
        save_btn.move(0, 100)
        save_btn.setToolTip("Save settings")
        save_btn.clicked.connect(self.save_settings)

        font_btn = QPushButton("Set font", self)
        font_btn.move(0, 150)
        font_btn.setToolTip("Set font")
        font_btn.clicked.connect(self.open_fonts)
