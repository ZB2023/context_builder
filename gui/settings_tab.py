from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QTextEdit,
    QMessageBox,
    QListWidget,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

from src.config import save_profile, load_profile, list_profiles, delete_profile


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("⚙️ Настройки и профили")
        title.setObjectName("title")
        layout.addWidget(title)

        profiles_group = QGroupBox("Профили")
        profiles_layout = QVBoxLayout(profiles_group)

        self.profile_list = QListWidget()
        profiles_layout.addWidget(self.profile_list)

        self.refresh_button = QPushButton("Обновить список")
        self.refresh_button.setProperty("cssClass", "secondary")
        self.refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_button.clicked.connect(self._refresh_profiles)
        profiles_layout.addWidget(self.refresh_button)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Имя профиля:"))
        self.profile_name_input = QLineEdit()
        self.profile_name_input.setPlaceholderText("Название нового профиля")
        name_layout.addWidget(self.profile_name_input)
        profiles_layout.addLayout(name_layout)

        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Сохранить")
        self.save_button.setProperty("cssClass", "success")
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self._save_profile)
        buttons_layout.addWidget(self.save_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setProperty("cssClass", "danger")
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.clicked.connect(self._delete_profile)
        buttons_layout.addWidget(self.delete_button)

        profiles_layout.addLayout(buttons_layout)
        layout.addWidget(profiles_group)

        info_group = QGroupBox("О программе")
        info_layout = QVBoxLayout(info_group)

        info_layout.addWidget(QLabel("🏗️ Context Builder v1.0.0"))
        info_layout.addWidget(QLabel("Инструмент для сканирования и экспорта структуры проектов"))
        info_layout.addWidget(QLabel("Python 3.10+ | PySide6 | MIT License"))

        layout.addWidget(info_group)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(100)
        layout.addWidget(self.log)

        layout.addStretch()
        self._refresh_profiles()

    def _refresh_profiles(self):
        self.profile_list.clear()
        profiles = list_profiles()

        for p in profiles:
            self.profile_list.addItem(f"📋 {p}")

        self.log.append(f"Профилей: {len(profiles)}")

    def _save_profile(self):
        name = self.profile_name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название профиля")
            return

        settings = {
            "mode": "single",
            "root_path": "",
            "include_tree": True,
            "export_format": "txt",
            "output_dir": None,
        }

        path = save_profile(name, settings)
        self.log.append(f"✅ Профиль сохранён: {path}")
        self.profile_name_input.clear()
        self._refresh_profiles()

    def _delete_profile(self):
        current = self.profile_list.currentItem()

        if not current:
            QMessageBox.warning(self, "Ошибка", "Выберите профиль")
            return

        name = current.text().replace("📋 ", "")

        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить профиль '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            if delete_profile(name):
                self.log.append(f"✅ Профиль '{name}' удалён")
            else:
                self.log.append(f"❌ Профиль '{name}' не найден")

            self._refresh_profiles()