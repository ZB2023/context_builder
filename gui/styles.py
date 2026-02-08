DARK_THEME = {
    "name": "dark",
    "bg_base": "#1e1e2e",
    "bg_surface": "#252536",
    "bg_element": "#3b3b54",
    "primary": "#89b4fa",
    "primary_hover": "#b4d0ff",
    "secondary": "#585b70",
    "success": "#a6e3a1",
    "success_dark": "#3a5a38",
    "warning": "#f9e2af",
    "danger": "#f38ba8",
    "danger_dark": "#5c2636",
    "text_main": "#cdd6f4",
    "text_dim": "#9399b2",
    "text_on_primary": "#11111b",
    "border": "#3b3b54",
    "border_hover": "#5a5a7a",
    "radius": "8",
    "sidebar_bg": "#181825",
    "sidebar_hover": "#2a2a3c",
    "sidebar_selected": "#313244",
    "input_bg": "#181825",
    "shadow": "rgba(0,0,0,0.3)",
}

LIGHT_THEME = {
    "name": "light",
    "bg_base": "#f5f5fa",
    "bg_surface": "#ffffff",
    "bg_element": "#e8e8f0",
    "primary": "#4a6cf7",
    "primary_hover": "#6b88ff",
    "secondary": "#9ca0b0",
    "success": "#34a853",
    "success_dark": "#c8f0cc",
    "warning": "#f5a623",
    "danger": "#ea4335",
    "danger_dark": "#fdd",
    "text_main": "#2d2d3a",
    "text_dim": "#6c6f85",
    "text_on_primary": "#ffffff",
    "border": "#d8d8e4",
    "border_hover": "#b0b0c4",
    "radius": "8",
    "sidebar_bg": "#eaeaf2",
    "sidebar_hover": "#dddde8",
    "sidebar_selected": "#d0d0e0",
    "input_bg": "#f0f0f8",
    "shadow": "rgba(0,0,0,0.08)",
}


