import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from gui.styles import MAIN_STYLE


def run_gui():
    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())