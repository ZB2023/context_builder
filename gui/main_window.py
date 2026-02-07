from PySide6.QtWidgets import QMainWindow, QTabWidget
from PySide6.QtCore import Qt

from gui.scan_tab import ScanTab
from gui.convert_tab import ConvertTab
from gui.delete_tab import DeleteTab
from gui.files_tab import FilesTab
from gui.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Context Builder")
        self.setMinimumSize(900, 700)
        self._setup_ui()

    def _setup_ui(self):
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)

        tabs.addTab(ScanTab(), "📁 Сканирование")
        tabs.addTab(ConvertTab(), "🔄 Конвертация")
        tabs.addTab(DeleteTab(), "🗑️ Удаление")
        tabs.addTab(FilesTab(), "🔍 Файлы")
        tabs.addTab(SettingsTab(), "⚙️ Настройки")

        self.setCentralWidget(tabs)