from PySide6.QtWidgets import QMainWindow
from .ui_builder import UiBuilder
from .path_manager import PathManager
from .ui_event_handler import IOManagerEventHandler

# from pathlib import Path


class IOManagerWindow(QMainWindow):
    """I/O Manager 메인 윈도우"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("I/O Manager")
        self.setMinimumSize(1200, 800)

        self.ui = UiBuilder()
        self.setCentralWidget(self.ui)

        show_root = "/show"
        self.path_mgr = PathManager(show_root)

        self.setup_ui()

        # 이벤트 핸들러 연결
        self.event_handler = IOManagerEventHandler(
            ui=self.ui.widget_dict, path_manager=self.path_mgr
        )
        self.event_handler.setup_signals()

    def setup_ui(self):
        """기본 UI 구성"""
        self.ui.widget_dict["path_line_edit"].setText(str(self.path_mgr.show_root))
