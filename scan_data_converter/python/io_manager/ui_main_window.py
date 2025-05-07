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
        self.ui.widget_dict["date_combo_box"].currentTextChanged.connect(
            self.date_link_scan_path
        )

    def update_path_line_edit(self, path: Path):
        self.ui.widget_dict["path_line_edit"].clear()
        self.ui.widget_dict["path_line_edit"].setText(str(path))

    def load_project_list(self):
        """Path Manager에서 Project List 받기"""
        self.ui.widget_dict["project_combo_box"].clear()
        self.ui.widget_dict["project_combo_box"].addItem("Select Project")
        project_list = self.path_mgr.get_project_list()
        self.ui.widget_dict["project_combo_box"].addItems(project_list)

    def load_scan_date_list(self):
        """Path Manager에서 Scan Date List 받기"""
        self.ui.widget_dict["date_combo_box"].clear()
        self.ui.widget_dict["date_combo_box"].addItem("Select Date")
        scan_date_list = self.path_mgr.get_scan_date_list()
        self.ui.widget_dict["date_combo_box"].addItems(scan_date_list)

    def project_link_scan_path(self, item: str):
        """Project 선택 후 path_line_edit에 자동 경로 세팅"""
        if item == "Select Project":
            self.update_path_line_edit(Path(""))  # 빈 경로로 초기화
            self.ui.widget_dict["date_combo_box"].clear()
            self.ui.widget_dict["date_combo_box"].addItem("Select Date")
            return

        # 실제 프로젝트 선택 시
        scan_path = self.path_mgr.project_to_path(item, "scan")
        self.update_path_line_edit(scan_path)

        self.load_scan_date_list()  # Project 선택 후 Scan Date List 출력

    def date_link_scan_path(self, item: str):
        """
        이미 path_line_edit에 날짜가 포함되어 있다면 중복 방지
        """
        if item == "Select Date":
            self.update_path_line_edit(self.path_mgr.scan_path or Path(""))
            return

        current_path = Path(self.ui.widget_dict["path_line_edit"].text())
        base_path = self.path_mgr.scan_path or current_path

        # 중복 날짜 방지: 이미 마지막 경로가 날짜이면 제거
        if current_path.name == item:
            current_path = current_path.parent

        new_path = base_path / item
        self.update_path_line_edit(new_path)

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

    def load_metadata(self):
        # TODO: 구현 예정
        pass
