MAIN_STYLE = """
QMainWindow {
    background-color: #1e1e2e;
}

QTabWidget::pane {
    border: 1px solid #313244;
    background-color: #1e1e2e;
    border-radius: 8px;
}

QTabBar::tab {
    background-color: #313244;
    color: #cdd6f4;
    padding: 10px 20px;
    margin: 2px;
    border-radius: 6px;
    font-size: 13px;
}

QTabBar::tab:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
    font-weight: bold;
}

QTabBar::tab:hover {
    background-color: #45475a;
}

QPushButton {
    background-color: #89b4fa;
    color: #1e1e2e;
    border: none;
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #74c7ec;
}

QPushButton:pressed {
    background-color: #585b70;
}

QPushButton:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QPushButton#danger {
    background-color: #f38ba8;
}

QPushButton#danger:hover {
    background-color: #eba0ac;
}

QPushButton#success {
    background-color: #a6e3a1;
}

QPushButton#success:hover {
    background-color: #94e2d5;
}

QLabel {
    color: #cdd6f4;
    font-size: 13px;
}

QLabel#title {
    font-size: 18px;
    font-weight: bold;
    color: #89b4fa;
}

QLabel#subtitle {
    font-size: 12px;
    color: #6c7086;
}

QLabel#status_success {
    color: #a6e3a1;
    font-weight: bold;
}

QLabel#status_error {
    color: #f38ba8;
    font-weight: bold;
}

QLineEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 13px;
}

QLineEdit:focus {
    border-color: #89b4fa;
}

QComboBox {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 13px;
}

QComboBox:hover {
    border-color: #89b4fa;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #313244;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
    border-radius: 4px;
}

QCheckBox {
    color: #cdd6f4;
    font-size: 13px;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #45475a;
    background-color: #313244;
}

QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}

QTreeWidget {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 4px;
    font-size: 13px;
}

QTreeWidget::item {
    padding: 4px;
}

QTreeWidget::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
    border-radius: 4px;
}

QTreeWidget::item:hover {
    background-color: #45475a;
}

QHeaderView::section {
    background-color: #313244;
    color: #cdd6f4;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QTextEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 8px;
    font-family: Consolas, monospace;
    font-size: 12px;
}

QProgressBar {
    background-color: #313244;
    border: none;
    border-radius: 8px;
    height: 20px;
    text-align: center;
    color: #cdd6f4;
    font-size: 11px;
}

QProgressBar::chunk {
    background-color: #89b4fa;
    border-radius: 8px;
}

QScrollBar:vertical {
    background-color: #1e1e2e;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #45475a;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #585b70;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QGroupBox {
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-size: 13px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}
"""