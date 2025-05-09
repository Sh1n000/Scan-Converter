import sys
from PySide6.QtWidgets import QApplication
from io_manager.ui_main_window import IOManagerWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = IOManagerWindow()
    win.show()
    sys.exit(app.exec())