def generate_stylesheet(theme):
    t = theme
    r = t["radius"]

    return f"""
    * {{
        font-family: "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
        font-size: 13px;
        color: {t['text_main']};
        outline: none;
    }}

    QMainWindow, QWidget {{
        background-color: {t['bg_base']};
    }}

    QWidget#Sidebar {{
        background-color: {t['sidebar_bg']};
        border-right: 1px solid {t['border']};
    }}

    QLabel[cssClass="header"] {{
        font-size: 18px;
        font-weight: 700;
        color: {t['primary']};
        padding: 0;
        margin: 0;
        letter-spacing: 0.5px;
    }}

    QLabel[cssClass="title"] {{
        font-size: 20px;
        font-weight: 700;
        color: {t['text_main']};
        padding: 0;
        margin: 0;
    }}

    QLabel[cssClass="subtitle"] {{
        font-size: 12px;
        color: {t['text_dim']};
        padding: 0;
        margin: 0;
    }}

    QLabel[cssClass="field-label"] {{
        font-size: 11px;
        font-weight: 600;
        color: {t['text_dim']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 0;
        margin: 0;
    }}

    QLabel[cssClass="success"] {{
        color: {t['success']};
        font-weight: 600;
    }}

    QLabel[cssClass="error"] {{
        color: {t['danger']};
        font-weight: 600;
    }}

    QListWidget#NavList {{
        background-color: transparent;
        border: none;
        outline: none;
    }}

    QListWidget#NavList::item {{
        height: 42px;
        padding-left: 16px;
        padding-right: 8px;
        border-radius: {r}px;
        margin: 2px 8px;
        color: {t['text_dim']};
        border: none;
        font-size: 13px;
    }}

    QListWidget#NavList::item:hover {{
        background-color: {t['sidebar_hover']};
        color: {t['text_main']};
    }}

    QListWidget#NavList::item:selected {{
        background-color: {t['sidebar_selected']};
        color: {t['primary']};
        font-weight: 600;
    }}

    QListWidget#NavList::item:focus {{
        outline: none;
        border: none;
    }}

    QPushButton {{
        background-color: {t['bg_element']};
        color: {t['text_main']};
        border: 1px solid {t['border']};
        border-radius: {r}px;
        padding: 8px 20px;
        min-width: 70px;
        min-height: 18px;
        font-size: 13px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        background-color: {t['border_hover']};
        border-color: {t['border_hover']};
    }}

    QPushButton:pressed {{
        background-color: {t['primary']};
        color: {t['text_on_primary']};
        border-color: {t['primary']};
    }}

    QPushButton:disabled {{
        opacity: 0.5;
        background-color: {t['bg_element']};
        color: {t['text_dim']};
    }}

    QPushButton[cssClass="success"] {{
        background-color: {t['primary']};
        color: {t['text_on_primary']};
        border: 1px solid {t['primary']};
        font-weight: 600;
    }}

    QPushButton[cssClass="success"]:hover {{
        background-color: {t['primary_hover']};
        border-color: {t['primary_hover']};
    }}

    QPushButton[cssClass="success"]:disabled {{
        background-color: {t['bg_element']};
        color: {t['text_dim']};
        border-color: {t['border']};
    }}

    QPushButton[cssClass="danger"] {{
        background-color: transparent;
        color: {t['danger']};
        border: 1px solid {t['danger']};
        font-weight: 600;
    }}

    QPushButton[cssClass="danger"]:hover {{
        background-color: {t['danger']};
        color: {t['text_on_primary']};
    }}

    QPushButton[cssClass="secondary"] {{
        background-color: transparent;
        color: {t['text_dim']};
        border: 1px solid {t['border']};
        font-weight: 400;
        padding: 4px 12px;
        min-height: 14px;
    }}

    QPushButton[cssClass="secondary"]:hover {{
        background-color: {t['bg_element']};
        color: {t['text_main']};
    }}

    QLineEdit, QComboBox {{
        background-color: {t['input_bg']};
        border: 1px solid {t['border']};
        border-radius: {r}px;
        padding: 8px 12px;
        font-size: 13px;
        min-height: 16px;
        selection-background-color: {t['primary']};
        selection-color: {t['text_on_primary']};
    }}

    QLineEdit:focus, QComboBox:focus {{
        border: 1px solid {t['primary']};
    }}

    QLineEdit:hover, QComboBox:hover {{
        border: 1px solid {t['border_hover']};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 28px;
    }}

    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {t['text_dim']};
        margin-right: 8px;
    }}

    QComboBox QAbstractItemView {{
        background-color: {t['bg_surface']};
        border: 1px solid {t['border']};
        border-radius: {r}px;
        padding: 4px;
        selection-background-color: {t['primary']};
        selection-color: {t['text_on_primary']};
        outline: none;
    }}

    QTextEdit, QPlainTextEdit {{
        background-color: {t['input_bg']};
        border: 1px solid {t['border']};
        border-radius: {r}px;
        padding: 8px;
        font-size: 12px;
        font-family: "Cascadia Code", "Consolas", monospace;
        selection-background-color: {t['primary']};
        selection-color: {t['text_on_primary']};
    }}

    QTextEdit:focus, QPlainTextEdit:focus {{
        border: 1px solid {t['primary']};
    }}

    QFrame#InputGroup {{
        background-color: {t['input_bg']};
        border: 1px solid {t['border']};
        border-radius: {r}px;
    }}

    QFrame#InputGroup:hover {{
        border: 1px solid {t['border_hover']};
    }}

    QLineEdit#GroupInput {{
        background: transparent;
        border: none;
        padding: 8px 12px;
        min-height: 16px;
    }}

    QLineEdit#GroupInput:focus {{
        border: none;
    }}

    QPushButton#GroupBtn {{
        background-color: {t['bg_element']};
        color: {t['text_main']};
        border: none;
        border-left: 1px solid {t['border']};
        border-top-right-radius: {r}px;
        border-bottom-right-radius: {r}px;
        border-top-left-radius: 0;
        border-bottom-left-radius: 0;
        padding: 8px 16px;
        margin: 0;
        min-width: 60px;
        font-weight: 500;
    }}

    QPushButton#GroupBtn:hover {{
        background-color: {t['border_hover']};
    }}

    QGroupBox {{
        border: 1px solid {t['border']};
        border-radius: {r}px;
        margin-top: 24px;
        padding: 16px 12px 12px 12px;
        font-size: 13px;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 14px;
        padding: 2px 8px;
        color: {t['primary']};
        font-weight: 700;
        font-size: 13px;
        background-color: {t['bg_base']};
        border-radius: 4px;
    }}

    QCheckBox {{
        spacing: 8px;
        font-size: 13px;
        color: {t['text_main']};
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {t['border']};
        border-radius: 4px;
        background-color: {t['input_bg']};
    }}

    QCheckBox::indicator:hover {{
        border-color: {t['primary']};
    }}

    QCheckBox::indicator:checked {{
        background-color: {t['primary']};
        border-color: {t['primary']};
        image: none;
    }}

    QListWidget {{
        background-color: {t['input_bg']};
        border: 1px solid {t['border']};
        border-radius: {r}px;
        padding: 4px;
        outline: none;
    }}

    QListWidget::item {{
        padding: 6px 8px;
        border-radius: 4px;
        margin: 1px 2px;
    }}

    QListWidget::item:hover {{
        background-color: {t['bg_element']};
    }}

    QListWidget::item:selected {{
        background-color: {t['primary']};
        color: {t['text_on_primary']};
    }}

    QProgressBar {{
        background-color: {t['bg_element']};
        border: none;
        border-radius: 2px;
        text-align: center;
        max-height: 4px;
    }}

    QProgressBar::chunk {{
        background-color: {t['primary']};
        border-radius: 2px;
    }}

    QTreeWidget {{
        background-color: {t['input_bg']};
        border: 1px solid {t['border']};
        border-radius: {r}px;
        padding: 4px;
        alternate-background-color: {t['bg_element']};
        outline: none;
    }}

    QTreeWidget::item {{
        padding: 3px 4px;
        border-radius: 3px;
    }}

    QTreeWidget::item:hover {{
        background-color: {t['bg_element']};
    }}

    QTreeWidget::item:selected {{
        background-color: {t['primary']};
        color: {t['text_on_primary']};
    }}

    QHeaderView::section {{
        background-color: {t['bg_element']};
        color: {t['text_dim']};
        padding: 6px 8px;
        border: none;
        border-bottom: 1px solid {t['border']};
        font-weight: 600;
        font-size: 11px;
        text-transform: uppercase;
    }}

    QSplitter::handle {{
        background-color: {t['border']};
        height: 3px;
        margin: 0px 40px;
        border-radius: 1px;
    }}

    QSplitter::handle:hover {{
        background-color: {t['primary']};
    }}

    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0;
        border-radius: 4px;
    }}

    QScrollBar::handle:vertical {{
        background: {t['bg_element']};
        min-height: 30px;
        border-radius: 4px;
        margin: 2px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {t['secondary']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: transparent;
        height: 8px;
        margin: 0;
        border-radius: 4px;
    }}

    QScrollBar::handle:horizontal {{
        background: {t['bg_element']};
        min-width: 30px;
        border-radius: 4px;
        margin: 2px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {t['secondary']};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    QListWidget#NavList QScrollBar:vertical {{
        width: 0px;
        height: 0px;
    }}

    QToolTip {{
        background-color: {t['bg_surface']};
        color: {t['text_main']};
        border: 1px solid {t['border']};
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
    }}

    QMessageBox {{
        background-color: {t['bg_surface']};
    }}

    QMessageBox QLabel {{
        color: {t['text_main']};
        font-size: 13px;
    }}

    QMessageBox QPushButton {{
        min-width: 80px;
    }}
    """