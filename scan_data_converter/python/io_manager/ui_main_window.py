from PySide6.QtWidgets import QMainWindow, QFileDialog
from .ui_builder import UiBuilder
from .path_manager import PathManager

import os
from pathlib import Path


class IOManagerWindow(QMainWindow):
    """Io Manager UI Event 관리 Class"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("I/O Manager")
        self.setMinimumSize(1200, 800)

        self.ui = UiBuilder()
        self.setCentralWidget(self.ui)

        show_root = "/show"
        self.path_mgr = PathManager(show_root)

        self.setup_ui()

        self.init_signals()
        self.load_project_list()

    def setup_ui(self):
        """UI 시작시 Setting"""
        # Line Edit에 기본 경로 세팅 (예: /show)
        self.ui.widget_dict["path_line_edit"].setText(str(self.path_mgr.show_root))

    def init_signals(self):
        self.ui.widget_dict["select_btn"].clicked.connect(self.select_scan_dir)
        self.ui.widget_dict["load_btn"].clicked.connect(self.load_metadata)
        self.ui.widget_dict["project_combo_box"].currentTextChanged.connect(
            self.project_link_scan_path
        )

        # self.ui.widget_dict["date_combo_box"].currentTextChanged.connect(
        #     self.update_scan_path
        # )

    def load_project_list(self):
        project_list = self.path_mgr.get_project_list()

        self.ui.widget_dict["project_combo_box"].clear()
        self.ui.widget_dict["project_combo_box"].addItems(project_list)

    def project_link_scan_path(self):
        """
        ### 수정중 ###
        Project 선택 후 path_line_edit에 자동 경로 세팅
        """
        project = self.ui.widget_dict["project_combo_box"].currentText()
        scan_path = self.path_mgr.project_to_path(project, "scan")

        self.update_path_line_edit(scan_path)

    def update_path_line_edit(self, path: Path):
        self.ui.widget_dict["path_line_edit"].clear()
        self.ui.widget_dict["path_line_edit"].setText(str(path))

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

    def analyze_scan_ext(self):
        """
        Convert하기 위한 Scan Folder안의 확장자 식별 (exr, MOV)
        mov 인경우 : exr로 변환하는 경우가 있다. [Nuke Convert]
        """
        pass

    # def project_link_date_list(self):
    #     """프로젝트 선택 시 날짜 목록 갱신"""
    #     project = self.ui.widget_dict["project_combo_box"].currentText()
    #     if not project:
    #         return

    #     scan_path = self.path_mgr.project_to_path(project, "scan")

    # if os.path.exists(scan_path):
    #     scan_dates = [
    #         date_f
    #         for date_f in os.listdir(scan_path)
    #         if os.path.isdir(os.path.join(scan_path, date_f))
    #     ]
    #     self.ui.widget_dict["date_combo_box"].clear()
    #     self.ui.widget_dict["date_combo_box"].addItems(scan_dates)

    def path_link_date_list(self):
        pass
        # date = self.ui.widget_dict["date_combo_box"].currentText()

        # if project and date:
        #     # full_path = os.path.join(self.get_scan_path(project), date)
        #     full_path = scan_path / date  # Path 객체

        #     self.ui.widget_dict["path_line_edit"].setText(str(full_path))
        #     print(f"[INFO] 경로 설정: {full_path}")

    def load_metadata(self):
        # TODO: 구현 예정
        pass
