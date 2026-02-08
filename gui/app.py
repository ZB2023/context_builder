import sys
import ctypes
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFont

from gui.main_window import MainWindow


def set_windows_taskbar_icon():
    try:
        app_id = "contextbuilder.app.gui.1.2.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except (AttributeError, OSError):
        pass


def run_gui():
    set_windows_taskbar_icon()

    app = QApplication(sys.argv)
    app.setApplicationName("Context Builder")
    app.setApplicationVersion("1.2.0")
    app.setOrganizationName("ContextBuilder")

    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    app.setFont(font)

    icon_path = Path(__file__).parent.parent / "icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())