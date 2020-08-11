import sys
import os
import subprocess
import style_rc
import utils
import imghdr
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QTextEdit, \
    QFileDialog, QLabel, QWidget, QHBoxLayout, QTreeWidget, QSizePolicy, QSplitter, \
    QLayout, QTreeWidgetItem, QMessageBox, QTabWidget
from PyQt5.QtGui import QIcon, QFont, QDesktopServices, QFontDatabase, QPixmap
from PyQt5.QtCore import QFile, QTextStream, QUrl
from syntax import SyntaxHighlighter
from ui.settings import Settings
from ui.about import About
from config import Config

basedir = os.path.abspath(os.path.dirname(__file__))
config = Config(os.path.expanduser('~/.kettle/'), 'config.ini')


class Kettle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.filename = "untitled"

    def save_file(self):
        name = self.filename[0]
        if not self.filename or self.filename == "untitled":
            name = QFileDialog.getSaveFileName(self, 'Save File')[0]

        file = open(name, 'wt')
        save_text = self.current_editor.toPlainText()
        file.write(save_text)
        file.close()

    def save_file_as(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')[0]
        file = open(name, 'wt')
        save_text = self.current_editor.toPlainText()
        file.write(save_text)
        file.close()

    def open_file(self):
        name = QFileDialog.getOpenFileName(self, 'Open File')
        self.filename = name
        file_image_type = imghdr.what(name[0])
        if file_image_type is not None:
            self.open_image(self.filename[0])
        else:
            file = open(name[0], 'r', encoding='utf-8', errors='ignore')

            with file:
                self.new_document(title=os.path.basename(self.filename[0]))
                self.current_editor.setText(file.read())

    def open_image(self, filename):
        label = QLabel(self)
        pixmap = QPixmap(filename)
        label.setPixmap(pixmap)
        self.tab_widget.addTab(label, filename)
        self.tab_widget.setCurrentWidget(label)

    def run(self):
        subprocess.Popen('python ' + self.filename[0])

    def view_status(self, state):
        if state:
            self.statusbar.show()
            config.update_config('General', 'view_statusbar', 'True')
        else:
            self.statusbar.hide()
            config.update_config('General', 'view_statusbar', 'False')

    def status_line_position(self):
        line = self.current_editor.textCursor().blockNumber()
        column = self.current_editor.textCursor().columnNumber()
        line_column = ("Line: " + str(line) + " | " + "Column: " + str(column))
        self.statusbar.showMessage(line_column)

    def load_project_structure(self, startpath, tree):
        for element in os.listdir(startpath):
            path_info = startpath + "/" + element
            parent_itm = QTreeWidgetItem(tree, [os.path.basename(element), os.path.join(startpath, element)])
            if os.path.isdir(path_info):
                self.load_project_structure(path_info, parent_itm)
                parent_itm.setIcon(0, QIcon(os.path.join(basedir, '../assets/folder.png')))
            else:
                parent_itm.setIcon(0, QIcon(os.path.join(basedir, '../assets/file.png')))
            if not utils.str2bool(config.get_setting('General', 'show_hidden_items', 'False')):
                if element.startswith('.'):
                    parent_itm.setHidden(True)

    def tree_clicked(self):
        if os.path.isdir(self.treeView.selectedItems()[0].text(1)):
            print("This is not a file, is a directory.")
        else:
            try:
                file_image_type = imghdr.what(self.treeView.selectedItems()[0].text(1))
                if file_image_type is not None:
                    self.open_image(self.treeView.selectedItems()[0].text(1))
                else:
                    file = open(self.treeView.selectedItems()[0].text(1), 'r', encoding='utf-8', errors='ignore')

                    with file:
                        text = file.read()
                        self.new_document(title=os.path.basename(self.treeView.selectedItems()[0].text(1)))
                        self.current_editor.setText(text)
            except FileNotFoundError as error:
                print("No such file found : " + str(error))
                QMessageBox.question(self, 'Error', 'Error occured : ' + str(error), QMessageBox.Close)

    def open_prof(self):
        self.proj_folder = str(
            QFileDialog.getExistingDirectory(
                self, 'Select Directory'))
        self.treeView.clear()
        self.load_project_structure(self.proj_folder, self.treeView)
        config.update_config('General', 'last_opened_project', self.proj_folder)

    def open_settings(self):
        settings = Settings(self)
        settings.show()

    def open_github_link(self):
        url = QUrl('https://github.com/Mozzo1000/kettle/')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open URL', 'Could not open url')

    def open_about(self):
        about = About(self)
        about.show()

    def create_editor(self):
        text_editor = QTextEdit()
        font = QFont()
        print(config.get_setting('General', 'font'))
        font.setFamily(config.get_setting('General', 'font'))
        font.setPointSize(11)
        text_editor.setFont(font)
        text_editor.setTabStopWidth(30)
        self.highlighter = SyntaxHighlighter(text_editor.document())
        return text_editor

    def remove_editor(self, index):
        self.tab_widget.removeTab(index)
        if index < len(self.editors):
            del self.editors[index]

    def change_text_editor(self, index):
        if index < len(self.editors):
            self.current_editor = self.editors[index]

    def new_document(self, checked=False, title="Untitled"):
        self.current_editor = self.create_editor()
        self.current_editor.cursorPositionChanged.connect(self.status_line_position)
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, str(title) + " - " + str(len(self.editors)))
        self.tab_widget.setCurrentWidget(self.current_editor)

    def init_ui(self):
        self.resize(800, 600)
        self.setWindowTitle('Kettle')

        self.current_editor = self.create_editor()
        self.editors = []

        self.central_widget = QWidget(self)
        QFontDatabase.addApplicationFont('../assets/font/Monoid-Regular.ttf')

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.statusbar = self.statusBar()

        self.horizontal_layoutW = QWidget(self.central_widget)
        self.splitter = QSplitter(self.central_widget)

        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.currentChanged.connect(self.change_text_editor)
        self.tab_widget.tabCloseRequested.connect(self.remove_editor)
        self.new_document()

        print(self.sizeHint())
        self.horizontal_layout = QHBoxLayout(self.central_widget)
        self.horizontal_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.treeView = QTreeWidget(self.central_widget)
        self.treeView.setHeaderLabel('Project View')
        self.treeView.itemDoubleClicked.connect(self.tree_clicked)
        self.splitter.addWidget(self.treeView)
        self.splitter.addWidget(self.tab_widget)

        self.horizontal_layout.addWidget(self.splitter)
        self.setCentralWidget(self.central_widget)
        label = QLabel("wafawfwa")
        label2 = QLabel("testest")
        self.statusbar.addPermanentWidget(label)
        self.statusbar.addWidget(label2)
        self.splitter.setSizes([5, 300])

        if not utils.str2bool(config.get_setting('General', 'view_statusbar')):
            self.statusbar.hide()

        if config.get_setting('General', 'last_opened_project'):
            self.load_project_structure(config.get_setting('General', 'last_opened_project'), self.treeView)

        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_document)
        new_action.setShortcut('Ctrl+N')

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        save_action.setShortcut('Ctrl+S')

        save_as_action = QAction("Save as..", self)
        save_as_action.triggered.connect(self.save_file_as)
        save_as_action.setShortcut('Ctrl+Alt+S')

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        open_action.setShortcut('Ctrl+O')

        open_proj_action = QAction('Open Project', self)
        open_proj_action.triggered.connect(self.open_prof)

        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.open_settings)

        undo_action = QAction('Undo', self)
        undo_action.triggered.connect(self.current_editor.undo)
        undo_action.setShortcut('Ctrl+Z')

        redo_action = QAction('Redo', self)
        redo_action.triggered.connect(self.current_editor.redo)
        redo_action.setShortcut('Ctrl+Y')

        cut_action = QAction('Cut', self)
        cut_action.triggered.connect(self.current_editor.cut)
        cut_action.setShortcut('Ctrl+X')

        copy_action = QAction('Copy', self)
        copy_action.triggered.connect(self.current_editor.copy)
        copy_action.setShortcut('Ctrl+C')

        paste_action = QAction('Paste', self)
        paste_action.triggered.connect(self.current_editor.paste)
        paste_action.setShortcut('Ctrl+V')

        select_all_action = QAction('Select all', self)
        select_all_action.triggered.connect(self.current_editor.selectAll)
        select_all_action.setShortcut('Ctrl+A')

        run_action = QAction('Run', self)
        run_action.triggered.connect(self.run)
        run_action.setShortcut('Ctrl+SPACE')

        view_status_action = QAction('View statusbar', self, checkable=True)
        view_status_action.setChecked(utils.str2bool(config.get_setting('General', 'view_statusbar')))
        view_status_action.triggered.connect(self.view_status)

        github_link_action = QAction('Github', self)
        github_link_action.triggered.connect(self.open_github_link)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.open_about)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        edit_menu = menubar.addMenu('&Edit')
        run_menu = menubar.addMenu('&Run')
        view_menu = menubar.addMenu('&View')
        help_menu = menubar.addMenu('&Help')

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(open_proj_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(settings_action)
        file_menu.addAction(exit_action)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        edit_menu.addAction(select_all_action)

        run_menu.addAction(run_action)

        view_menu.addAction(view_status_action)

        help_menu.addAction(github_link_action)
        help_menu.addAction(about_action)

        self.showMaximized()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('../assets/icon.png'))
    if utils.str2bool(config.get_setting('General', 'use_dark_theme', 'True')):
        style = QFile(os.path.join(basedir, '../assets/style/style.qss'))
        style.open(QFile.ReadOnly | QFile.Text)
        app.setStyleSheet(QTextStream(style).readAll())
    print(os.path.dirname(os.path.abspath(__file__)))

    kettle = Kettle()
    sys.exit(app.exec_())
