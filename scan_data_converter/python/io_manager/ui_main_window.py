from PySide6.QtWidgets import QMainWindow, QFileDialog
from .ui_builder import UiBuilder


import os


class IOManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("I/O Manager")
        self.setMinimumSize(1200, 800)

        self.ui = UiBuilder()
        self.setCentralWidget(self.ui)

        self.init_signals()
        self.load_project_list()

    def init_signals(self):
        self.ui.widget_dict["select_btn"].clicked.connect(self.select_scan_dir)
        self.ui.widget_dict["load_btn"].clicked.connect(self.load_metadata)
        self.ui.widget_dict["project_combo_box"].currentIndexChanged.connect(
            self.load_metadata
        )

    def select_scan_dir(self):
        scan_dir_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if scan_dir_path:
            self.ui.widget_dict["path_line_edit"].setText(scan_dir_path)

    def get_project_list(self):
        path = "/show"
        project_list = []
        for folder in os.listdir(path): 
            if os.path.isdir(
                os.path.join(path, folder)
            ): 
                project_list.append(folder)
        return project_list

    def load_project_list(self):
        project_list = self.get_project_list()
        self.ui.widget_dict["project_combo_box"].clear()
        self.ui.widget_dict["project_combo_box"].addItems(project_list)

    def load_metadata(self):
        # 실제 메타데이터 로딩 구현 예정
        pass
