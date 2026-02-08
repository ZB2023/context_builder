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
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
)

from gui.widgets import DirectoryPicker


class FilesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.all_files = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("🔍 Выбор файлов")
        title.setObjectName("title")
        layout.addWidget(title)

        source_group = QGroupBox("Источник")
        source_layout = QVBoxLayout(source_group)

        self.dir_picker = DirectoryPicker("Директория для поиска файлов...")
        source_layout.addWidget(self.dir_picker)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Фильтр:"))
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Расширения: .py, .js или часть имени")
        filter_layout.addWidget(self.filter_input)

        self.search_button = QPushButton("🔍 Найти")
        self.search_button.clicked.connect(self._search_files)
        filter_layout.addWidget(self.search_button)
        source_layout.addLayout(filter_layout)

        layout.addWidget(source_group)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        layout.addWidget(self.file_list)

        self.count_label = QLabel("")
        self.count_label.setObjectName("subtitle")
        layout.addWidget(self.count_label)

        export_group = QGroupBox("Экспорт выбранных")
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

        self.output_picker = DirectoryPicker("Директория для сохранения...")
        export_layout.addWidget(self.output_picker)

        self.tree_check = QCheckBox("Включить дерево структуры")
        self.tree_check.setChecked(True)
        export_layout.addWidget(self.tree_check)

        self.export_button = QPushButton("💾 Создать отчёт")
        self.export_button.setObjectName("success")
        self.export_button.clicked.connect(self._export)
        export_layout.addWidget(self.export_button)

        layout.addWidget(export_group)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(100)
        layout.addWidget(self.log)

    def _search_files(self):
        path = self.dir_picker.get_path()

        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите директорию")
            return

        from src.scanner import collect_text_files, filter_by_extensions, filter_by_name

        self.all_files = collect_text_files(path)
        filter_text = self.filter_input.text().strip()

        if filter_text:
            if "." in filter_text:
                extensions = [e.strip() for e in filter_text.split(",")]
                filtered = filter_by_extensions(self.all_files, extensions)
            else:
                filtered = filter_by_name(self.all_files, filter_text)
        else:
            filtered = self.all_files

        self.file_list.clear()

        for f in filtered:
            try:
                relative = f.relative_to(path)
            except ValueError:
                relative = f.name

            item = QListWidgetItem(f"📄 {relative}")
            item.setData(256, f)
            self.file_list.addItem(item)

        self.count_label.setText(f"Найдено: {len(filtered)} файлов")
        self.log.append(f"🔍 Поиск в {path}: {len(filtered)} файлов")

    def _export(self):
        selected = self.file_list.selectedItems()

        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите файлы")
            return

        files = [item.data(256) for item in selected]
        root_path = self.dir_picker.get_path()

        filename = self.filename_input.text().strip()
        if not filename:
            filename = f"files_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        fmt = self.format_combo.currentText()
        output_dir = self.output_picker.get_path() or root_path
        include_tree = self.tree_check.isChecked()

        try:
            from src.scanner import scan_selected_files
            from src.exporter import export
            from src.session import save_session

            scan_result = scan_selected_files(files, root_path)
            output_file = export(scan_result, filename, fmt, output_dir, include_tree)
            save_session(scan_result, report_path=output_file)

            self.log.append(f"✅ Отчёт создан: {output_file}")
            QMessageBox.information(self, "Готово", f"Отчёт создан:\n{output_file}")
        except Exception as e:
            self.log.append(f"❌ Ошибка: {e}")
            QMessageBox.critical(self, "Ошибка", str(e))