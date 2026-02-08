from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QScrollArea,
)
from PySide6.QtCore import Qt


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        container.setMaximumWidth(800)

        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Context Builder")
        title.setProperty("cssClass", "title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        version = QLabel("Версия 1.2.0")
        version.setProperty("cssClass", "subtitle")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        about = QTextEdit()
        about.setReadOnly(True)
        about.setFrameShape(QTextEdit.Shape.NoFrame)
        about.setHtml("""
        <h3>Для чего создан Context Builder?</h3>
        <p>Context Builder — инструмент для разработчиков, аналитиков и всех,
        кто работает с проектами, содержащими множество файлов и папок.</p>

        <p>Программа позволяет быстро создать полный снимок структуры проекта —
        от дерева папок до содержимого каждого файла — и сохранить его
        в удобном формате.</p>

        <h3>Зачем это нужно?</h3>
        <ul>
            <li><b>Документирование</b> — отчёты о структуре кодовой базы</li>
            <li><b>Работа с ИИ</b> — подготовка контекста для LLM</li>
            <li><b>Аудит безопасности</b> — поиск и маскировка конфиденциальных данных</li>
            <li><b>Архивирование</b> — снимок состояния проекта</li>
            <li><b>Код-ревью</b> — передача структуры коллегам</li>
        </ul>

        <h3>Возможности</h3>
        <ul>
            <li>Сканирование директорий (3 режима)</li>
            <li>Экспорт в TXT, Markdown, JSON, PDF</li>
            <li>Конвертация между форматами</li>
            <li>Цензура паролей, ключей, email</li>
            <li>Подсчёт токенов для LLM</li>
            <li>Профили настроек</li>
            <li>GUI + CLI</li>
        </ul>

        <h3>Технологии</h3>
        <p>Python 3.10+ · PySide6 · InquirerPy · Rich · fpdf2 · PyMuPDF · tiktoken</p>

        <h3>Лицензия</h3>
        <p>MIT License — свободное использование и распространение.</p>
        """)
        layout.addWidget(about, 1)

        footer = QLabel("© 2025 Context Builder · MIT License")
        footer.setProperty("cssClass", "subtitle")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addWidget(container)
        wrapper.addStretch()

        scroll_content = QWidget()
        scroll_content.setLayout(wrapper)
        scroll.setWidget(scroll_content)

        outer.addWidget(scroll)