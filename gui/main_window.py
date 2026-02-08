from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QLabel,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import Qt, QSize

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
    icon_theme_toggle,
)
from gui.styles import DARK_THEME, LIGHT_THEME, generate_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = DARK_THEME
        self.setWindowTitle("Context Builder")
        self.resize(1150, 780)
        self.setMinimumSize(950, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self._setup_sidebar()
        self._setup_content()
        self._apply_theme()

    def _setup_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(250)

        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(20, 24, 20, 8)
        header_layout.setSpacing(2)

        title = QLabel("Context Builder")
        title.setProperty("cssClass", "header")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)

        version = QLabel("v1.2.0")
        version.setProperty("cssClass", "subtitle")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(version)

        layout.addWidget(header_container)
        layout.addSpacing(16)

        sep_label = QLabel("  НАВИГАЦИЯ")
        sep_label.setProperty("cssClass", "field-label")
        sep_label.setContentsMargins(20, 8, 0, 4)
        layout.addWidget(sep_label)

        self.nav_list = QListWidget()
        self.nav_list.setObjectName("NavList")
        self.nav_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.nav_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nav_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nav_list.setIconSize(QSize(20, 20))

        self.nav_list.currentRowChanged.connect(self._change_page)

        self._add_nav_item("Сканирование", icon_scan, 0)
        self._add_nav_item("Конвертация", icon_convert, 1)
        self._add_nav_item("Очистка", icon_delete, 2)
        self._add_nav_item("Файлы", icon_files, 3)
        self._add_nav_item("Настройки", icon_settings, 4)

        layout.addWidget(self.nav_list)
        layout.addStretch()

        bottom_sep = QLabel("  ПРОЧЕЕ")
        bottom_sep.setProperty("cssClass", "field-label")
        bottom_sep.setContentsMargins(20, 8, 0, 4)
        layout.addWidget(bottom_sep)

        self.nav_list_bottom = QListWidget()
        self.nav_list_bottom.setObjectName("NavList")
        self.nav_list_bottom.setFixedHeight(110)
        self.nav_list_bottom.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.nav_list_bottom.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nav_list_bottom.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nav_list_bottom.setIconSize(QSize(20, 20))
        self.nav_list_bottom.itemClicked.connect(self._handle_bottom_click)

        self.about_item = QListWidgetItem("О программе")
        self.nav_list_bottom.addItem(self.about_item)

        self.theme_item = QListWidgetItem("Светлая тема")
        self.nav_list_bottom.addItem(self.theme_item)

        layout.addWidget(self.nav_list_bottom)
        layout.addSpacing(12)

        self.main_layout.addWidget(self.sidebar)

    def _setup_content(self):
        self.content_area = QStackedWidget()
        self.tabs = [
            ScanTab(),
            ConvertTab(),
            DeleteTab(),
            FilesTab(),
            SettingsTab(),
            AboutTab(),
        ]
        for tab in self.tabs:
            self.content_area.addWidget(tab)

        self.main_layout.addWidget(self.content_area)
        self.nav_list.setCurrentRow(0)

    def _add_nav_item(self, text, icon_func, index):
        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, index)
        self.nav_list.addItem(item)

    def _change_page(self, row):
        item = self.nav_list.item(row)
        if item:
            index = item.data(Qt.UserRole)
            self.content_area.setCurrentIndex(index)
            self.nav_list_bottom.clearSelection()

    def _handle_bottom_click(self, item):
        if item == self.about_item:
            self.content_area.setCurrentIndex(5)
            self.nav_list.clearSelection()
        elif item == self.theme_item:
            self._toggle_theme()
            item.setSelected(False)

    def _toggle_theme(self):
        if self.current_theme["name"] == "dark":
            self.current_theme = LIGHT_THEME
            self.theme_item.setText("Тёмная тема")
        else:
            self.current_theme = DARK_THEME
            self.theme_item.setText("Светлая тема")
        self._apply_theme()

    def _apply_theme(self):
        self.setStyleSheet(generate_stylesheet(self.current_theme))

        c = self.current_theme["primary"]
        is_dark = self.current_theme["name"] == "dark"
        delete_c = self.current_theme["danger"]

        icons_main = [
            (icon_scan, c),
            (icon_convert, c),
            (icon_delete, delete_c),
            (icon_files, c),
            (icon_settings, c),
        ]
        for i, (icon_func, color) in enumerate(icons_main):
            item = self.nav_list.item(i)
            if item:
                item.setIcon(icon_func(color=color, size=24))

        self.about_item.setIcon(icon_about(color=c, size=24))
        self.theme_item.setIcon(icon_theme_toggle(is_dark=is_dark, color=c, size=24))