DARK_THEME = {
    "name": "dark",
    "bg_primary": "#1e1e2e",
    "bg_secondary": "#282839",
    "bg_card": "#313244",
    "bg_input": "#3b3b50",
    "bg_hover": "#45475a",
    "accent": "#89b4fa",
    "accent_hover": "#a6c8ff",
    "accent_pressed": "#6a9be0",
    "success": "#a6e3a1",
    "success_hover": "#b8f0b4",
    "danger": "#f38ba8",
    "danger_hover": "#f5a0b8",
    "warning": "#f9e2af",
    "text_primary": "#cdd6f4",
    "text_secondary": "#a6adc8",
    "text_placeholder": "#7f849c",
    "text_on_accent": "#1e1e2e",
    "border": "#3b3b50",
    "border_focus": "#89b4fa",
    "check_bg": "#3b3b50",
    "check_border": "#5a5a72",
    "check_active": "#89b4fa",
    "check_mark": "#1e1e2e",
    "scrollbar_bg": "transparent",
    "scrollbar_handle": "#45475a",
    "scrollbar_hover": "#585b70",
    "tab_bg": "#282839",
    "tab_selected_bg": "#89b4fa",
    "tab_selected_text": "#1e1e2e",
    "tab_hover_bg": "#3b3b50",
    "header_bg": "#282839",
    "header_border": "#3b3b50",
    "toast_bg": "#313244",
    "toast_border": "#45475a",
    "code_bg": "#181825",
    "shadow": "rgba(0,0,0,0.3)",
    "radius": "6",
    "radius_lg": "10",
}

LIGHT_THEME = {
    "name": "light",
    "bg_primary": "#f5f5f9",
    "bg_secondary": "#ecedf2",
    "bg_card": "#ffffff",
    "bg_input": "#f0f0f5",
    "bg_hover": "#e4e4ec",
    "accent": "#4a6cf7",
    "accent_hover": "#5b7bf8",
    "accent_pressed": "#3a5ce0",
    "success": "#2ecc71",
    "success_hover": "#3dd87e",
    "danger": "#e74c3c",
    "danger_hover": "#f05a4a",
    "warning": "#f39c12",
    "text_primary": "#2c3e50",
    "text_secondary": "#5a6a7e",
    "text_placeholder": "#95a5b6",
    "text_on_accent": "#ffffff",
    "border": "#d8dae0",
    "border_focus": "#4a6cf7",
    "check_bg": "#f0f0f5",
    "check_border": "#c0c4cc",
    "check_active": "#4a6cf7",
    "check_mark": "#ffffff",
    "scrollbar_bg": "transparent",
    "scrollbar_handle": "#c8cad0",
    "scrollbar_hover": "#aeb0b8",
    "tab_bg": "#ecedf2",
    "tab_selected_bg": "#4a6cf7",
    "tab_selected_text": "#ffffff",
    "tab_hover_bg": "#e0e1e8",
    "header_bg": "#ffffff",
    "header_border": "#e0e1e8",
    "toast_bg": "#ffffff",
    "toast_border": "#d8dae0",
    "code_bg": "#f8f8fc",
    "shadow": "rgba(0,0,0,0.08)",
    "radius": "6",
    "radius_lg": "10",
}


