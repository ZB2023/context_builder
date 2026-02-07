import sys
import ctypes
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from gui.main_window import MainWindow
from gui.styles import MAIN_STYLE


def set_windows_taskbar_icon():
    try:
        app_id = "contextbuilder.app.gui.1.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except (AttributeError, OSError):
        pass


def run_gui():
    set_windows_taskbar_icon()

    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLE)
    app.setApplicationName("Context Builder")
    app.setApplicationVersion("1.1.0")
    app.setOrganizationName("ContextBuilder")

    icon_path = Path(__file__).parent.parent / "icon.ico"
    if icon_path.exists():
        icon = QIcon(str(icon_path))
        app.setWindowIcon(icon)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())