# class IOManagerWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("I/O Manager")
#         self.setMinimumSize(1200, 800)

#         self.ui = UiBuilder()
#         self.setCentralWidget(self.ui)

#         self.init_signals()
#         self.load_project_list()

#     def init_signals(self):
#         self.ui.widget_dict["select_btn"].clicked.connect(self.select_scan_dir)
#         self.ui.widget_dict["load_btn"].clicked.connect(self.load_metadata)
#         # Project Combo Box
#         self.ui.widget_dict["project_combo_box"].currentTextChanged.connect(
#             self.link_to_project_scan_dirs
#         )

#     def select_scan_dir(self):
#         """
#         폴더만 선택가능
#         Select Scan Directory
#         Scan Data : EXR image sequence, MOV
#         """
#         # 폴더만 선택할 수 있게 제한
#         options = QFileDialog.Options()
#         options |= QFileDialog.ShowDirsOnly

#         scan_dir_path = QFileDialog.getExistingDirectory(
#             self,
#             "Select Folder",
#             self.ui.widget_dict["path_line_edit"].text(),  # 시작 폴더 (기본값)
#             options=options,
#         )
#         if scan_dir_path:
#             self.ui.widget_dict["path_line_edit"].setText(scan_dir_path)

#     def get_project_list(self):
#         """show경로에서 Project Dir 리스트 반환"""
#         path = "/show"
#         project_list = []
#         for folder in os.listdir(path):
#             if os.path.isdir(os.path.join(path, folder)):
#                 project_list.append(folder)
#         return project_list

#     def load_project_list(self):
#         project_list = self.get_project_list()
#         self.ui.widget_dict["project_combo_box"].clear()
#         self.ui.widget_dict["project_combo_box"].addItems(project_list)

#     def link_to_project_scan_path(self):
#         """ComboBox에서 Project를 받아, scan 경로를 자동으로 연결"""
#         selected_project = self.ui.widget_dict["project_combo_box"].currentText()
#         if selected_project:
#             project_path = f"/show/{selected_project}"
#             scan_dirs_path = f"{project_path}/product/scan"
#             self.ui.widget_dict["path_line_edit"].setText(scan_dirs_path)
#             print(
#                 f"[INFO] 프로젝트 선택: {selected_project}, 경로 설정: {scan_dirs_path}"
#             )

#     def load_scan_date_list(self):
#         selected_project = self.ui.widget_dict["project_combo_box"].currentText()
#         project_path = f"/show/{selected_project}"
#         scan_date_list = []
#         for folder in os.listdir(f"{project_path}/product/scan"):
#             if os.path.isdir(os.path.join(f"{project_path}/product/scan", folder)):
#                 scan_date_list.append(folder)
#         self.ui.widget_dict["date_combo_box"].clear()
#         self.ui.widget_dict["date_combo_box"].addItems(scan_date_list)

#     def link_to_scan_date_path(self):
#         selected_project = self.ui.widget_dict["project_combo_box"].currentText()
#         selected_date = self.ui.widget_dict["date_combo_box"].currentText()
#         if selected_project and selected_date:
#             project_path = f"/show/{selected_project}"
#             scan_date_path = f"{project_path}/product/scan/{selected_date}"
#             self.ui.widget_dict["path_line_edit"].setText(scan_date_path)
#             print(
#                 f"[INFO] 프로젝트 선택: {selected_project}, 일자 선택: {selected_date}, 경로 설정: {scan_date_path}"
#             )


#     def load_metadata(self):
#         # 실제 메타데이터 로딩 구현 예정
#         pass
