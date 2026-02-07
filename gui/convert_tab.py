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
    QMessageBox,
)

from gui.widgets import DirectoryPicker


class ConvertTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("🔄 Конвертация")
        title.setObjectName("title")
        layout.addWidget(title)

        source_group = QGroupBox("Источник сессии")
        source_layout = QVBoxLayout(source_group)

        self.session_picker = DirectoryPicker("Директория с сохранённой сессией...")
        source_layout.addWidget(self.session_picker)

        self.load_button = QPushButton("📂 Загрузить сессию")
        self.load_button.clicked.connect(self._load_session)
        source_layout.addWidget(self.load_button)

        self.session_info = QLabel("")
        self.session_info.setObjectName("subtitle")
        source_layout.addWidget(self.session_info)

        layout.addWidget(source_group)

        export_group = QGroupBox("Параметры конвертации")
        export_layout = QVBoxLayout(export_group)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Целевой формат:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["txt", "md", "json"])
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

    def _load_session(self):
        path = self.session_picker.get_path()

        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите директорию с сессией")
            return

        from src.session import load_session

        self.session_data = load_session(path)

        if self.session_data is None:
            self.session_info.setText("❌ Сессия не найдена")
            self.session_info.setStyleSheet("color: #f38ba8;")
            self.log.append(f"❌ Сессия не найдена: {path}")
            return

        files_count = len(self.session_data["scan_data"]["files"])
        created = self.session_data.get("created_at", "неизвестно")

        self.session_info.setText(f"✅ Загружена | Файлов: {files_count} | Создана: {created}")
        self.session_info.setStyleSheet("color: #a6e3a1;")
        self.convert_button.setEnabled(True)
        self.log.append(f"✅ Сессия загружена: {path}")

    def _convert(self):
        if not hasattr(self, "session_data") or self.session_data is None:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите сессию")
            return

        filename = self.filename_input.text().strip()
        if not filename:
            filename = f"convert_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        fmt = self.format_combo.currentText()
        output_dir = self.output_picker.get_path() or self.session_picker.get_path()
        include_tree = self.tree_check.isChecked()

        try:
            from src.exporter import export
            from src.session import save_session

            scan_data = self.session_data["scan_data"]
            output_file = export(scan_data, filename, fmt, output_dir, include_tree)
            save_session(scan_data, output_dir, output_file)

            self.log.append(f"✅ Конвертация завершена: {output_file}")
            QMessageBox.information(self, "Готово", f"Файл создан:\n{output_file}")
        except Exception as e:
            self.log.append(f"❌ Ошибка: {e}")
            QMessageBox.critical(self, "Ошибка", str(e))