# scripts/run_app.py

import sys
from PySide6.QtWidgets import QApplication
from ui.ui_main_window import IOManagerWindow

# from core.shotgrid_link import ShotGridLink


def main():
    # 1) ShotGrid 연결 세팅
    # 연결시 주석해제
    # sg = ShotGridLink(
    #     server_url="https://your-site.shotgrid.autodesk.com",
    #     script_name="my_script",
    #     api_key="MY_SECRET_KEY",
    # )

    # 2) Qt 애플리케이션 시작
    app = QApplication(sys.argv)
    # window = IOManagerWindow(sg_link=sg)
    window = IOManagerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
