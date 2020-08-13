
class Theme:
    def __init__(self, config):
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

    def get_active(self):
        return self.themes[self.active_theme]

