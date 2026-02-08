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
    QScrollArea,
    QSplitter,
)
from PySide6.QtCore import Qt

from gui.widgets import DirectoryPicker


class ConvertTab(QWidget):
    def __init__(self):
        super().__init__()
        self.session_data = None
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

        title = QLabel("Конвертация")
        title.setProperty("cssClass", "title")
        layout.addWidget(title)

        subtitle = QLabel("Конвертируйте отчёты между форматами или извлекайте текст из PDF")
        subtitle.setProperty("cssClass", "subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(4)

        source_group = QGroupBox("Источник")
        source_layout = QVBoxLayout(source_group)
        source_layout.setSpacing(8)
        source_layout.setContentsMargins(16, 16, 16, 16)

        mode_label = QLabel("Режим")
        mode_label.setProperty("cssClass", "field-label")
        source_layout.addWidget(mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Из сохранённой сессии", "Из PDF файла"])
        self.mode_combo.setToolTip("Сессия — структурированная конвертация, PDF — извлечение текста")
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        source_layout.addWidget(self.mode_combo)

        self.session_label = QLabel("Директория с сессией")
        self.session_label.setProperty("cssClass", "field-label")
        source_layout.addWidget(self.session_label)

        self.session_picker = DirectoryPicker("Папка с .context_builder...")
        source_layout.addWidget(self.session_picker)

        self.pdf_label = QLabel("PDF файл")
        self.pdf_label.setProperty("cssClass", "field-label")
        self.pdf_label.hide()
        source_layout.addWidget(self.pdf_label)

        self.pdf_row = QWidget()
        pdf_layout = QHBoxLayout(self.pdf_row)
        pdf_layout.setContentsMargins(0, 0, 0, 0)
        pdf_layout.setSpacing(8)

        self.pdf_path_input = QLineEdit()
        self.pdf_path_input.setPlaceholderText("Путь к PDF файлу...")
        pdf_layout.addWidget(self.pdf_path_input)

        self.pdf_browse = QPushButton("Обзор")
        self.pdf_browse.setProperty("cssClass", "secondary")
        self.pdf_browse.setMinimumWidth(80)
        self.pdf_browse.setMinimumHeight(34)
        self.pdf_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pdf_browse.clicked.connect(self._browse_pdf)
        pdf_layout.addWidget(self.pdf_browse)

        self.pdf_row.hide()
        source_layout.addWidget(self.pdf_row)

        source_layout.addSpacing(4)

        load_row = QHBoxLayout()
        load_row.addStretch()
        self.load_button = QPushButton("  Загрузить  ")
        self.load_button.setMinimumWidth(200)
        self.load_button.setMinimumHeight(36)
        self.load_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.load_button.clicked.connect(self._load_source)
        load_row.addWidget(self.load_button)
        load_row.addStretch()
        source_layout.addLayout(load_row)

        self.source_info = QLabel("")
        self.source_info.setProperty("cssClass", "subtitle")
        source_layout.addWidget(self.source_info)

        layout.addWidget(source_group)

        params_group = QGroupBox("Параметры")
        params_layout = QVBoxLayout(params_group)
        params_layout.setSpacing(10)
        params_layout.setContentsMargins(16, 16, 16, 16)

        row1 = QHBoxLayout()
        row1.setSpacing(16)

        name_col = QVBoxLayout()
        name_col.setSpacing(4)
        nl = QLabel("Имя файла")
        nl.setProperty("cssClass", "field-label")
        name_col.addWidget(nl)
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Автоматическое имя с датой")
        name_col.addWidget(self.filename_input)
        row1.addLayout(name_col, 3)

        fmt_col = QVBoxLayout()
        fmt_col.setSpacing(4)
        fl = QLabel("Целевой формат")
        fl.setProperty("cssClass", "field-label")
        fmt_col.addWidget(fl)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["txt", "md", "json", "pdf"])
        fmt_col.addWidget(self.format_combo)
        row1.addLayout(fmt_col, 1)

        params_layout.addLayout(row1)

        sl = QLabel("Сохранить в")
        sl.setProperty("cssClass", "field-label")
        params_layout.addWidget(sl)

        self.output_picker = DirectoryPicker("По умолчанию — рядом с источником")
        params_layout.addWidget(self.output_picker)

        params_layout.addSpacing(4)

        opts = QHBoxLayout()
        opts.setSpacing(24)
        self.tree_check = QCheckBox("Дерево структуры")
        self.tree_check.setChecked(True)
        opts.addWidget(self.tree_check)
        self.redact_check = QCheckBox("Цензура данных")
        opts.addWidget(self.redact_check)
        opts.addStretch()
        params_layout.addLayout(opts)

        params_layout.addSpacing(4)

        convert_row = QHBoxLayout()
        convert_row.addStretch()
        self.convert_button = QPushButton("  Конвертировать  ")
        self.convert_button.setProperty("cssClass", "success")
        self.convert_button.setMinimumWidth(200)
        self.convert_button.setMinimumHeight(36)
        self.convert_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self._convert)
        convert_row.addWidget(self.convert_button)
        convert_row.addStretch()
        params_layout.addLayout(convert_row)

        layout.addWidget(params_group)
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

    def _on_mode_changed(self, index):
        is_session = index == 0
        self.session_label.setVisible(is_session)
        self.session_picker.setVisible(is_session)
        self.pdf_label.setVisible(not is_session)
        self.pdf_row.setVisible(not is_session)
        self.convert_button.setEnabled(False)
        self.source_info.setText("")
        self.session_data = None

    def _browse_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "PDF файл", "", "PDF (*.pdf)")
        if path:
            self.pdf_path_input.setText(path)

    def _load_source(self):
        if self.mode_combo.currentIndex() == 0:
            self._load_session()
        else:
            self._load_pdf()

    def _load_session(self):
        path = self.session_picker.get_path()
        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите директорию")
            return

        from src.session import load_session

        self.session_data = load_session(path)
        if not self.session_data:
            self.source_info.setText("Сессия не найдена")
            self.source_info.setProperty("cssClass", "error")
            self.source_info.style().unpolish(self.source_info)
            self.source_info.style().polish(self.source_info)
            self.log.append(f"✗ Сессия не найдена: {path}")
            return

        n = len(self.session_data["scan_data"]["files"])
        self.source_info.setText(f"✓ Загружено: {n} файлов")
        self.source_info.setProperty("cssClass", "success")
        self.source_info.style().unpolish(self.source_info)
        self.source_info.style().polish(self.source_info)
        self.convert_button.setEnabled(True)
        self.log.append(f"✓ Сессия: {path}")

    def _load_pdf(self):
        path = self.pdf_path_input.text().strip()
        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите PDF файл")
            return

        pf = Path(path)
        if not pf.exists() or pf.suffix.lower() != ".pdf":
            self.source_info.setText("Файл не найден или не PDF")
            self.source_info.setProperty("cssClass", "error")
            self.source_info.style().unpolish(self.source_info)
            self.source_info.style().polish(self.source_info)
            return

        kb = pf.stat().st_size / 1024
        self.source_info.setText(f"✓ PDF: {pf.name} ({kb:.1f} KB)")
        self.source_info.setProperty("cssClass", "success")
        self.source_info.style().unpolish(self.source_info)
        self.source_info.style().polish(self.source_info)
        self.convert_button.setEnabled(True)
        self.log.append(f"✓ PDF: {path}")

    def _convert(self):
        filename = self.filename_input.text().strip()
        if not filename:
            filename = f"convert_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        fmt = self.format_combo.currentText()
        if self.mode_combo.currentIndex() == 0:
            self._convert_session(filename, fmt)
        else:
            self._convert_pdf(filename, fmt)

    def _convert_session(self, filename, fmt):
        if not self.session_data:
            return

        output_dir = self.output_picker.get_path() or self.session_picker.get_path()
        tree = self.tree_check.isChecked()
        redact = self.redact_check.isChecked()

        try:
            from src.exporter import export
            from src.session import save_session

            data = self.session_data["scan_data"]
            if redact:
                from src.redactor import redact_scan_result, get_available_patterns
                data, _ = redact_scan_result(data, get_available_patterns())

            out = export(data, filename, fmt, output_dir, tree)
            save_session(data, output_dir, out)
            self.log.append(f"✓ {out}")
            QMessageBox.information(self, "Готово", f"Создан:\n{out}")
        except Exception as e:
            self.log.append(f"✗ {e}")
            QMessageBox.critical(self, "Ошибка", str(e))

    def _convert_pdf(self, filename, fmt):
        path = self.pdf_path_input.text().strip()
        output_dir = self.output_picker.get_path() or str(Path(path).parent)
        if fmt == "pdf":
            QMessageBox.warning(self, "Ошибка", "PDF → PDF невозможно")
            return

        try:
            from src.converter import convert_pdf_to_format

            out = convert_pdf_to_format(path, filename, fmt, output_dir)
            if out:
                self.log.append(f"✓ {out}")
                QMessageBox.information(self, "Готово", f"Создан:\n{out}")
            else:
                self.log.append("✗ Ошибка конвертации")
        except Exception as e:
            self.log.append(f"✗ {e}")
            QMessageBox.critical(self, "Ошибка", str(e))