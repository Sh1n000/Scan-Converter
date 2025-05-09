from PySide6.QtWidgets import QFileDialog
from pathlib import Path

from managers.file_manager import FileManager
from utils.folder_generator import DirectoryManager


class IOManagerEventHandler:
    """UI Event 관리 Class"""

    def __init__(self, ui: dict, path_manager):
        self.ui = ui
        self.path_mgr = path_manager

    def setup_signals(self):
        # 버튼 클릭 이벤트 연결
        self.ui["select_btn"].clicked.connect(self.selected_to_convert)
        self.ui["load_btn"].clicked.connect(self.load_metadata)

        # 콤보박스 변경 이벤트 연결
        self.ui["project_combo_box"].currentTextChanged.connect(self.project_changed)
        self.ui["date_combo_box"].currentTextChanged.connect(self.date_changed)

        # 초기 프로젝트 리스트 로드
        self.load_project_list()

    def update_path_line_edit(self, path: Path):
        """Path Line Edit에 경로를 문자열로 설정"""
        self.ui["path_line_edit"].setText(str(path))

    def load_project_list(self):
        """프로젝트 리스트를 콤보박스에 로드"""
        self.ui["project_combo_box"].clear()
        self.ui["project_combo_box"].addItem("Select Project")
        project_list = self.path_mgr.get_project_list()
        self.ui["project_combo_box"].addItems(project_list)

    def load_scan_date_list(self):
        """Date 리스트를 콤보박스에 로드"""
        self.ui["date_combo_box"].clear()
        self.ui["date_combo_box"].addItem("Select Date")
        scan_date_list = self.path_mgr.get_scan_date_list()
        self.ui["date_combo_box"].addItems(scan_date_list)

    def project_changed(self, item: str):
        """프로젝트 선택 시 경로와 Date 리스트 업데이트"""
        if item == "Select Project":
            self.update_path_line_edit(Path(""))
            self.ui["date_combo_box"].clear()
            self.ui["date_combo_box"].addItem("Select Date")
            return

        scan_path = self.path_mgr.project_to_path(item, "scan")
        self.update_path_line_edit(scan_path)
        self.load_scan_date_list()

    def date_changed(self, item: str):
        """Date 선택 시 경로 업데이트"""
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
        """폴더 선택 대화상자를 띄우고 선택된 경로를 Path Line Edit에 반영"""
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
        """Convert 버튼 클릭 시 폴더 선택 및 초기 변환 준비"""
        self.select_dir()
        selected_p = self.ui["path_line_edit"].text()
        selected_path = Path(selected_p)
        print(f"Selected Path: {selected_path}")

        if not selected_path:
            return

        # select_event.json 생성
        selected_fm = FileManager(selected_path)
        selected_fm.save_initial_json()

        # org, jpg 디렉토리 생성
        dm = DirectoryManager()
        org_path = selected_path / "org"
        dm.ensure_directory(org_path, exist_ok=True, parents=True)
        jpg_path = selected_path / "jpg"
        dm.ensure_directory(jpg_path, exist_ok=True, parents=True)

        # 변환 로직 분기
        if selected_fm.is_exr_sequence():
            # EXR 시퀀스 변환 처리
            pass
        elif selected_fm.is_mov():
            # MOV 파일 변환 처리
            pass

    def load_metadata(self):
        """Metadata 로드 처리 (추후 구현)"""
        pass
