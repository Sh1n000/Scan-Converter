from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QComboBox,
    QSpinBox,
    QSpacerItem,
    QSizePolicy,
)

# import os


class UiBuilder(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # --- 위젯 리스트 --- UI 이름 / 타입 / setText
        # ComboBox는 addWidget사용
        self.widget_list = [
            ("project_label", QLabel, "Project :"),
            ("project_combo_box", QComboBox, ""),
            ("date_label", QLabel, "Date :"),
            ("date_combo_box", QComboBox, ""),
            ("path_label", QLabel, "Path :"),
            ("path_line_edit", QLineEdit, ""),
            ("select_btn", QPushButton, "Select to Convert"),
            ("load_btn", QPushButton, "Load Metadata"),
            ("btn_edit", QPushButton, "Edit"),
            ("btn_save", QPushButton, "Save"),
            ("btn_collect", QPushButton, "Collect"),
            ("btn_publish", QPushButton, "Publish"),
        ]
        self.widget_dict = {}

        for name, widget_type, value in self.widget_list:
            widget = widget_type()

            # Set Text
            if isinstance(widget, (QLabel, QPushButton, QLineEdit)):
                widget.setText(value)

            # elif isinstance(widget, QComboBox):
            #     widget.addItems(value)

            # 위젯 생성
            self.widget_dict[name] = widget

        header_layout1 = self.build_header_layout1()
        header_layout2 = self.build_header_layout2()
        table_widget = self.build_table()
        bottom_layout = self.build_bottom_layout()

        main_layout.addLayout(header_layout1)
        main_layout.addLayout(header_layout2)
        main_layout.addWidget(table_widget)
        main_layout.addLayout(bottom_layout)

    def build_header_layout1(self):
        """최상단 레이아웃"""
        layout = QHBoxLayout()
        layout.addWidget(self.widget_dict["project_label"])
        layout.addWidget(self.widget_dict["project_combo_box"])
        layout.addWidget(self.widget_dict["date_label"])
        layout.addWidget(self.widget_dict["date_combo_box"])

        return layout

    def build_header_layout2(self):
        """2번째 레이아웃"""
        layout = QHBoxLayout()
        layout.addWidget(self.widget_dict["path_label"])
        layout.addWidget(self.widget_dict["path_line_edit"], 3)
        layout.addWidget(self.widget_dict["select_btn"])
        layout.addWidget(self.widget_dict["load_btn"])
        return layout

    def build_table(self):
        """Plate List Table : 체크 박스 추가 예정"""
        table = QTableWidget(30, 10)
        table.setHorizontalHeaderLabels(
            ["Frame", "Timecode", "Clip Name", "Slate", "Note"]
        )
        self.table = table  # 다른 메서드에서 접근하려면 저장
        return table

    def build_bottom_layout(self):
        layout = QHBoxLayout()

        excel_layout = QVBoxLayout()
        excel_layout.addWidget(QLabel("Excel"))
        excel_layout.addWidget(self.widget_dict["btn_edit"])
        excel_layout.addWidget(self.widget_dict["btn_save"])

        action_layout = QVBoxLayout()
        action_layout.addWidget(QLabel("Action"))
        action_layout.addWidget(self.widget_dict["btn_collect"])
        action_layout.addWidget(self.widget_dict["btn_publish"])

        layout.addLayout(excel_layout)
        layout.addLayout(action_layout)

        return layout
