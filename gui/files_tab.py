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
    QScrollArea,
    QSplitter,
)
from PySide6.QtCore import Qt

from gui.widgets import DirectoryPicker


class FilesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.all_files = []
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

        title = QLabel("Выбор файлов")
        title.setProperty("cssClass", "title")
        layout.addWidget(title)

        subtitle = QLabel("Выберите конкретные файлы для включения в отчёт")
        subtitle.setProperty("cssClass", "subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(4)

        source_group = QGroupBox("Поиск")
        source_layout = QVBoxLayout(source_group)
        source_layout.setSpacing(8)
        source_layout.setContentsMargins(16, 16, 16, 16)

        dl = QLabel("Директория")
        dl.setProperty("cssClass", "field-label")
        source_layout.addWidget(dl)

        self.dir_picker = DirectoryPicker("Папка для поиска файлов...")
        source_layout.addWidget(self.dir_picker)

        fl = QLabel("Фильтр")
        fl.setProperty("cssClass", "field-label")
        source_layout.addWidget(fl)

        filter_row = QHBoxLayout()
        filter_row.setSpacing(8)
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Расширения (.py, .js) или часть имени")
        self.filter_input.setToolTip("Введите расширения через запятую или часть имени файла")
        filter_row.addWidget(self.filter_input)

        self.search_button = QPushButton("  Найти  ")
        self.search_button.setMinimumWidth(100)
        self.search_button.setMinimumHeight(34)
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_button.clicked.connect(self._search_files)
        filter_row.addWidget(self.search_button)
        source_layout.addLayout(filter_row)

        layout.addWidget(source_group)

        self.count_label = QLabel("")
        self.count_label.setProperty("cssClass", "subtitle")
        layout.addWidget(self.count_label)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.file_list.setMinimumHeight(100)
        self.file_list.setMaximumHeight(220)
        layout.addWidget(self.file_list)

        export_group = QGroupBox("Экспорт выбранных")
        export_layout = QVBoxLayout(export_group)
        export_layout.setSpacing(10)
        export_layout.setContentsMargins(16, 16, 16, 16)

        row1 = QHBoxLayout()
        row1.setSpacing(16)

        nc = QVBoxLayout()
        nc.setSpacing(4)
        nl = QLabel("Имя файла")
        nl.setProperty("cssClass", "field-label")
        nc.addWidget(nl)
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Автоматическое имя")
        nc.addWidget(self.filename_input)
        row1.addLayout(nc, 3)

        fc = QVBoxLayout()
        fc.setSpacing(4)
        ffl = QLabel("Формат")
        ffl.setProperty("cssClass", "field-label")
        fc.addWidget(ffl)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["txt", "md", "json", "pdf"])
        fc.addWidget(self.format_combo)
        row1.addLayout(fc, 1)

        export_layout.addLayout(row1)

        sl = QLabel("Сохранить в")
        sl.setProperty("cssClass", "field-label")
        export_layout.addWidget(sl)

        self.output_picker = DirectoryPicker("По умолчанию — исходная директория")
        export_layout.addWidget(self.output_picker)

        export_layout.addSpacing(4)

        self.tree_check = QCheckBox("Дерево структуры")
        self.tree_check.setChecked(True)
        export_layout.addWidget(self.tree_check)

        export_layout.addSpacing(4)

        er = QHBoxLayout()
        er.addStretch()
        self.export_button = QPushButton("  Создать отчёт  ")
        self.export_button.setProperty("cssClass", "success")
        self.export_button.setMinimumWidth(200)
        self.export_button.setMinimumHeight(36)
        self.export_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_button.clicked.connect(self._export)
        er.addWidget(self.export_button)
        er.addStretch()
        export_layout.addLayout(er)

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

        from src.scanner import collect_all_files, filter_by_extensions, filter_by_name

        self.all_files = collect_all_files(path)

        ft = self.filter_input.text().strip()
        if ft:
            if "." in ft:
                exts = [e.strip() for e in ft.split(",")]
                filtered = filter_by_extensions(self.all_files, exts)
            else:
                filtered = filter_by_name(self.all_files, ft)
        else:
            filtered = self.all_files

        self.file_list.clear()
        for f in filtered:
            try:
                rel = f.relative_to(path)
            except ValueError:
                rel = f.name
            item = QListWidgetItem(str(rel))
            item.setData(256, f)
            self.file_list.addItem(item)

        self.count_label.setText(f"Найдено: {len(filtered)} файлов")
        self.log.append(f"Поиск в {path}: {len(filtered)}")

    def _export(self):
        selected = self.file_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите файлы")
            return

        files = [i.data(256) for i in selected]
        root = self.dir_picker.get_path()
        filename = self.filename_input.text().strip()
        if not filename:
            filename = f"files_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        fmt = self.format_combo.currentText()
        output_dir = self.output_picker.get_path() or root
        tree = self.tree_check.isChecked()

        try:
            from src.scanner import scan_selected_files
            from src.exporter import export
            from src.session import save_session

            result = scan_selected_files(files, root)
            out = export(result, filename, fmt, output_dir, tree)
            save_session(result, report_path=out)
            self.log.append(f"✓ {out}")
            QMessageBox.information(self, "Готово", f"Создан:\n{out}")
        except Exception as e:
            self.log.append(f"✗ {e}")
            QMessageBox.critical(self, "Ошибка", str(e))