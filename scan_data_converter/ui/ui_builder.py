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
    QHeaderView,
    QSizePolicy,
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
            ("btn_excel_load", QPushButton, "Load"),
            ("btn_excel_edit", QPushButton, "Edit"),
            ("btn_excel_save", QPushButton, "Save"),
            ("btn_collect", QPushButton, "Collect"),
            ("btn_publish", QPushButton, "Publish"),
            ("btn_check_all", QPushButton, "Check All"),
            ("btn_uncheck_all", QPushButton, "Uncheck All"),
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
        main_layout.addLayout(self.build_header_layout3())
        main_layout.addWidget(self.build_main_table())
        main_layout.addLayout(self.build_bottom_layout())

    def build_header_layout1(self):
        layout = QHBoxLayout()
        layout.addWidget(self.widget_dict["path_label"])
        layout.addWidget(self.widget_dict["path_line_edit"], 3)
        layout.addWidget(self.widget_dict["btn_select"])
        layout.addWidget(self.widget_dict["btn_load"])
        return layout

    def build_header_layout2(self):
        # 전체 레이아웃
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Project와 Date 블록 사이만 띄우기

        project_lay = self.build_project_layout()
        layout.addLayout(project_lay)

        date_lay = self.build_date_layout()
        layout.addLayout(date_lay)

        layout.addStretch()  # 공간 채우기

        return layout

    def build_header_layout3(self):
        layout = QHBoxLayout()
        check_layout = self.build_check_layout()
        check_layout.setSizeConstraint(QHBoxLayout.SetFixedSize)

        layout.addLayout(check_layout)

        layout.addStretch()

        # project_lay = self.build_project_layout()
        # layout.addLayout(project_lay)

        # date_lay = self.build_date_layout()
        # layout.addLayout(date_lay)

        return layout

    def build_bottom_layout(self):
        layout = QHBoxLayout()
        """Excel Layout"""
        excel_layout = self.build_excel_layout()
        layout.addLayout(excel_layout)

        """Action Layout"""
        action_layout = self.build_action_layout()
        layout.addLayout(action_layout)

        return layout

    def build_check_layout(self):
        """Check All, Uncheck All"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        btn_all = self.widget_dict["btn_check_all"]
        btn_none = self.widget_dict["btn_uncheck_all"]

        btn_all.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_none.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_all.setFixedSize(80, 30)
        btn_none.setFixedSize(80, 30)

        layout.addWidget(btn_all)
        layout.addWidget(btn_none)
        return layout

    def build_table_check(self, row: int):
        """column idx : 0번째 row 에 체크박스 셀을 추가"""
        item = QTableWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table.setItem(row, 0, item)

    def build_main_table(self):
        table = QTableWidget()
        # widget_dict 에 'table' 키로 등록
        self.widget_dict["table"] = table

        """Column Header Setting"""
        headers = [
            "check",
            "thumbnail",
            "seq_name",
            "shot_name",
            "version",
            "type",
            "scan_path",
            "resoliution",
        ]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)

        table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )  # 체크박스 셀
        """Table Size Setting"""
        size_rate = 1.3
        default_row_height = 90 * size_rate
        table.verticalHeader().setDefaultSectionSize(default_row_height)

        table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Fixed
        )  # Thumbnail 셀
        table.setColumnWidth(1, 160 * size_rate)
        # 나머지 텍스트 열은 화면 꽉 채우기
        for col in range(2, len(headers)):
            table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

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

    def build_table_thumbnail(self, row: int, thumbnail_path: str):
        """idx : 1번째 row에 Thumbnail 추가"""
        label = QLabel()
        pixmap = QPixmap(thumbnail_path).scaled(80, 80, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        self.table.setCellWidget(row, 1, label)

    def build_excel_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Excel"))
        layout.addWidget(self.widget_dict["btn_excel_edit"])
        layout.addWidget(self.widget_dict["btn_excel_save"])
        return layout

    def build_action_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Action"))
        layout.addWidget(self.widget_dict["btn_collect"])
        layout.addWidget(self.widget_dict["btn_publish"])
        return layout

    def build_project_layout(self):
        project_lay = QHBoxLayout()
        project_lay.setContentsMargins(0, 0, 0, 0)
        project_lay.setSpacing(2)

        pro_lbl = self.widget_dict["project_label"]
        pro_lbl.setFixedWidth(60)
        pro_lbl.setMargin(0)  # 레이블 텍스트 주변 공백 없애기

        pro_cmb = self.widget_dict["project_combo_box"]
        pro_cmb.setFixedWidth(150)
        pro_cmb.setStyleSheet("padding:0px; margin:0px;")  # 내부 여백 최소화

        project_lay.addWidget(pro_lbl)
        project_lay.addWidget(pro_cmb)

        return project_lay

    def build_date_layout(self):
        date_lay = QHBoxLayout()
        date_lay.setContentsMargins(0, 0, 0, 0)
        date_lay.setSpacing(2)

        date_lbl = self.widget_dict["date_label"]
        date_lbl.setFixedWidth(40)
        date_lbl.setMargin(0)

        date_cmb = self.widget_dict["date_combo_box"]
        date_cmb.setFixedWidth(150)
        date_cmb.setStyleSheet("padding:0px; margin:0px;")

        date_lay.addWidget(date_lbl)
        date_lay.addWidget(date_cmb)
        return date_lay
