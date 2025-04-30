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

        self.ui.widget_dict["project_combo_box"].currentTextChanged.connect(
            self.project_link_date_list
        )
        self.ui.widget_dict["date_combo_box"].currentTextChanged.connect(
            self.update_scan_path
        )

    def get_scan_path(self, project):
        return f"/show/{project}/product/scan"

    def update_scan_path(self):
        """Project + Date 선택 후 path_line_edit에 자동 경로 세팅"""
        project = self.ui.widget_dict["project_combo_box"].currentText()
        date = self.ui.widget_dict["date_combo_box"].currentText()
        if project and date:
            full_path = os.path.join(self.get_scan_path(project), date)
            self.ui.widget_dict["path_line_edit"].setText(full_path)
            print(f"[INFO] 경로 설정: {full_path}")

    def select_scan_dir(self):
        """
        폴더만 선택가능
        Select Scan Directory
        Scan Data : EXR image sequence, MOV
        """
        # 폴더만 선택할 수 있게 제한
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        scan_dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            self.ui.widget_dict["path_line_edit"].text(),
            options=options,
        )
        if scan_dir_path:
            self.ui.widget_dict["path_line_edit"].setText(scan_dir_path)

    def get_project_list(self):
        base_path = "/show"
        return [
            f
            for f in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, f))
        ]

    def load_project_list(self):
        project_list = self.get_project_list()
        self.ui.widget_dict["project_combo_box"].clear()
        self.ui.widget_dict["project_combo_box"].addItems(project_list)

    def project_link_date_list(self):
        """프로젝트 선택 시 날짜 목록 갱신"""
        project = self.ui.widget_dict["project_combo_box"].currentText()
        if not project:
            return
        scan_base = self.get_scan_path(project)
        if os.path.exists(scan_base):
            scan_dates = [
                f
                for f in os.listdir(scan_base)
                if os.path.isdir(os.path.join(scan_base, f))
            ]
            self.ui.widget_dict["date_combo_box"].clear()
            self.ui.widget_dict["date_combo_box"].addItems(scan_dates)

    def load_metadata(self):
        # TODO: 구현 예정
        pass
