# ui/ui_main_window.py

from pathlib import Path

from PySide6.QtWidgets import QMainWindow

from ui.ui_builder import UiBuilder
from ui.ui_event_handler import IOManagerEventHandler
from managers.path_manager import PathManager


class IOManagerWindow(QMainWindow):
    """I/O Manager 메인 윈도우"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("I/O Manager")
        self.setMinimumSize(1200, 800)

        # UI 빌더 초기화
        self.ui = UiBuilder()
        self.setCentralWidget(self.ui)

        # PathManager 초기화 (show_root 는 Path 객체로 관리)
        show_root = Path("/show")
        self.path_mgr = PathManager(show_root)

        # 이벤트 핸들러 연결
        self.event_handler = IOManagerEventHandler(
            self.ui.widget_dict,
            self.path_mgr,
        )

        # UI 초기값 세팅
        self.setup_ui()

    def setup_ui(self):
        """기본 UI 구성: 경로 입력란 초기값 세팅"""
        # show_root 를 문자열로 바꿔 QLineEdit 에 입력
        self.ui.widget_dict["path_line_edit"].setText(str(self.path_mgr.show_root))
