from PySide6.QtWidgets import QFileDialog, QMessageBox
from pathlib import Path
from managers.file_manager import FileManager
from converters.media_converter import MediaConverter
from utils.folder_generator import DirectoryManager
from converters.convert_cfg import ConvertConfigFactory
from managers.exif_manager import ExifManager
from managers.metadata_manager import MetadataManager


class IOManagerEventHandler:
    """UI Event 관리 Class"""

    def __init__(self, ui_widgets: dict, path_manager):
        super().__init__()
        self.ui = ui_widgets
        self.path_mgr = path_manager
        # self.scan_list = []
        self._connect_signals()

    def _connect_signals(self):
        # 콤보박스 변경 이벤트 연결
        self.ui["project_combo_box"].currentTextChanged.connect(self.project_changed)
        self.ui["date_combo_box"].currentTextChanged.connect(self.date_changed)

        # 버튼 클릭 이벤트 연결
        self.ui["btn_select"].clicked.connect(self.selected_to_convert)
        self.ui["btn_load"].clicked.connect(self.load_metadata)
        # self.ui["btn_excel_edit"].clicked.connect(self.edit_metadata)
        # self.ui["btn_excel_save"].clicked.connect(self.save_metadata)
        # self.ui["btn_collect"].clicked.connect(self.collect_to_shot) # Seq / Shot Name이 지정된 경로 생성 후 Data이동
        # self.ui["btn_publish"].clicked.connect(self.)

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

        # "/show/{project}/scan"
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
        1. org Dir, jpg Dir 생성
        2. event json 생성
        3. jpg ffmpeg Converting
        4. 원본 파일 이동 (org)
        """
        self.select_dir()
        selected_p = self.ui["path_line_edit"].text()
        selected_path = Path(selected_p)
        selected_fm = FileManager(selected_path)
        print(f"Selected Path: {selected_path}")

        # Converting 폴더 체크
        if not (selected_fm.is_exr_sequence() or selected_fm.is_mov()):
            QMessageBox.information(None, "알림", "변환 대상 파일이 없습니다.")
            return

        """org, jpg 디렉토리 생성"""
        dm = DirectoryManager()
        org_path = selected_path / "org"
        jpg_path = selected_path / "jpg"
        # filmstrip_path = selected_path / "filmstrip"
        # montage_path = selected_path / "montage"  #################

        dm.ensure_directory(org_path, exist_ok=True, parents=True)
        dm.ensure_directory(jpg_path, exist_ok=True, parents=True)
        # dm.ensure_directory(filmstrip_path, exist_ok=True, parents=True)
        # dm.ensure_directory(
        #     montage_path, exist_ok=True, parents=True
        # )  ##################

        # select_event.json 생성
        selected_fm.save_select_event_json()

        # Convert Config 생성
        selected_cfg_factory = ConvertConfigFactory(selected_fm)

        if selected_fm.is_exr_sequence():
            """Scan Data = EXR Sequence"""
            try:
                exr_to_jpg = selected_cfg_factory.get("exr_to_jpg")
                jpg_mc = MediaConverter(exr_to_jpg)
                jpg_mc.convert()
                print("EXR to JPG Conversion Complete")

                # jpg_to_webm = selected_cfg_factory.get("jpg_seq_to_webm")
                # webm_mc = MediaConverter(jpg_to_webm)
                # webm_mc.convert()

                # jpg_to_mp4 = selected_cfg_factory.get("jpg_seq_to_mp4")
                # mp4_mc = MediaConverter(jpg_to_mp4)
                # mp4_mc.convert()

                """
                Meta Data 생성 (JSON & 엑셀)
                """
                # 1) EXR 파일 리스트 수집
                exr_dict = selected_fm.collect_by_extension()
                exr_files = exr_dict[".exr"]

                # 2) ExifManager로 메타데이터 추출
                exif_mgr = ExifManager()
                raw_meta_list = exif_mgr.extract_metadata(exr_files)
                # print(f"Raw Meta List: {raw_meta_list}")

                # 3) MetadataManager에 맵핑 & 저장
                meta_mgr = MetadataManager()
                for path, meta in zip(exr_files, raw_meta_list):
                    meta_mgr.add_record(path, meta)

                # 4) JSON 또는 Excel로 출력
                meta_mgr.save_json(selected_path)
                # 또는
                meta_mgr.save_excel(selected_path)

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

            # #################
            # jpg_to_montage = selected_cfg_factory.get("jpg_seq_to_tile_montage")
            # montage_mc = MediaConverter(jpg_to_montage)
            # montage_mc.convert()

            # # Filmstrip 만들기
            # film_cfg = selected_cfg_factory.get("jpg_seq_to_filmstrip", columns=5)
            # film_mc = MediaConverter(film_cfg)
            # film_mc.convert()

            # 메세지 박스
            QMessageBox.information(
                None,
                "완료",
                f"1. org 파일 이동 \n org : {org_path} \n 2. jpg 파일 변환 \n jpg : {jpg_path} \n 3. 메타 데이터 생성 \n json/excel : {selected_path}/metadata",
                QMessageBox.Ok,
            )

        elif selected_fm.is_mov():  # mov
            """MOV는 보류"""
            pass
            # mov 파일 이동
            for mov in selected_fm.file_dict[".mov"]:
                dm.move_file(mov, org_path / mov.name)

    def load_metadata(self):
        """
        - select_to_convert 버튼으로 생성된 엑셀파일 불러오기
        -  Metadata (엑셀파일)를 Table Wiget의 scan_list에 추가

        scan_list = [
            {
            "file_path :"",
            "thumbnail": thumbnail_path,
            }
            ]
        - 썸네일 UI와 연결
        """
        pass

    def edit_metadata(self):
        """Check Box에 체크되어있는 Metadata를 수정할 수 있도록 엑셀파일 실행"""
        pass

    def save_metadata(self):
        """
        1. Seq / Shot Name이 있는지 없는지 체크  ( Validate )
        2. 수정된 엑셀파일 저장
        3. Seq / Shot Name이 지정된 경로 생성
        4. Seq / Shot Name 지정된 경로로 Data 이동
        """
        pass

    def collect_to_shot(self):
        """
        1. Seq / Shot Name이 지정된 경로 생성
        2. Seq / Shot Name 지정된 경로로 Data 이동
        """
        pass

    def nuke_set_slate_info(self):
        """
        ShotGrid 연결 +  Publish 까지 구현되면
        Publish할 Slate 썸네일

        Nuke의 Group Node로 Slate 정보 Setting
        1. Date   2. Project 3. FrameRate
        4.seq/shot 5. [value firtst_frame]_[value last_frame]([value frame])

        """
        pass
