from datetime import datetime
from pathlib import Path

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
    QMessageBox,
    QFileDialog,
)

from gui.widgets import DirectoryPicker


class ConvertTab(QWidget):
    def __init__(self):
        super().__init__()
        self.session_data = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("🔄 Конвертация")
        title.setObjectName("title")
        layout.addWidget(title)

        source_group = QGroupBox("Источник")
        source_layout = QVBoxLayout(source_group)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Режим:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Из сессии", "Из PDF файла"])
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        source_layout.addLayout(mode_layout)

        self.session_picker = DirectoryPicker("Директория с сохранённой сессией...")
        source_layout.addWidget(self.session_picker)

        self.pdf_layout = QHBoxLayout()
        self.pdf_path_input = QLineEdit()
        self.pdf_path_input.setPlaceholderText("Путь к PDF файлу...")
        self.pdf_browse_button = QPushButton("Обзор")
        self.pdf_browse_button.setFixedWidth(100)
        self.pdf_browse_button.clicked.connect(self._browse_pdf)
        self.pdf_layout.addWidget(self.pdf_path_input)
        self.pdf_layout.addWidget(self.pdf_browse_button)

        self.pdf_widget = QWidget()
        self.pdf_widget.setLayout(self.pdf_layout)
        self.pdf_widget.hide()
        source_layout.addWidget(self.pdf_widget)

        self.load_button = QPushButton("📂 Загрузить")
        self.load_button.clicked.connect(self._load_source)
        source_layout.addWidget(self.load_button)

        self.source_info = QLabel("")
        self.source_info.setObjectName("subtitle")
        source_layout.addWidget(self.source_info)

        layout.addWidget(source_group)

        export_group = QGroupBox("Параметры конвертации")
        export_layout = QVBoxLayout(export_group)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Целевой формат:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["txt", "md", "json", "pdf"])
        format_layout.addWidget(self.format_combo)
        export_layout.addLayout(format_layout)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Имя файла:"))
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Автоматическое имя с датой")
        name_layout.addWidget(self.filename_input)
        export_layout.addLayout(name_layout)

        self.output_picker = DirectoryPicker("Директория для сохранения...")
        export_layout.addWidget(self.output_picker)

        self.tree_check = QCheckBox("Включить дерево структуры")
        self.tree_check.setChecked(True)
        export_layout.addWidget(self.tree_check)

        self.redact_check = QCheckBox("Цензура данных")
        export_layout.addWidget(self.redact_check)

        self.convert_button = QPushButton("🔄 Конвертировать")
        self.convert_button.setObjectName("success")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self._convert)
        export_layout.addWidget(self.convert_button)

        layout.addWidget(export_group)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(120)
        self.log.setPlaceholderText("Лог операций...")
        layout.addWidget(self.log)

        layout.addStretch()

    def _on_mode_changed(self, index):
        if index == 0:
            self.session_picker.setVisible(True)
            self.pdf_widget.hide()
        else:
            self.session_picker.setVisible(False)
            self.pdf_widget.show()

        self.convert_button.setEnabled(False)
        self.source_info.setText("")
        self.session_data = None

    def _browse_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите PDF файл", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.pdf_path_input.setText(file_path)

    def _load_source(self):
        if self.mode_combo.currentIndex() == 0:
            self._load_session()
        else:
            self._load_pdf()

    def _load_session(self):
        path = self.session_picker.get_path()

        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите директорию с сессией")
            return

        from src.session import load_session

        self.session_data = load_session(path)

        if self.session_data is None:
            self.source_info.setText("❌ Сессия не найдена")
            self.source_info.setStyleSheet("color: #f38ba8;")
            self.log.append(f"❌ Сессия не найдена: {path}")
            return

        files_count = len(self.session_data["scan_data"]["files"])
        created = self.session_data.get("created_at", "неизвестно")

        self.source_info.setText(f"✅ Загружена | Файлов: {files_count} | Создана: {created}")
        self.source_info.setStyleSheet("color: #a6e3a1;")
        self.convert_button.setEnabled(True)
        self.log.append(f"✅ Сессия загружена: {path}")

    def _load_pdf(self):
        path = self.pdf_path_input.text().strip()

        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите путь к PDF файлу")
            return

        pdf_file = Path(path)

        if not pdf_file.exists():
            self.source_info.setText("❌ Файл не найден")
            self.source_info.setStyleSheet("color: #f38ba8;")
            return

        if pdf_file.suffix.lower() != ".pdf":
            self.source_info.setText("❌ Это не PDF файл")
            self.source_info.setStyleSheet("color: #f38ba8;")
            return

        size_kb = pdf_file.stat().st_size / 1024
        self.source_info.setText(f"✅ PDF загружен | {pdf_file.name} | {size_kb:.1f} KB")
        self.source_info.setStyleSheet("color: #a6e3a1;")
        self.convert_button.setEnabled(True)
        self.log.append(f"✅ PDF загружен: {path}")

    def _convert(self):
        filename = self.filename_input.text().strip()
        if not filename:
            filename = f"convert_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        fmt = self.format_combo.currentText()

        if self.mode_combo.currentIndex() == 0:
            self._convert_from_session(filename, fmt)
        else:
            self._convert_from_pdf(filename, fmt)

    def _convert_from_session(self, filename, fmt):
        if self.session_data is None:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите сессию")
            return

        output_dir = self.output_picker.get_path() or self.session_picker.get_path()
        include_tree = self.tree_check.isChecked()
        redact = self.redact_check.isChecked()

        try:
            from src.exporter import export
            from src.session import save_session

            scan_data = self.session_data["scan_data"]

            if redact:
                from src.redactor import redact_scan_result, get_available_patterns
                patterns = get_available_patterns()
                scan_data, findings = redact_scan_result(scan_data, patterns)
                if findings:
                    self.log.append("⚠ Цензура применена")

            output_file = export(scan_data, filename, fmt, output_dir, include_tree)
            save_session(scan_data, output_dir, output_file)

            self.log.append(f"✅ Конвертация завершена: {output_file}")
            QMessageBox.information(self, "Готово", f"Файл создан:\n{output_file}")
        except Exception as e:
            self.log.append(f"❌ Ошибка: {e}")
            QMessageBox.critical(self, "Ошибка", str(e))

    def _convert_from_pdf(self, filename, fmt):
        pdf_path = self.pdf_path_input.text().strip()
        output_dir = self.output_picker.get_path() or str(Path(pdf_path).parent)

        if fmt == "pdf":
            QMessageBox.warning(self, "Ошибка", "Нельзя конвертировать PDF в PDF")
            return

        try:
            from src.converter import convert_pdf_to_format

            output_file = convert_pdf_to_format(pdf_path, filename, fmt, output_dir)

            if output_file:
                self.log.append(f"✅ PDF конвертирован: {output_file}")
                QMessageBox.information(self, "Готово", f"Файл создан:\n{output_file}")
            else:
                self.log.append("❌ Ошибка конвертации PDF")
                QMessageBox.critical(self, "Ошибка", "Не удалось конвертировать PDF")
        except Exception as e:
            self.log.append(f"❌ Ошибка: {e}")
            QMessageBox.critical(self, "Ошибка", str(e))