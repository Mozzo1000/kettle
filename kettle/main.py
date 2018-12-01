import sys
import os
import subprocess
import qdarkstyle
import config
import utils
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QTextEdit, \
    QFileDialog, QLabel, QWidget, QHBoxLayout, QTreeWidget, QSizePolicy, QSplitter, \
    QLayout, QTreeWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from syntax import SyntaxHighlighter


class Kettle(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.filename = "untitled"

    def text_window(self):
        self.text = QTextEdit(self.central_widget)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.text.setFont(font)
        self.text.setTabStopWidth(30)
        self.highlighter = SyntaxHighlighter(self.text.document())

    def create_new(self):
        print("Create new file")
        self.text.clear()
        self.filename = "untitled"

    def save_file(self):
        name = self.filename[0]
        if not self.filename or self.filename == "untitled":
            name = QFileDialog.getSaveFileName(self, 'Save File')[0]

        file = open(name, 'wt')
        save_text = self.text.toPlainText()
        file.write(save_text)
        file.close()

    def save_file_as(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')[0]
        file = open(name, 'wt')
        save_text = self.text.toPlainText()
        file.write(save_text)
        file.close()

    def open_file(self):
        name = QFileDialog.getOpenFileName(self, 'Open File')
        self.filename = name
        file = open(name[0], 'r')
        self.text.clear()
        with file:
            text = file.read()
            self.text.setText(text)

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
        line = self.text.textCursor().blockNumber()
        column = self.text.textCursor().columnNumber()
        line_column = ("Line: " + str(line) + " | " + "Column: " + str(column))
        self.statusbar.showMessage(line_column)

    def load_project_structure(self, startpath, tree):
        for element in os.listdir(startpath):
            path_info = startpath + "/" + element
            parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
            if os.path.isdir(path_info):
                self.load_project_structure(path_info, parent_itm)
                parent_itm.setIcon(0, QIcon('../assets/folder.png'))
            else:
                parent_itm.setIcon(0, QIcon('../assets/file.png'))

    def tree_clicked(self):
        print(self.treeView.selectedItems()[0].text(0))
        print(self.proj_folder)
        try:
            file = open(utils.find_file_location(self.treeView.selectedItems()[0].text(0), self.proj_folder), 'r')

            self.text.clear()
            with file:
                text = file.read()
                self.text.setText(text)
        except IsADirectoryError as error:
            print("This is not a file, is a directory : " + str(error))
        except FileNotFoundError as error:
            print("No such file found : " + str(error))
            QMessageBox.question(self, 'Error', 'Error occured : ' + str(error), QMessageBox.Close)

    def open_prof(self):
        self.proj_folder = str(
            QFileDialog.getExistingDirectory(
                self, 'Select Directory'))
        self.load_project_structure(self.proj_folder, self.treeView)

    def init_ui(self):
        self.resize(800, 600)
        self.setWindowTitle('Kettle')

        self.central_widget = QWidget(self)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.statusbar = self.statusBar()

        self.horizontal_layoutW = QWidget(self.central_widget)
        self.splitter = QSplitter(self.central_widget)
        self.text_window()

        print(self.sizeHint())
        self.horizontal_layout = QHBoxLayout(self.central_widget)
        self.horizontal_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.treeView = QTreeWidget(self.central_widget)
        self.treeView.itemDoubleClicked.connect(self.tree_clicked)
        self.splitter.addWidget(self.treeView)
        self.splitter.addWidget(self.text)

        self.horizontal_layout.addWidget(self.splitter)
        self.setCentralWidget(self.central_widget)
        label = QLabel("wafawfwa")
        label2 = QLabel("testest")
        self.statusbar.addPermanentWidget(label)
        self.statusbar.addWidget(label2)
        self.text.cursorPositionChanged.connect(self.status_line_position)
        self.splitter.setSizes([5, 300])

        if not utils.str2bool(config.get_setting('General', 'view_statusbar')):
            self.statusbar.hide()

        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        new_action = QAction('New', self)
        new_action.triggered.connect(self.create_new)
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

        undo_action = QAction('Undo', self)
        undo_action.triggered.connect(self.text.undo)
        undo_action.setShortcut('Ctrl+Z')

        redo_action = QAction('Redo', self)
        redo_action.triggered.connect(self.text.redo)
        redo_action.setShortcut('Ctrl+Y')

        cut_action = QAction('Cut', self)
        cut_action.triggered.connect(self.text.cut)
        cut_action.setShortcut('Ctrl+X')

        copy_action = QAction('Copy', self)
        copy_action.triggered.connect(self.text.copy)
        copy_action.setShortcut('Ctrl+C')

        paste_action = QAction('Paste', self)
        paste_action.triggered.connect(self.text.paste)
        paste_action.setShortcut('Ctrl+V')

        select_all_action = QAction('Select all', self)
        select_all_action.triggered.connect(self.text.selectAll)
        select_all_action.setShortcut('Ctrl+A')

        run_action = QAction('Run', self)
        run_action.triggered.connect(self.run)
        run_action.setShortcut('Ctrl+SPACE')

        view_status_action = QAction('View statusbar', self, checkable=True)
        view_status_action.setChecked(utils.str2bool(config.get_setting('General', 'view_statusbar')))
        view_status_action.triggered.connect(self.view_status)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        edit_menu = menubar.addMenu('&Edit')
        run_menu = menubar.addMenu('&Run')
        view_menu = menubar.addMenu('&View')

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(open_proj_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(exit_action)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        edit_menu.addAction(select_all_action)

        run_menu.addAction(run_action)

        view_menu.addAction(view_status_action)

        self.showMaximized()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('../assets/icon.png'))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    print(os.path.dirname(os.path.abspath(__file__)))

    config.create_config()

    kettle = Kettle()
    sys.exit(app.exec_())
