import os
from PyQt5.QtWidgets import QStatusBar
from utils import str2bool
from config import Config

config = Config(os.path.expanduser('~/.kettle/'), 'config.ini')


class Statusbar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        if not str2bool(config.get_setting('view', 'view_statusbar')):
            self.hide()

    def view_status(self, state):
        if state:
            self.show()
            config.update_config('view', 'view_statusbar', 'True')
        else:
            self.hide()
            config.update_config('view', 'view_statusbar', 'False')

    def status_line_position(self):
        line = self.parent.current_editor.textCursor().blockNumber()
        column = self.parent.current_editor.textCursor().columnNumber()
        line_column = ("Line: " + str(line) + " | " + "Column: " + str(column))
        self.showMessage(line_column)
