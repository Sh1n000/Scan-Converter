from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QSpinBox,
)
import sys


class IOManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("I/O Manager")
        self.setMinimumSize(1200, 800)

        self.init_ui()  # UI 생성
        self.init_signals()  # 시그널 설정
        self.init_values()  # Data 불러오기 & 저장

    def init_ui(self):
        # 1. --- 메인 레이아웃 생성 ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 2. --- 위젯 리스트 정의 ---
        self.widget_list = [
            # (이름, 타입, 초기값)
            ("path_label", QLabel, "Path :"),
            (
                "path_line_edit",
                QLineEdit,
                "",
            ),
            ("select_btn", QPushButton, "Select"),
            ("load_btn", QPushButton, "Load"),
            ("btn_edit", QPushButton, "Edit"),
            ("btn_save", QPushButton, "Save"),
            ("btn_collect", QPushButton, "Collect"),
            ("btn_publish", QPushButton, "Publish"),
        ]

        # 3. --- 위젯 생성 ---
        self.widget_dict = {}

        for name, widget_type, value in self.widget_list:
            widget = widget_type()

            if isinstance(widget, QLabel):
                widget.setText(value)
            elif isinstance(widget, QPushButton):
                widget.setText(value)
            elif isinstance(widget, QLineEdit):
                widget.setText(value)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(value)
            elif isinstance(widget, QComboBox):
                widget.addItems(value)
            # elif isinstance(widget, QSpinBox):
            #     widget.setValue(value)

            self.widget_dict[name] = widget

        # 4. --- 레이아웃 구성 ---

        ## 4-1. 경로 선택 영역
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.widget_dict["path_label"])
        path_layout.addWidget(self.widget_dict["path_line_edit"], 3)
        path_layout.addWidget(self.widget_dict["select_btn"])
        path_layout.addWidget(self.widget_dict["load_btn"])

        ## 4-2. 테이블 영역
        self.table = QTableWidget(30, 10)
        self.table.setHorizontalHeaderLabels(
            ["Frame", "Timecode", "Clip Name", "Slate", "Note"]
        )

        ## 4-3. 하단 영역 (Excel, Action)
        bottom_layout = QHBoxLayout()

        ### Excel 관련 버튼
        excel_layout = QVBoxLayout()
        excel_layout.addWidget(QLabel("Excel"))
        excel_layout.addWidget(self.widget_dict["btn_edit"])
        excel_layout.addWidget(self.widget_dict["btn_save"])

        ### Action 관련 버튼
        action_layout = QVBoxLayout()
        action_layout.addWidget(QLabel("Action"))
        action_layout.addWidget(self.widget_dict["btn_collect"])
        action_layout.addWidget(self.widget_dict["btn_publish"])

        bottom_layout.addLayout(excel_layout)
        bottom_layout.addLayout(action_layout)

        ## 4-4. 메인 레이아웃에 추가
        main_layout.addLayout(path_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(bottom_layout)

    def init_signals(self):
        # 5. --- 시그널 연결 ---
        self.widget_dict["select_btn"].clicked.connect(self.select_scan_dir)
        self.widget_dict["load_btn"].clicked.connect(self.load_metadata)

    def init_values(self):
        pass

    def select_scan_dir(self):
        """
        Scan Data : EXR image sequence, MOV
        """
        scan_dir_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if scan_dir_path:
            self.widget_dict["path_line_edit"].setText(scan_dir_path)

    def load_metadata(self):
        """
        썸네일과 연결된 메타데이터를 UI에 보여줌
        """
        # # 예시: 테이블에 하드코딩된 값 채우기
        # data = [
        #     ("0000001", "01:00:00:01", "Clip_A", "Slate01", "Good"),
        #     ("0000002", "01:00:00:02", "Clip_A", "Slate01", "Blur"),
        # ]
        # self.table.setRowCount(len(data))
        # for i, row in enumerate(data):
        #     for j, val in enumerate(row):
        #         self.table.setItem(i, j, QTableWidgetItem(val))

        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = IOManagerWindow()
    win.show()
    sys.exit(app.exec())
