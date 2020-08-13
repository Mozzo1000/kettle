import os
from utils import str2bool
from config import Config
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QCheckBox, QFontDialog, QMessageBox, QComboBox

config = Config(os.path.expanduser('~/.kettle/'), 'config.ini')


class Settings(QMainWindow):
    def __init__(self, parent, themes):
        super().__init__(parent)
        self.themes = themes
        self.init_ui()

    def save_settings(self):

        if self.show_statusbar.isChecked():
            config.update_config('view', 'view_statusbar', 'True')
        else:
            config.update_config('view', 'view_statusbar', 'False')
        self.close()

        QMessageBox.question(self, 'Info', 'Please restart the application for changes to take affect.',
                             QMessageBox.Close)

    def open_fonts(self):
        font, ok = QFontDialog.getFont()
        if ok:
            print(font.toString().split(',')[0])
            config.update_config('General', 'font', font.toString().split(',')[0])
            QMessageBox.question(self, 'Info', 'Please restart the application for changes to take affect.', QMessageBox.Close)

    def change_theme(self):
        self.themes.set(self.theme_selector.currentText())
        config.update_config('General', 'theme', self.theme_selector.currentText())
        print('Theme selected: ' + self.theme_selector.currentText())

    def init_ui(self):
        self.resize(200, 200)
        self.show_statusbar = QCheckBox("Show statusbar", self)

        if str2bool(config.get_setting('view', 'view_statusbar')):
            self.show_statusbar.setChecked(True)
        theme_label = QLabel("Theme:", self)
        theme_label.move(0, 50)
        self.theme_selector = QComboBox(self)
        self.theme_selector.move(50, 50)
        self.theme_selector.addItems(self.themes.get_all())
        self.theme_selector.setCurrentText(config.get_setting('General', 'theme'))
        self.theme_selector.currentTextChanged.connect(self.change_theme)


        save_btn = QPushButton("Save", self)
        save_btn.move(0, 100)
        save_btn.setToolTip("Save settings")
        save_btn.clicked.connect(self.save_settings)

        font_btn = QPushButton("Set font", self)
        font_btn.move(0, 150)
        font_btn.setToolTip("Set font")
        font_btn.clicked.connect(self.open_fonts)
