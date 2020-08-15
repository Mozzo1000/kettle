import configparser
import os


class Config:
    def __init__(self, config_path, config_name):
        self.config_path = config_path
        self.config_name = config_name
        self.config = configparser.ConfigParser()
        self.config.read(config_path + config_name)

        if not os.path.exists(config_path):
            os.makedirs(config_path)
        if not os.path.exists(config_path + config_name):

            self.config.add_section('General')
            self.config.add_section('view')
            self.config.add_section('editor')

            self.config.set('General', 'font', 'Monoid')
            self.config.set('General', 'show_hidden_items', 'False')
            self.config.set('General', 'last_opened_project', '')
            self.config.set('General', 'theme', 'dark')

            self.config.set('view', 'view_statusbar', 'True')
            self.config.set('view', 'view_projectview', 'True')

            self.config.set('editor', 'highlight_line', 'True')

            with open(config_path + config_name, 'w') as config_file:
                self.config.write(config_file)

    def get_setting(self, section, setting, fallback=None):
        return self.config.get(section, setting, fallback=fallback)

    def update_config(self, section, setting, value):
        self.config.set(section, setting, value)
        with open(self.config_path + self.config_name, 'w') as config_file:
            self.config.write(config_file)