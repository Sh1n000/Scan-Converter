from PySide6.QtWidgets import QFileDialog
from pathlib import Path

from .file_manager import FileManager
from folder_generator import DirectoryManager


class IOManagerEventHandler:
    """UI Event 관리 Class"""

    def __init__(self, ui: dict, path_manager):
        self.ui = ui  # UI Widgets Dict <- UI Builder
        self.path_mgr = path_manager

    def setup_signals(self):
        # Click Event
        self.ui["select_btn"].clicked.connect(self.selected_to_convert)
        self.ui["load_btn"].clicked.connect(self.load_metadata)

        # 콤보박스
        self.ui["project_combo_box"].currentTextChanged.connect(self.project_changed)
        self.ui["date_combo_box"].currentTextChanged.connect(self.date_changed)

        # Load Data
        self.load_project_list()

    def update_path_line_edit(self, path: Path):
        self.ui["path_line_edit"].setText(str(path))

    def load_project_list(self):
        self.ui["project_combo_box"].clear()
        self.ui["project_combo_box"].addItem("Select Project")
        project_list = self.path_mgr.get_project_list()
        self.ui["project_combo_box"].addItems(project_list)

    def load_scan_date_list(self):
        """Date List는 Project가 정해지면 Load"""
        self.ui["date_combo_box"].clear()
        self.ui["date_combo_box"].addItem("Select Date")
        scan_date_list = self.path_mgr.get_scan_date_list()
        self.ui["date_combo_box"].addItems(scan_date_list)

    def project_changed(self, item: str):
        if item == "Select Project":
            self.update_path_line_edit(Path(""))
            self.ui["date_combo_box"].clear()
            self.ui["date_combo_box"].addItem("Select Date")
            return

        scan_path = self.path_mgr.project_to_path(item, "scan")
        self.update_path_line_edit(scan_path)
        self.load_scan_date_list()

    def date_changed(self, item: str):
        if item == "Select Date":
            self.update_path_line_edit(self.path_mgr.scan_path or Path(""))
            return

        current_path = Path(self.ui["path_line_edit"].text())
        base_path = self.path_mgr.scan_path or current_path

        if current_path.name == item:
            current_path = current_path.parent

        new_path = base_path / item
        self.update_path_line_edit(new_path)

    def select_dir(self):
        """폴더만 선택가능"""
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly

        scan_dir_path = QFileDialog.getExistingDirectory(
            None,
            "Select Folder",
            self.ui["path_line_edit"].text(),
            options=options,
        )
        if scan_dir_path:
            self.ui["path_line_edit"].setText(scan_dir_path)

    def selected_to_convert(self):
        """
        User가 폴더 선택시 Event
        """
        self.select_dir()  # 폴더 선택
        selected_p = self.ui["path_line_edit"].text()
        selected_path = Path(selected_p)
        print(f"Selected Path: {selected_path}")

        if not selected_path:
            return

        # select_event.json 생성
        selected_fm = FileManager(selected_path)
        selected_fm.save_initial_json()

        # org Dir, jpg Dir 생성
        dm = DirectoryManager()
        org_path = selected_path / "org"
        dm.ensure_directory(org_path, exist_ok=True, parents=True)
        jpg_path = selected_path / "jpg"
        dm.ensure_directory(jpg_path, exist_ok=True, parents=True)

        if selected_fm.is_exr_sequence():
            """
            1. ffmpeg Convert (exr to jpg)
            2. EXif tool Convert -> 엑셀 -> Load Meta, 썸네일
            """

            #

            pass

        elif selected_fm.is_mov():
            """
            # 원래계획은 mov_to_exr은 선택으로 생성이지만 일단 주요기능부터
            """
            pass

        # else:
        #     pass

    def load_metadata(self):
        # TODO: 이후 구현
        pass
