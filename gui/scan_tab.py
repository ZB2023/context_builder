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
)

from gui.widgets import DirectoryPicker, FileTreeWidget
from gui.workers import ScanWorker, ExportWorker


class ScanTab(QWidget):
    def __init__(self):
        super().__init__()
        self.scan_result = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("📁 Сканирование и запись")
        title.setObjectName("title")
        layout.addWidget(title)

        source_group = QGroupBox("Источник")
        source_layout = QVBoxLayout(source_group)

        self.dir_picker = DirectoryPicker("Путь к директории для сканирования...")
        source_layout.addWidget(self.dir_picker)

        self.scan_button = QPushButton("🔍 Сканировать")
        self.scan_button.clicked.connect(self._start_scan)
        source_layout.addWidget(self.scan_button)

        layout.addWidget(source_group)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        layout.addWidget(self.progress)

        self.tree = FileTreeWidget()
        self.tree.hide()
        layout.addWidget(self.tree)

        self.status_label = QLabel("")
        self.status_label.setObjectName("subtitle")
        layout.addWidget(self.status_label)

        export_group = QGroupBox("Экспорт")
        export_layout = QVBoxLayout(export_group)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Имя файла:"))
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Автоматическое имя с датой")
        name_layout.addWidget(self.filename_input)
        export_layout.addLayout(name_layout)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Формат:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["txt", "md", "json", "pdf"])
        format_layout.addWidget(self.format_combo)
        export_layout.addLayout(format_layout)

        self.output_picker = DirectoryPicker("Директория для сохранения (по умолчанию — сканируемая)...")
        export_layout.addWidget(self.output_picker)

        options_layout = QHBoxLayout()
        self.tree_check = QCheckBox("Включить дерево структуры")
        self.tree_check.setChecked(True)
        options_layout.addWidget(self.tree_check)

        self.redact_check = QCheckBox("Цензура данных")
        options_layout.addWidget(self.redact_check)
        export_layout.addLayout(options_layout)

        self.export_button = QPushButton("💾 Создать отчёт")
        self.export_button.setObjectName("success")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self._start_export)
        export_layout.addWidget(self.export_button)

        layout.addWidget(export_group)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(120)
        self.log.setPlaceholderText("Лог операций...")
        layout.addWidget(self.log)

    def _start_scan(self):
        path = self.dir_picker.get_path()

        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите путь к директории")
            return

        self.scan_button.setEnabled(False)
        self.progress.show()
        self.status_label.setText("Сканирование...")
        self.log.append(f"▶ Сканирование: {path}")

        self.worker = ScanWorker(path)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished_signal.connect(self._on_scan_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_progress(self, message):
        self.log.append(f"  {message}")

    def _on_scan_finished(self, result):
        self.scan_result = result
        self.progress.hide()
        self.scan_button.setEnabled(True)
        self.export_button.setEnabled(True)

        self.tree.load_scan_result(result)
        self.tree.show()

        files_count = len(result["files"])
        skipped_count = len(result["skipped"])
        errors_count = len(result["errors"])

        self.status_label.setText(
            f"✅ Файлов: {files_count} | Пропущено: {skipped_count} | Ошибок: {errors_count}"
        )
        self.status_label.setObjectName("status_success")
        self.status_label.setStyleSheet("color: #a6e3a1; font-weight: bold;")

        self.log.append(f"✅ Сканирование завершено: {files_count} файлов")

    def _on_error(self, error_message):
        self.progress.hide()
        self.scan_button.setEnabled(True)

        self.status_label.setText(f"❌ Ошибка: {error_message}")
        self.status_label.setObjectName("status_error")
        self.status_label.setStyleSheet("color: #f38ba8; font-weight: bold;")

        self.log.append(f"❌ Ошибка: {error_message}")

    def _start_export(self):
        if self.scan_result is None:
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
        self.log.append(f"▶ Экспорт: {filename}.{fmt}")

        self.export_worker = ExportWorker(
            self.scan_result, filename, fmt, output_dir, include_tree, redact, patterns
        )
        self.export_worker.finished_signal.connect(self._on_export_finished)
        self.export_worker.error.connect(self._on_error)
        self.export_worker.start()

    def _on_export_finished(self, output_path):
        self.export_button.setEnabled(True)
        self.log.append(f"✅ Отчёт создан: {output_path}")

        QMessageBox.information(self, "Готово", f"Отчёт создан:\n{output_path}")