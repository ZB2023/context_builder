from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QStatusBar,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from gui.scan_tab import ScanTab
from gui.convert_tab import ConvertTab
from gui.delete_tab import DeleteTab
from gui.files_tab import FilesTab
from gui.settings_tab import SettingsTab
from gui.about_tab import AboutTab
from gui.icons import (
    icon_scan,
    icon_convert,
    icon_delete,
    icon_files,
    icon_settings,
    icon_about,
    icon_theme,
)
from gui.styles import DARK_THEME, LIGHT_THEME, generate_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = DARK_THEME
        self.setWindowTitle("Context Builder")
        self.setMinimumSize(1000, 750)
        self._set_icon()
        self._setup_ui()
        self._apply_theme()

    def _set_icon(self):
        icon_path = Path(__file__).parent.parent / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(52)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 8, 16, 8)

        app_title = QLabel("Context Builder")
        app_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(app_title)

        header_layout.addStretch()

        self.theme_button = QPushButton()
        self.theme_button.setFixedSize(36, 36)
        self.theme_button.setToolTip("Сменить тему")
        self.theme_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_button.clicked.connect(self._toggle_theme)
        header_layout.addWidget(self.theme_button)

        main_layout.addWidget(header)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setDocumentMode(True)

        self.scan_tab = ScanTab()
        self.convert_tab = ConvertTab()
        self.delete_tab = DeleteTab()
        self.files_tab = FilesTab()
        self.settings_tab = SettingsTab()
        self.about_tab = AboutTab()

        self.tabs.addTab(self.scan_tab, "Сканирование")
        self.tabs.addTab(self.convert_tab, "Конвертация")
        self.tabs.addTab(self.delete_tab, "Удаление")
        self.tabs.addTab(self.files_tab, "Файлы")
        self.tabs.addTab(self.settings_tab, "Настройки")
        self.tabs.addTab(self.about_tab, "О программе")

        main_layout.addWidget(self.tabs)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")

    def _apply_theme(self):
        t = self.current_theme
        stylesheet = generate_stylesheet(t)
        self.setStyleSheet(stylesheet)

        color = t["accent"]
        self.tabs.setTabIcon(0, icon_scan(color))
        self.tabs.setTabIcon(1, icon_convert(color))
        self.tabs.setTabIcon(2, icon_delete(t["danger"]))
        self.tabs.setTabIcon(3, icon_files(color))
        self.tabs.setTabIcon(4, icon_settings(color))
        self.tabs.setTabIcon(5, icon_about(color))
        self.theme_button.setIcon(icon_theme(color))

        theme_name = "Тёмная" if t["name"] == "dark" else "Светлая"
        self.status_bar.showMessage(f"Тема: {theme_name}")

    def _toggle_theme(self):
        if self.current_theme["name"] == "dark":
            self.current_theme = LIGHT_THEME
        else:
            self.current_theme = DARK_THEME

        self._apply_theme()