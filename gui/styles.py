DARK_THEME = {
    "name": "dark",
    "bg_primary": "#1e1e2e",
    "bg_secondary": "#313244",
    "bg_tertiary": "#45475a",
    "bg_hover": "#585b70",
    "accent": "#89b4fa",
    "accent_hover": "#74c7ec",
    "accent_pressed": "#b4befe",
    "success": "#a6e3a1",
    "success_hover": "#94e2d5",
    "danger": "#f38ba8",
    "danger_hover": "#eba0ac",
    "warning": "#f9e2af",
    "text_primary": "#cdd6f4",
    "text_secondary": "#a6adc8",
    "text_dim": "#6c7086",
    "border": "#45475a",
    "border_focus": "#89b4fa",
    "scrollbar": "#45475a",
    "scrollbar_hover": "#585b70",
    "selection": "#89b4fa",
    "selection_text": "#1e1e2e",
    "header_bg": "#313244",
    "code_bg": "#181825",
}

LIGHT_THEME = {
    "name": "light",
    "bg_primary": "#eff1f5",
    "bg_secondary": "#e6e9ef",
    "bg_tertiary": "#ccd0da",
    "bg_hover": "#bcc0cc",
    "accent": "#1e66f5",
    "accent_hover": "#2a6ef5",
    "accent_pressed": "#1252d9",
    "success": "#40a02b",
    "success_hover": "#36922a",
    "danger": "#d20f39",
    "danger_hover": "#b80d33",
    "warning": "#df8e1d",
    "text_primary": "#4c4f69",
    "text_secondary": "#5c5f77",
    "text_dim": "#8c8fa1",
    "border": "#ccd0da",
    "border_focus": "#1e66f5",
    "scrollbar": "#ccd0da",
    "scrollbar_hover": "#bcc0cc",
    "selection": "#1e66f5",
    "selection_text": "#eff1f5",
    "header_bg": "#e6e9ef",
    "code_bg": "#dce0e8",
}


