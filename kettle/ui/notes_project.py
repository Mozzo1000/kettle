import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLineEdit, QLabel, QFileDialog, QVBoxLayout, \
    QMessageBox
from config import Config

config = Config(os.path.expanduser('~/.kettle/'), 'config.ini')


class CreateNotesProject(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Create new notes project')
        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self)

        self.folder_selected = False

        project_name_label = QLabel(self)
        project_name_label.setText('Notes project name: ')
        self.project_name = QLineEdit(self)
        self.project_name.textChanged.connect(self.on_text_changed)

        browse_folder_button = QPushButton(self)
        browse_folder_button.setText('Browse folder')
        browse_folder_button.clicked.connect(self.open_browse_dialog)

        self.create_button = QPushButton(self)
        self.create_button.setText('Create')
        self.create_button.setDisabled(True)
        self.create_button.clicked.connect(self.create_project)

        self.browse_label = QLabel(self)

        self.layout.addWidget(project_name_label)
        self.layout.addWidget(self.project_name)
        self.layout.addWidget(browse_folder_button)
        self.layout.addWidget(self.browse_label)
        self.layout.addWidget(self.create_button)
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)


    def on_text_changed(self):
        print("ON TEXT CHANGED")
        if self.project_name.text() and self.folder_selected:
            self.create_button.setEnabled(True)
        if not self.project_name.text():
            self.create_button.setDisabled(True)

    def open_browse_dialog(self):
        self.browse_folder = QFileDialog(self)
        self.browse_folder.setFileMode(QFileDialog.Directory)
        self.browse_folder.setOption(QFileDialog.ShowDirsOnly)
        if self.browse_folder.exec_():
            self.browse_label.setText(f"Your new notes project will be placed in\n'{self.browse_folder.selectedFiles()[0]}'")
            self.folder_selected = True
            if self.project_name.text():
                self.create_button.setEnabled(True)
            print(self.browse_folder.selectedFiles()[0])

    def create_project(self):
        print('create project folder..')
        whole_project_path = self.browse_folder.selectedFiles()[0] + '/' + self.project_name.text()
        if not os.path.exists(whole_project_path):
            os.makedirs(whole_project_path)
            os.makedirs(whole_project_path + '/' + '.notes')
        else:
            QMessageBox.question(self, 'Info',
                                 f'The folder selected already has project with name {self.project_name.text()}, '
                                 f'please select another folder.',
                                 QMessageBox.Close)
        self.close()
        self.parent.treeView.clear()
        self.parent.load_project_structure(whole_project_path, self.parent.treeView)
        self.parent.treeView.setHeaderHidden(False)
        self.parent.treeView.setHeaderLabel(os.path.basename(os.path.normpath(whole_project_path)))
        config.update_config('General', 'last_opened_project', whole_project_path)
