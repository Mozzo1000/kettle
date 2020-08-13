from PyQt5.QtCore import QFile, QTextStream


class Theme:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.theme_name = ''
        self.theme_location = ''

        self.themes = {}
        self.active_theme = ''

    def add(self, theme_name, theme_location, highlight_color, icon_set):
        self.theme_name = theme_name
        self.theme_location = theme_location
        self.themes[theme_name] = {'location': theme_location, 'highlight_color': highlight_color,
                                   'icon_set': icon_set}

    def get_all(self):
        return self.themes.keys()

    def set(self, name):
        self.active_theme = name
        self.config.update_config('General', 'theme', name)
        style = QFile(self.get_active()['location'])
        style.open(QFile.ReadOnly | QFile.Text)
        self.app.setStyleSheet(QTextStream(style).readAll())

    def get_icon(self, icon):
        return self.get_active()['icon_set'] + icon

    def get_active(self):
        return self.themes[self.active_theme]

