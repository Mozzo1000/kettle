import os
from utils import str2bool
from config import Config
from PyQt5.QtWidgets import QMainWindow, QPushButton, QCheckBox, QFontDialog, QMessageBox, \
    QComboBox, QListWidget, QHBoxLayout, QWidget, QStackedWidget, QFormLayout

config = Config(os.path.expanduser('~/.kettle/'), 'config.ini')


class Settings(QMainWindow):
    def __init__(self, parent, themes):
        super().__init__(parent)
        self.themes = themes
        self.resize(200, 200)
        self.main_widget = QWidget(self)
        self.layout = QHBoxLayout(self)

        self.stack_widget = QStackedWidget(self)

        self.general_widget = QWidget(self)
        self.general_ui()

        self.view_widget = QWidget(self)
        self.view_ui()

        self.editor_widget = QWidget(self)
        self.editor_ui()

        self.stack_widget.addWidget(self.general_widget)
        self.stack_widget.addWidget(self.view_widget)
        self.stack_widget.addWidget(self.editor_widget)

        settings_list = QListWidget(self)
        settings_list.currentRowChanged.connect(self.switch_display)
        settings_list.insertItem(0, 'General')
        settings_list.insertItem(1, 'View')
        settings_list.insertItem(2, 'Editor')

        save_btn = QPushButton("Save", self)
        save_btn.setToolTip("Save settings")
        save_btn.clicked.connect(self.save_settings)

        self.layout.addWidget(settings_list)
        self.layout.addWidget(self.stack_widget)
        self.layout.addWidget(save_btn)
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def general_ui(self):
        layout = QFormLayout()
        font_btn = QPushButton("Change font", self)
        font_btn.setToolTip("Change font")
        font_btn.clicked.connect(self.open_fonts)

        self.theme_selector = QComboBox(self)
        self.theme_selector.addItems(self.themes.get_all())
        self.theme_selector.setCurrentText(config.get_setting('General', 'theme'))
        self.theme_selector.currentTextChanged.connect(self.change_theme)

        self.show_hidden_items = QCheckBox("Show hidden items", self)
        if str2bool(config.get_setting('General', 'show_hidden_items')):
            self.show_hidden_items.setChecked(True)

        layout.addRow(f'Font: {config.get_setting("General", "font")}', font_btn)
        layout.addRow("Theme", self.theme_selector)
        layout.addRow(self.show_hidden_items)
        self.general_widget.setLayout(layout)

    def view_ui(self):
        layout = QFormLayout()

        self.show_statusbar = QCheckBox("Show statusbar", self)
        if str2bool(config.get_setting('view', 'view_statusbar')):
            self.show_statusbar.setChecked(True)

        self.show_projectview = QCheckBox("Show project view", self)
        if str2bool(config.get_setting('view', 'view_projectview')):
            self.show_projectview.setChecked(True)

        layout.addRow(self.show_statusbar)
        layout.addRow(self.show_projectview)

        self.view_widget.setLayout(layout)

    def editor_ui(self):
        layout = QFormLayout()
        self.highlight_line = QCheckBox("Highlight line", self)
        if str2bool(config.get_setting('editor', 'highlight_line')):
            self.highlight_line.setChecked(True)

        layout.addRow(self.highlight_line)
        self.editor_widget.setLayout(layout)

    def switch_display(self, i):
        self.stack_widget.setCurrentIndex(i)

    def save_settings(self):

        if self.show_statusbar.isChecked():
            config.update_config('view', 'view_statusbar', 'True')
        else:
            config.update_config('view', 'view_statusbar', 'False')
        if self.show_projectview.isChecked():
            config.update_config('view', 'view_projectview', 'True')
        else:
            config.update_config('view', 'view_projectview', 'False')

        if self.show_hidden_items.isChecked():
            config.update_config('General', 'show_hidden_items', 'True')
        else:
            config.update_config('General', 'show_hidden_items', 'False')

        if self.highlight_line.isChecked():
            config.update_config('editor', 'highlight_line', 'True')
        else:
            config.update_config('editor', 'highlight_line', 'False')
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
