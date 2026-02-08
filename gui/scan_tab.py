from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QPushButton,
    QGroupBox,
    QTextEdit,
    QProgressBar,
    QMessageBox,
    QSplitter,
    QScrollArea,
)
from PySide6.QtCore import Qt

from gui.widgets import DirectoryPicker, FileTreeWidget
from gui.workers import ScanWorker, ExportWorker


class ScanTab(QWidget):
    def __init__(self):
        super().__init__()
        self.scan_result = None
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

        title = QLabel("Сканирование и запись")
        title.setProperty("cssClass", "title")
        layout.addWidget(title)

        subtitle = QLabel("Выберите директорию для анализа структуры проекта")
        subtitle.setProperty("cssClass", "subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(4)

        source_group = QGroupBox("Источник")
        source_layout = QVBoxLayout(source_group)
        source_layout.setSpacing(8)
        source_layout.setContentsMargins(16, 16, 16, 16)

        dir_label = QLabel("Директория")
        dir_label.setProperty("cssClass", "field-label")
        source_layout.addWidget(dir_label)

        self.dir_picker = DirectoryPicker("Укажите путь к папке проекта...")
        source_layout.addWidget(self.dir_picker)

        source_layout.addSpacing(4)

        scan_row = QHBoxLayout()
        scan_row.addStretch()
        self.scan_button = QPushButton("  Сканировать  ")
        self.scan_button.setMinimumWidth(200)
        self.scan_button.setMinimumHeight(36)
        self.scan_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_button.setToolTip("Запустить сканирование выбранной директории")
        self.scan_button.clicked.connect(self._start_scan)
        scan_row.addWidget(self.scan_button)
        scan_row.addStretch()
        source_layout.addLayout(scan_row)

        layout.addWidget(source_group)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setFixedHeight(4)
        self.progress.hide()
        layout.addWidget(self.progress)

        self.status_label = QLabel("")
        self.status_label.setProperty("cssClass", "subtitle")
        layout.addWidget(self.status_label)

        self.tree = FileTreeWidget()
        self.tree.hide()
        self.tree.setMinimumHeight(140)
        self.tree.setMaximumHeight(280)
        layout.addWidget(self.tree)

        export_group = QGroupBox("Экспорт")
        export_layout = QVBoxLayout(export_group)
        export_layout.setSpacing(10)
        export_layout.setContentsMargins(16, 16, 16, 16)

        row1 = QHBoxLayout()
        row1.setSpacing(16)

        name_col = QVBoxLayout()
        name_col.setSpacing(4)
        name_label = QLabel("Имя файла")
        name_label.setProperty("cssClass", "field-label")
        name_col.addWidget(name_label)
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Автоматическое имя с датой")
        self.filename_input.setToolTip("Оставьте пустым для автогенерации")
        name_col.addWidget(self.filename_input)
        row1.addLayout(name_col, 3)

        format_col = QVBoxLayout()
        format_col.setSpacing(4)
        format_label = QLabel("Формат")
        format_label.setProperty("cssClass", "field-label")
        format_col.addWidget(format_label)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["txt", "md", "json", "pdf"])
        self.format_combo.setToolTip("TXT — текст, MD — Markdown, JSON — данные, PDF — документ")
        format_col.addWidget(self.format_combo)
        row1.addLayout(format_col, 1)

        export_layout.addLayout(row1)

        save_label = QLabel("Сохранить в")
        save_label.setProperty("cssClass", "field-label")
        export_layout.addWidget(save_label)

        self.output_picker = DirectoryPicker("По умолчанию — в сканируемую директорию")
        export_layout.addWidget(self.output_picker)

        export_layout.addSpacing(4)

        options_layout = QHBoxLayout()
        options_layout.setSpacing(24)
        self.tree_check = QCheckBox("Дерево структуры")
        self.tree_check.setChecked(True)
        self.tree_check.setToolTip("Добавить визуализацию дерева папок в отчёт")
        options_layout.addWidget(self.tree_check)
        self.redact_check = QCheckBox("Цензура данных")
        self.redact_check.setToolTip("Заменить пароли, ключи, email на ***REDACTED***")
        options_layout.addWidget(self.redact_check)
        options_layout.addStretch()
        export_layout.addLayout(options_layout)

        export_layout.addSpacing(4)

        export_row = QHBoxLayout()
        export_row.addStretch()
        self.export_button = QPushButton("  Создать отчёт  ")
        self.export_button.setProperty("cssClass", "success")
        self.export_button.setMinimumWidth(200)
        self.export_button.setMinimumHeight(36)
        self.export_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_button.setEnabled(False)
        self.export_button.setToolTip("Сначала выполните сканирование")
        self.export_button.clicked.connect(self._start_export)
        export_row.addWidget(self.export_button)
        export_row.addStretch()
        export_layout.addLayout(export_row)

        layout.addWidget(export_group)
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
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(16, 8, 16, 8)
        log_layout.setSpacing(4)

        log_header = QHBoxLayout()
        log_label = QLabel("Лог")
        log_label.setProperty("cssClass", "field-label")
        log_header.addWidget(log_label)
        log_header.addStretch()
        self.clear_log_button = QPushButton("Очистить")
        self.clear_log_button.setProperty("cssClass", "secondary")
        self.clear_log_button.setFixedHeight(24)
        self.clear_log_button.setMaximumWidth(90)
        self.clear_log_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_log_button.clicked.connect(lambda: self.log.clear())
        log_header.addWidget(self.clear_log_button)
        log_layout.addLayout(log_header)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Результаты операций появятся здесь...")
        log_layout.addWidget(self.log)

        splitter.addWidget(log_widget)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([600, 120])

        outer.addWidget(splitter)

    def _start_scan(self):
        path = self.dir_picker.get_path()
        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите путь к директории")
            return

        self.scan_button.setEnabled(False)
        self.progress.show()
        self.status_label.setText("Сканирование...")
        self.log.append(f"▶ {path}")

        self.worker = ScanWorker(path)
        self.worker.progress.connect(lambda m: self.log.append(f"  {m}"))
        self.worker.finished_signal.connect(self._on_scan_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_scan_finished(self, result):
        self.scan_result = result
        self.progress.hide()
        self.scan_button.setEnabled(True)
        self.export_button.setEnabled(True)
        self.export_button.setToolTip("Создать отчёт")

        self.tree.load_scan_result(result)
        self.tree.show()

        f = len(result["files"])
        s = len(result["skipped"])
        e = len(result["errors"])
        self.status_label.setText(f"Файлов: {f}  ·  Пропущено: {s}  ·  Ошибок: {e}")
        self.status_label.setProperty("cssClass", "success")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.log.append(f"✓ {f} файлов")

    def _on_error(self, msg):
        self.progress.hide()
        self.scan_button.setEnabled(True)
        self.status_label.setText(f"Ошибка: {msg}")
        self.status_label.setProperty("cssClass", "error")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.log.append(f"✗ {msg}")

    def _start_export(self):
        if not self.scan_result:
            QMessageBox.warning(self, "Ошибка", "Сначала выполните сканирование")
            return

        filename = self.filename_input.text().strip()
        if not filename:
            filename = f"scan_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        fmt = self.format_combo.currentText()
        output_dir = self.output_picker.get_path() or self.scan_result["root"]
        include_tree = self.tree_check.isChecked()
        redact = self.redact_check.isChecked()

        patterns = None
        if redact:
            from src.redactor import get_available_patterns
            patterns = get_available_patterns()

        self.export_button.setEnabled(False)
        self.log.append(f"▶ {filename}.{fmt}")

        self.export_worker = ExportWorker(
            self.scan_result, filename, fmt, output_dir, include_tree, redact, patterns
        )
        self.export_worker.finished_signal.connect(self._on_export_finished)
        self.export_worker.error.connect(self._on_error)
        self.export_worker.start()

    def _on_export_finished(self, path):
        self.export_button.setEnabled(True)
        self.log.append(f"✓ {path}")
        QMessageBox.information(self, "Готово", f"Отчёт создан:\n{path}")