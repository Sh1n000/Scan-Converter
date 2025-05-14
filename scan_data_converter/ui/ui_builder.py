from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class UiBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # --- 위젯 리스트: 이름, 타입, 초기 텍스트 ---
        self.widget_list = [
            ("project_label", QLabel, "Project :"),
            ("project_combo_box", QComboBox, ""),
            ("date_label", QLabel, "Date :"),
            ("date_combo_box", QComboBox, ""),
            ("path_label", QLabel, "Path :"),
            ("path_line_edit", QLineEdit, ""),
            ("btn_select", QPushButton, "Select to Convert"),
            ("btn_load", QPushButton, "Load Metadata"),
            ("btn_excel_edit", QPushButton, "Edit"),
            ("btn_excel_save", QPushButton, "Save"),
            ("btn_collect", QPushButton, "Collect"),
            ("btn_publish", QPushButton, "Publish"),
        ]
        self.widget_dict = {}

        # 위젯 생성 및 초기 텍스트 설정
        for name, widget_type, text in self.widget_list:
            widget = widget_type()
            if isinstance(widget, (QLabel, QPushButton, QLineEdit)):
                widget.setText(text)
            self.widget_dict[name] = widget

        # 레이아웃 구성
        main_layout.addLayout(self.build_header_layout1())
        main_layout.addLayout(self.build_header_layout2())
        main_layout.addWidget(self.build_main_table())
        main_layout.addLayout(self.build_bottom_layout())

    def build_header_layout1(self):
        layout = QHBoxLayout()
        layout.addWidget(self.widget_dict["project_label"])
        layout.addWidget(self.widget_dict["project_combo_box"])
        layout.addWidget(self.widget_dict["date_label"])
        layout.addWidget(self.widget_dict["date_combo_box"])
        return layout

    def build_header_layout2(self):
        layout = QHBoxLayout()
        layout.addWidget(self.widget_dict["path_label"])
        layout.addWidget(self.widget_dict["path_line_edit"], 3)
        layout.addWidget(self.widget_dict["btn_select"])
        layout.addWidget(self.widget_dict["btn_load"])
        return layout

    def build_main_table(self):
        # Plate List Table: 초기 행에는 체크박스가 표시됨
        table = QTableWidget()

        """Column Header Setting"""
        headers = [
            "Check",
            "Thumbnail",
            "seq_name",
            "shot_name",
            "version",
            "type",
            "scan_path",
            "Metadata",
        ]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)

        """Row Setting"""
        # 초반 설정
        initial_rows = 30
        table.setRowCount(initial_rows)

        self.table = table
        for row in range(initial_rows):
            self.build_table_check(row)

        # Load Metadata btn으로 scan_list를 구성
        scan_list = []  # User가 선택한 Meta Data

        for meta_data in scan_list:
            row = scan_list.index(meta_data)
            table.setRowCount(row + 1)
            self.build_table_check(row)
            # self.build_table_thumbnail(row, scan_data["thumbnail"])

        return table

    def build_table_check(self, row: int):
        """주어진 행에 체크박스 셀을 추가"""
        item = QTableWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        self.table.setItem(row, 0, item)

    def build_table_thumbnail(self, row: int, thumbnail_path: str):
        """"""
        label = QLabel()
        pixmap = QPixmap(thumbnail_path).scaled(80, 80, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        self.table.setCellWidget(row, 1, label)

    def build_bottom_layout(self):
        layout = QHBoxLayout()

        excel_layout = QVBoxLayout()
        excel_layout.addWidget(QLabel("Excel"))
        excel_layout.addWidget(self.widget_dict["btn_excel_edit"])
        excel_layout.addWidget(self.widget_dict["btn_excel_save"])

        action_layout = QVBoxLayout()
        action_layout.addWidget(QLabel("Action"))
        action_layout.addWidget(self.widget_dict["btn_collect"])
        action_layout.addWidget(self.widget_dict["btn_publish"])

        layout.addLayout(excel_layout)
        layout.addLayout(action_layout)
        return layout
