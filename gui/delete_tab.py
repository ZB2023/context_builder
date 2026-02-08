from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QTextEdit,
    QMessageBox,
    QCheckBox,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
)
from PySide6.QtCore import Qt

from gui.widgets import DirectoryPicker


class DeleteTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("🗑️ Удаление записей")
        title.setObjectName("title")
        layout.addWidget(title)

        source_group = QGroupBox("Директория")
        source_layout = QVBoxLayout(source_group)

        self.dir_picker = DirectoryPicker("Директория с отчётами...")
        source_layout.addWidget(self.dir_picker)

        self.search_button = QPushButton("Найти отчёты")
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        source_layout.addWidget(self.search_button)

        layout.addWidget(source_group)

        files_group = QGroupBox("Найденные файлы")
        files_layout = QVBoxLayout(files_group)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        files_layout.addWidget(self.file_list)

        self.delete_session_check = QCheckBox("Также удалить данные сессии (.context_builder)")
        files_layout.addWidget(self.delete_session_check)

        self.delete_button = QPushButton("Удалить выбранные")
        self.delete_button.setProperty("cssClass", "danger")
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self._delete_files)
        files_layout.addWidget(self.delete_button)

        layout.addWidget(files_group)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(120)
        self.log.setPlaceholderText("Лог операций...")
        layout.addWidget(self.log)

        layout.addStretch()

    def _search_files(self):
        path = self.dir_picker.get_path()

        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите директорию")
            return

        from src.session import find_report_files

        files = find_report_files(path)
        self.file_list.clear()

        if not files:
            self.log.append(f"⚠ Отчёты не найдены: {path}")
            self.delete_button.setEnabled(False)
            return

        for f in files:
            size_kb = f.stat().st_size / 1024
            item = QListWidgetItem(f"📄 {f.name} ({size_kb:.1f} KB)")
            item.setData(256, f)
            self.file_list.addItem(item)

        self.delete_button.setEnabled(True)
        self.log.append(f"🔍 Найдено файлов: {len(files)}")

    def _delete_files(self):
        selected = self.file_list.selectedItems()

        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите файлы для удаления")
            return

        names = [item.data(256).name for item in selected]
        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить {len(names)} файлов?\n\n" + "\n".join(names),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        for item in selected:
            filepath = item.data(256)
            try:
                filepath.unlink()
                self.log.append(f"✅ Удалён: {filepath.name}")
            except OSError as e:
                self.log.append(f"❌ Ошибка: {filepath.name} — {e}")

        if self.delete_session_check.isChecked():
            path = self.dir_picker.get_path()
            session_dir = Path(path) / ".context_builder"
            if session_dir.exists():
                try:
                    for f in session_dir.iterdir():
                        f.unlink()
                    session_dir.rmdir()
                    self.log.append("✅ Сессия удалена")
                except OSError as e:
                    self.log.append(f"❌ Ошибка удаления сессии: {e}")

        self._search_files()