def generate_stylesheet(theme):
    t = theme
    r = t["radius"]
    rl = t["radius_lg"]

    return f"""
* {{
    font-family: "Segoe UI", "Arial", sans-serif;
    outline: none;
}}

QMainWindow {{
    background-color: {t['bg_primary']};
}}

QWidget {{
    background-color: {t['bg_primary']};
    color: {t['text_primary']};
    font-size: 13px;
}}

QWidget[cssClass="header"] {{
    background-color: {t['header_bg']};
    border-bottom: 1px solid {t['header_border']};
}}

QTabWidget::pane {{
    border: none;
    background-color: {t['bg_primary']};
    margin-top: -1px;
}}

QTabBar {{
    background-color: {t['bg_primary']};
}}

QTabBar::tab {{
    background-color: {t['tab_bg']};
    color: {t['text_secondary']};
    padding: 8px 16px;
    margin: 0px 1px;
    border: none;
    border-bottom: 3px solid transparent;
    font-size: 12px;
    min-width: 100px;
}}

QTabBar::tab:selected {{
    background-color: {t['bg_primary']};
    color: {t['accent']};
    border-bottom: 3px solid {t['accent']};
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: {t['tab_hover_bg']};
    color: {t['text_primary']};
}}

QPushButton {{
    background-color: {t['accent']};
    color: {t['text_on_accent']};
    border: none;
    padding: 8px 20px;
    border-radius: {r}px;
    font-size: 13px;
    font-weight: 600;
    min-height: 18px;
}}

QPushButton:hover {{
    background-color: {t['accent_hover']};
}}

QPushButton:pressed {{
    background-color: {t['accent_pressed']};
}}

QPushButton:disabled {{
    background-color: {t['bg_hover']};
    color: {t['text_placeholder']};
}}

QPushButton[cssClass="danger"] {{
    background-color: {t['danger']};
    color: {t['text_on_accent']};
}}

QPushButton[cssClass="danger"]:hover {{
    background-color: {t['danger_hover']};
}}

QPushButton[cssClass="success"] {{
    background-color: {t['success']};
    color: {t['text_on_accent']};
}}

QPushButton[cssClass="success"]:hover {{
    background-color: {t['success_hover']};
}}

QPushButton[cssClass="secondary"] {{
    background-color: {t['bg_input']};
    color: {t['text_primary']};
    border: 1px solid {t['border']};
}}

QPushButton[cssClass="secondary"]:hover {{
    background-color: {t['bg_hover']};
    border-color: {t['accent']};
}}

QPushButton[cssClass="icon"] {{
    background-color: transparent;
    border: 1px solid {t['border']};
    border-radius: {r}px;
    padding: 6px;
    min-height: 14px;
    min-width: 14px;
}}

QPushButton[cssClass="icon"]:hover {{
    background-color: {t['bg_hover']};
    border-color: {t['accent']};
}}

QLabel {{
    color: {t['text_primary']};
    font-size: 13px;
    background-color: transparent;
    padding: 0px;
    margin: 0px;
}}

QLabel[cssClass="title"] {{
    font-size: 18px;
    font-weight: bold;
    color: {t['accent']};
    padding: 0px;
    margin: 0px;
}}

QLabel[cssClass="subtitle"] {{
    font-size: 11px;
    color: {t['text_placeholder']};
}}

QLabel[cssClass="section"] {{
    font-size: 13px;
    font-weight: bold;
    color: {t['text_primary']};
    padding: 4px 0px 2px 0px;
}}

QLabel[cssClass="success"] {{
    color: {t['success']};
    font-weight: bold;
    font-size: 12px;
}}

QLabel[cssClass="error"] {{
    color: {t['danger']};
    font-weight: bold;
    font-size: 12px;
}}

QLabel[cssClass="field-label"] {{
    font-size: 12px;
    color: {t['text_secondary']};
    font-weight: 600;
    padding: 0px;
    margin: 0px 0px 2px 2px;
}}

QLineEdit {{
    background-color: {t['bg_input']};
    color: {t['text_primary']};
    border: 1px solid {t['border']};
    padding: 7px 10px;
    border-radius: {r}px;
    font-size: 13px;
    min-height: 16px;
    selection-background-color: {t['accent']};
    selection-color: {t['text_on_accent']};
}}

QLineEdit:focus {{
    border-color: {t['border_focus']};
    border-width: 2px;
    padding: 6px 9px;
}}

QLineEdit::placeholder {{
    color: {t['text_placeholder']};
}}

QComboBox {{
    background-color: {t['bg_input']};
    color: {t['text_primary']};
    border: 1px solid {t['border']};
    padding: 7px 10px;
    border-radius: {r}px;
    font-size: 13px;
    min-height: 16px;
}}

QComboBox:hover {{
    border-color: {t['border_focus']};
}}

QComboBox:focus {{
    border-color: {t['border_focus']};
    border-width: 2px;
    padding: 6px 9px;
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
    padding-right: 6px;
}}

QComboBox QAbstractItemView {{
    background-color: {t['bg_card']};
    color: {t['text_primary']};
    border: 1px solid {t['border']};
    border-radius: {r}px;
    padding: 4px;
    selection-background-color: {t['accent']};
    selection-color: {t['text_on_accent']};
}}

QCheckBox {{
    color: {t['text_primary']};
    font-size: 13px;
    spacing: 8px;
    background-color: transparent;
    padding: 4px 0px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {t['check_border']};
    background-color: {t['check_bg']};
}}

QCheckBox::indicator:checked {{
    background-color: {t['check_active']};
    border-color: {t['check_active']};
    image: none;
}}

QCheckBox::indicator:hover {{
    border-color: {t['accent']};
}}

QTreeWidget {{
    background-color: {t['bg_card']};
    color: {t['text_primary']};
    border: 1px solid {t['border']};
    border-radius: {r}px;
    padding: 4px;
    font-size: 12px;
    alternate-background-color: {t['bg_input']};
}}

QTreeWidget::item {{
    padding: 3px 4px;
    border-radius: 3px;
}}

QTreeWidget::item:selected {{
    background-color: {t['accent']};
    color: {t['text_on_accent']};
}}

QTreeWidget::item:hover:!selected {{
    background-color: {t['bg_hover']};
}}

QHeaderView::section {{
    background-color: {t['bg_card']};
    color: {t['text_secondary']};
    padding: 6px 8px;
    border: none;
    border-bottom: 1px solid {t['border']};
    font-weight: 600;
    font-size: 11px;
}}

QTextEdit {{
    background-color: {t['code_bg']};
    color: {t['text_primary']};
    border: 1px solid {t['border']};
    border-radius: {r}px;
    padding: 6px 8px;
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 11px;
    selection-background-color: {t['accent']};
    selection-color: {t['text_on_accent']};
}}

QProgressBar {{
    background-color: {t['bg_input']};
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
    color: transparent;
}}

QProgressBar::chunk {{
    background-color: {t['accent']};
    border-radius: 4px;
}}

QScrollBar:vertical {{
    background-color: {t['scrollbar_bg']};
    width: 8px;
    border-radius: 4px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {t['scrollbar_handle']};
    border-radius: 4px;
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
    background-color: {t['scrollbar_bg']};
    height: 8px;
    border-radius: 4px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: {t['scrollbar_handle']};
    border-radius: 4px;
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
    border: 1px solid {t['border']};
    border-radius: {r}px;
    margin-top: 12px;
    padding: 14px 10px 10px 10px;
    font-size: 12px;
    font-weight: bold;
    background-color: {t['bg_card']};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: {t['accent']};
    background-color: {t['bg_card']};
    font-size: 12px;
}}

QListWidget {{
    background-color: {t['bg_card']};
    color: {t['text_primary']};
    border: 1px solid {t['border']};
    border-radius: {r}px;
    padding: 4px;
    font-size: 12px;
}}

QListWidget::item {{
    padding: 5px 6px;
    border-radius: 4px;
}}

QListWidget::item:selected {{
    background-color: {t['accent']};
    color: {t['text_on_accent']};
}}

QListWidget::item:hover:!selected {{
    background-color: {t['bg_hover']};
}}

QToolTip {{
    background-color: {t['toast_bg']};
    color: {t['text_primary']};
    border: 1px solid {t['toast_border']};
    border-radius: {r}px;
    padding: 6px 10px;
    font-size: 12px;
}}

QMessageBox {{
    background-color: {t['bg_card']};
}}

QMessageBox QLabel {{
    color: {t['text_primary']};
    font-size: 13px;
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}

QStatusBar {{
    background-color: {t['header_bg']};
    color: {t['text_placeholder']};
    border-top: 1px solid {t['header_border']};
    font-size: 11px;
    padding: 2px 8px;
}}
"""