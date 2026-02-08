from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QTextEdit,
    QMessageBox,
    QListWidget,
    QScrollArea,
    QSplitter,
)
from PySide6.QtCore import Qt

from src.config import save_profile, load_profile, list_profiles, delete_profile


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        container.setMaximumWidth(960)
        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("Настройки и профили")
        title.setProperty("cssClass", "title")
        layout.addWidget(title)

        subtitle = QLabel("Сохраняйте и загружайте конфигурации для повторяющихся задач")
        subtitle.setProperty("cssClass", "subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(4)

        profiles_group = QGroupBox("Профили")
        profiles_layout = QVBoxLayout(profiles_group)
        profiles_layout.setSpacing(8)
        profiles_layout.setContentsMargins(16, 16, 16, 16)

        self.profile_list = QListWidget()
        self.profile_list.setMinimumHeight(80)
        self.profile_list.setMaximumHeight(180)
        profiles_layout.addWidget(self.profile_list)

        nr = QHBoxLayout()
        nr.setSpacing(8)
        nl = QLabel("Имя")
        nl.setProperty("cssClass", "field-label")
        nl.setFixedWidth(35)
        nr.addWidget(nl)
        self.profile_name_input = QLineEdit()
        self.profile_name_input.setPlaceholderText("Название нового профиля")
        nr.addWidget(self.profile_name_input)
        profiles_layout.addLayout(nr)

        profiles_layout.addSpacing(4)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addStretch()

        self.refresh_button = QPushButton("  Обновить  ")
        self.refresh_button.setProperty("cssClass", "secondary")
        self.refresh_button.setMinimumWidth(110)
        self.refresh_button.setMinimumHeight(34)
        self.refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_button.clicked.connect(self._refresh)
        btn_row.addWidget(self.refresh_button)

        self.save_button = QPushButton("  Сохранить  ")
        self.save_button.setProperty("cssClass", "success")
        self.save_button.setMinimumWidth(110)
        self.save_button.setMinimumHeight(34)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self._save)
        btn_row.addWidget(self.save_button)

        self.delete_button = QPushButton("  Удалить  ")
        self.delete_button.setProperty("cssClass", "danger")
        self.delete_button.setMinimumWidth(110)
        self.delete_button.setMinimumHeight(34)
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.clicked.connect(self._delete)
        btn_row.addWidget(self.delete_button)

        btn_row.addStretch()
        profiles_layout.addLayout(btn_row)

        layout.addWidget(profiles_group)
        layout.addStretch(1)

        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addWidget(container)
        wrapper.addStretch()

        scroll_content = QWidget()
        scroll_content.setLayout(wrapper)
        scroll.setWidget(scroll_content)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(scroll)

        log_widget = QWidget()
        log_l = QVBoxLayout(log_widget)
        log_l.setContentsMargins(16, 8, 16, 8)
        log_l.setSpacing(4)

        lh = QHBoxLayout()
        ll = QLabel("Лог")
        ll.setProperty("cssClass", "field-label")
        lh.addWidget(ll)
        lh.addStretch()
        cb = QPushButton("Очистить")
        cb.setProperty("cssClass", "secondary")
        cb.setFixedHeight(24)
        cb.setMaximumWidth(90)
        cb.setCursor(Qt.CursorShape.PointingHandCursor)
        lh.addWidget(cb)
        log_l.addLayout(lh)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Результаты операций появятся здесь...")
        cb.clicked.connect(lambda: self.log.clear())
        log_l.addWidget(self.log)

        splitter.addWidget(log_widget)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([600, 120])

        outer.addWidget(splitter)
        self._refresh()

    def _refresh(self):
        self.profile_list.clear()
        for p in list_profiles():
            self.profile_list.addItem(p)
        self.log.append(f"Профилей: {self.profile_list.count()}")

    def _save(self):
        name = self.profile_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название")
            return
        settings = {
            "mode": "single",
            "root_path": "",
            "include_tree": True,
            "export_format": "txt",
        }
        save_profile(name, settings)
        self.profile_name_input.clear()
        self.log.append(f"✓ Сохранён: {name}")
        self._refresh()

    def _delete(self):
        current = self.profile_list.currentItem()
        if not current:
            QMessageBox.warning(self, "Ошибка", "Выберите профиль")
            return
        name = current.text()
        r = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if r == QMessageBox.StandardButton.Yes:
            delete_profile(name)
            self.log.append(f"✓ Удалён: {name}")
            self._refresh()