def generate_stylesheet(theme):
    t = theme
    return f"""
QMainWindow {{
    background-color: {t['bg_primary']};
}}

QWidget {{
    background-color: {t['bg_primary']};
    color: {t['text_primary']};
    font-family: "Segoe UI", "Arial", sans-serif;
    font-size: 13px;
}}

QTabWidget::pane {{
    border: 1px solid {t['border']};
    background-color: {t['bg_primary']};
    border-radius: 8px;
    top: -1px;
}}

QTabBar::tab {{
    background-color: {t['bg_secondary']};
    color: {t['text_secondary']};
    padding: 10px 20px;
    margin: 2px 1px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: 1px solid {t['border']};
    border-bottom: none;
    font-size: 13px;
    min-width: 120px;
}}

QTabBar::tab:selected {{
    background-color: {t['accent']};
    color: {t['selection_text']};
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: {t['bg_tertiary']};
    color: {t['text_primary']};
}}

QPushButton {{
    background-color: {t['accent']};
    color: {t['selection_text']};
    border: none;
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: bold;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {t['accent_hover']};
}}

QPushButton:pressed {{
    background-color: {t['accent_pressed']};
}}

QPushButton:disabled {{
    background-color: {t['bg_tertiary']};
    color: {t['text_dim']};
}}

QPushButton[cssClass="danger"] {{
    background-color: {t['danger']};
    color: {t['selection_text']};
}}

QPushButton[cssClass="danger"]:hover {{
    background-color: {t['danger_hover']};
}}

QPushButton[cssClass="success"] {{
    background-color: {t['success']};
    color: {t['selection_text']};
}}

QPushButton[cssClass="success"]:hover {{
    background-color: {t['success_hover']};
}}

QPushButton[cssClass="secondary"] {{
    background-color: {t['bg_secondary']};
    color: {t['text_primary']};
    border: 1px solid {t['border']};
}}

QPushButton[cssClass="secondary"]:hover {{
    background-color: {t['bg_tertiary']};
}}

QLabel {{
    color: {t['text_primary']};
    font-size: 13px;
    background-color: transparent;
}}

QLabel[cssClass="title"] {{
    font-size: 20px;
    font-weight: bold;
    color: {t['accent']};
    padding: 4px 0px;
}}

QLabel[cssClass="subtitle"] {{
    font-size: 12px;
    color: {t['text_dim']};
}}

QLabel[cssClass="section"] {{
    font-size: 14px;
    font-weight: bold;
    color: {t['text_primary']};
    padding: 8px 0px 4px 0px;
}}

QLabel[cssClass="success"] {{
    color: {t['success']};
    font-weight: bold;
}}

QLabel[cssClass="error"] {{
    color: {t['danger']};
    font-weight: bold;
}}

QLabel[cssClass="warning"] {{
    color: {t['warning']};
    font-weight: bold;
}}

QLineEdit {{
    background-color: {t['bg_secondary']};
    color: {t['text_primary']};
    border: 2px solid {t['border']};
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 13px;
    min-height: 20px;
}}

QLineEdit:focus {{
    border-color: {t['border_focus']};
}}

QLineEdit:disabled {{
    background-color: {t['bg_tertiary']};
    color: {t['text_dim']};
}}

QComboBox {{
    background-color: {t['bg_secondary']};
    color: {t['text_primary']};
    border: 2px solid {t['border']};
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 13px;
    min-height: 20px;
}}

QComboBox:hover {{
    border-color: {t['border_focus']};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {t['bg_secondary']};
    color: {t['text_primary']};
    selection-background-color: {t['selection']};
    selection-color: {t['selection_text']};
    border: 1px solid {t['border']};
    border-radius: 4px;
    padding: 4px;
}}

QCheckBox {{
    color: {t['text_primary']};
    font-size: 13px;
    spacing: 8px;
    background-color: transparent;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid {t['border']};
    background-color: {t['bg_secondary']};
}}

QCheckBox::indicator:checked {{
    background-color: {t['accent']};
    border-color: {t['accent']};
}}

QCheckBox::indicator:hover {{
    border-color: {t['border_focus']};
}}

QTreeWidget {{
    background-color: {t['bg_secondary']};
    color: {t['text_primary']};
    border: 2px solid {t['border']};
    border-radius: 8px;
    padding: 4px;
    font-size: 13px;
    alternate-background-color: {t['bg_tertiary']};
}}

QTreeWidget::item {{
    padding: 4px;
    border-radius: 4px;
}}

QTreeWidget::item:selected {{
    background-color: {t['selection']};
    color: {t['selection_text']};
}}

QTreeWidget::item:hover:!selected {{
    background-color: {t['bg_hover']};
}}

QHeaderView::section {{
    background-color: {t['header_bg']};
    color: {t['text_primary']};
    padding: 8px;
    border: none;
    border-bottom: 2px solid {t['border']};
    font-weight: bold;
}}

QTextEdit {{
    background-color: {t['code_bg']};
    color: {t['text_primary']};
    border: 2px solid {t['border']};
    border-radius: 8px;
    padding: 8px;
    font-family: "Cascadia Code", "Consolas", monospace;
    font-size: 12px;
}}

QTextEdit:focus {{
    border-color: {t['border_focus']};
}}

QProgressBar {{
    background-color: {t['bg_secondary']};
    border: none;
    border-radius: 8px;
    height: 24px;
    text-align: center;
    color: {t['text_primary']};
    font-size: 11px;
}}

QProgressBar::chunk {{
    background-color: {t['accent']};
    border-radius: 8px;
}}

QScrollBar:vertical {{
    background-color: transparent;
    width: 10px;
    border-radius: 5px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background-color: {t['scrollbar']};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {t['scrollbar_hover']};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: transparent;
    height: 10px;
    border-radius: 5px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background-color: {t['scrollbar']};
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {t['scrollbar_hover']};
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

QGroupBox {{
    color: {t['text_primary']};
    border: 2px solid {t['border']};
    border-radius: 10px;
    margin-top: 14px;
    padding: 20px 12px 12px 12px;
    font-size: 13px;
    font-weight: bold;
    background-color: {t['bg_secondary']};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 8px;
    color: {t['accent']};
    background-color: {t['bg_secondary']};
}}

QListWidget {{
    background-color: {t['bg_secondary']};
    color: {t['text_primary']};
    border: 2px solid {t['border']};
    border-radius: 8px;
    padding: 4px;
    font-size: 13px;
}}

QListWidget::item {{
    padding: 6px;
    border-radius: 4px;
}}

QListWidget::item:selected {{
    background-color: {t['selection']};
    color: {t['selection_text']};
}}

QListWidget::item:hover:!selected {{
    background-color: {t['bg_hover']};
}}

QSplitter::handle {{
    background-color: {t['border']};
}}

QToolTip {{
    background-color: {t['bg_secondary']};
    color: {t['text_primary']};
    border: 1px solid {t['border']};
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}}

QMessageBox {{
    background-color: {t['bg_primary']};
}}

QMessageBox QLabel {{
    color: {t['text_primary']};
}}
"""