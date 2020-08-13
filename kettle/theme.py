from PyQt5.QtCore import QFile, QTextStream


class Theme:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.theme_name = ''
        self.theme_location = ''

        self.themes = {}
        self.active_theme = ''

    def add(self, theme_name, theme_location):
        self.theme_name = theme_name
        self.theme_location = theme_location
        self.themes[theme_name] = {'location': theme_location}

    def get_all(self):
        return self.themes.keys()

    def set(self, name):
        self.active_theme = name
        self.config.update_config('General', 'theme', name)
        apply_style = ""
        if not name:
            style = QFile(self.get_active()['location'])
            style.open(QFile.ReadOnly | QFile.Text)
            apply_style = QTextStream(style).readAll()
        self.app.setStyleSheet(apply_style)

    def get_active(self):
        return self.themes[self.active_theme]

