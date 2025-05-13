from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QObject
from pathlib import Path
from managers.file_manager import FileManager
from converters.media_converter import MediaConverter
from utils.folder_generator import DirectoryManager


class IOManagerEventHandler:
    """UI Event 관리 Class"""

    def __init__(self, ui_widgets: dict, path_manager):
        super().__init__()
        self.ui = ui_widgets
        self.path_mgr = path_manager
        self._connect_signals()

    def _connect_signals(self):
        #     # 버튼 클릭 이벤트 연결
        self.ui["btn_select"].clicked.connect(self.selected_to_convert)
        self.ui["btn_load"].clicked.connect(self.load_metadata)

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
        Convert 버튼 클릭 시
        1. org 생성후 파일이동
        2. jpg Convert
        3. event json 생성
        """
        self.select_dir()
        selected_p = self.ui["path_line_edit"].text()
        selected_path = Path(selected_p)
        print(f"Selected Path: {selected_path}")

        if not selected_path:
            return

        # org, jpg 디렉토리 생성
        dm = DirectoryManager()
        org_path = selected_path / "org"
        jpg_path = selected_path / "jpg"
        dm.ensure_directory(org_path, exist_ok=True, parents=True)
        dm.ensure_directory(jpg_path, exist_ok=True, parents=True)

        selected_fm = FileManager(selected_path)

        # select_event.json 생성
        selected_fm.save_initial_json()
        # config 생성
        cfg = selected_fm.generate_config()

        # 1) 변환 대상 체크
        if not (selected_fm.is_exr_sequence() or selected_fm.is_mov()):
            QMessageBox.information(None, "알림", "변환 대상 파일이 없습니다.")
            return

        mc = MediaConverter(cfg)

        if selected_fm.is_exr_sequence():
            try:
                mc.ffmpeg_exr_to_jpg()  # 또는 mc.run()
            except Exception as e:
                err_box = QMessageBox()
                err_box.setIcon(QMessageBox.Critical)
                err_box.setWindowTitle("오류 발생")
                err_box.setText("변환 중 오류가 발생했습니다.")
                err_box.setInformativeText(str(e))
                err_box.exec()
                return

            # exr 파일 이동
            for exr in selected_fm.file_dict[".exr"]:
                dm.move_file(exr, org_path / exr.name)

            # 메세지
            QMessageBox.information(
                None,
                "완료",
                f"1. org 파일 이동 \n org : {org_path} \n 2. jpg 파일 변환 \n jpg : {jpg_path}",
                QMessageBox.Ok,
            )

        elif selected_fm.is_mov():  # mov
            """보류"""
            pass
            # mov 파일 이동
            for mov in selected_fm.file_dict[".mov"]:
                dm.move_file(mov, org_path / mov.name)

    def load_metadata(self):
        """Metadata 로드 처리 (추후 구현)"""
        pass
