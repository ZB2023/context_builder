from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QTextEdit,
    QMessageBox,
    QCheckBox,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QScrollArea,
    QSplitter,
)
from PySide6.QtCore import Qt

from gui.widgets import DirectoryPicker


class DeleteTab(QWidget):
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

        title = QLabel("Удаление записей")
        title.setProperty("cssClass", "title")
        layout.addWidget(title)

        subtitle = QLabel("Найдите и удалите ненужные отчёты и данные сессий")
        subtitle.setProperty("cssClass", "subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(4)

        source_group = QGroupBox("Директория")
        source_layout = QVBoxLayout(source_group)
        source_layout.setSpacing(8)
        source_layout.setContentsMargins(16, 16, 16, 16)

        dl = QLabel("Папка с отчётами")
        dl.setProperty("cssClass", "field-label")
        source_layout.addWidget(dl)

        self.dir_picker = DirectoryPicker("Укажите папку с отчётами...")
        source_layout.addWidget(self.dir_picker)

        source_layout.addSpacing(4)

        sr = QHBoxLayout()
        sr.addStretch()
        self.search_button = QPushButton("  Найти отчёты  ")
        self.search_button.setMinimumWidth(200)
        self.search_button.setMinimumHeight(36)
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_button.clicked.connect(self._search_files)
        sr.addWidget(self.search_button)
        sr.addStretch()
        source_layout.addLayout(sr)

        layout.addWidget(source_group)

        files_group = QGroupBox("Найденные файлы")
        files_layout = QVBoxLayout(files_group)
        files_layout.setSpacing(8)
        files_layout.setContentsMargins(16, 16, 16, 16)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.file_list.setMinimumHeight(100)
        self.file_list.setMaximumHeight(220)
        files_layout.addWidget(self.file_list)

        self.delete_session_check = QCheckBox("Удалить данные сессии (.context_builder)")
        self.delete_session_check.setToolTip("Удалит также внутренний JSON-слепок проекта")
        files_layout.addWidget(self.delete_session_check)

        files_layout.addSpacing(4)

        dr = QHBoxLayout()
        dr.addStretch()
        self.delete_button = QPushButton("  Удалить выбранные  ")
        self.delete_button.setProperty("cssClass", "danger")
        self.delete_button.setMinimumWidth(200)
        self.delete_button.setMinimumHeight(36)
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self._delete_files)
        dr.addWidget(self.delete_button)
        dr.addStretch()
        files_layout.addLayout(dr)

        layout.addWidget(files_group)
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

    def _search_files(self):
        path = self.dir_picker.get_path()
        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите директорию")
            return

        from src.session import find_report_files

        files = find_report_files(path)
        self.file_list.clear()

        if not files:
            self.log.append(f"Отчёты не найдены: {path}")
            self.delete_button.setEnabled(False)
            return

        for f in files:
            kb = f.stat().st_size / 1024
            item = QListWidgetItem(f"{f.name}  ({kb:.1f} KB)")
            item.setData(256, f)
            self.file_list.addItem(item)

        self.delete_button.setEnabled(True)
        self.log.append(f"Найдено: {len(files)} файлов")

    def _delete_files(self):
        selected = self.file_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите файлы")
            return

        names = [i.data(256).name for i in selected]
        r = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить {len(names)} файлов?\n\n" + "\n".join(names),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if r != QMessageBox.StandardButton.Yes:
            return

        for item in selected:
            fp = item.data(256)
            try:
                fp.unlink()
                self.log.append(f"✓ {fp.name}")
            except OSError as e:
                self.log.append(f"✗ {fp.name}: {e}")

        if self.delete_session_check.isChecked():
            path = self.dir_picker.get_path()
            sd = Path(path) / ".context_builder"
            if sd.exists():
                try:
                    for f in sd.iterdir():
                        f.unlink()
                    sd.rmdir()
                    self.log.append("✓ Сессия удалена")
                except OSError as e:
                    self.log.append(f"✗ Сессия: {e}")

        self._search_files()