from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Context Builder")
        title.setProperty("cssClass", "title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        version = QLabel("Версия 1.2.0")
        version.setProperty("cssClass", "subtitle")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        separator = QLabel("")
        separator.setFixedHeight(2)
        separator.setStyleSheet("background-color: palette(mid); border-radius: 1px;")
        layout.addWidget(separator)

        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml("""
        <h3 style="margin-bottom: 8px;">Для чего создан Context Builder?</h3>
        <p>Context Builder — это инструмент для разработчиков, аналитиков и всех,
        кто работает с проектами, содержащими множество файлов и папок.</p>

        <p>Программа позволяет быстро создать полный снимок структуры проекта —
        от дерева папок до содержимого каждого файла — и сохранить его
        в удобном формате для анализа, документирования или передачи.</p>

        <h3 style="margin-bottom: 8px;">Зачем это нужно?</h3>
        <ul>
            <li><b>Документирование проектов</b> — создание отчётов о структуре кодовой базы</li>
            <li><b>Работа с ИИ</b> — подготовка контекста для LLM (ChatGPT, Claude и др.)</li>
            <li><b>Аудит безопасности</b> — поиск и маскировка конфиденциальных данных</li>
            <li><b>Архивирование</b> — сохранение состояния проекта на определённый момент</li>
            <li><b>Код-ревью</b> — передача структуры проекта коллегам для анализа</li>
        </ul>

        <h3 style="margin-bottom: 8px;">Возможности</h3>
        <ul>
            <li>Сканирование директорий в трёх режимах</li>
            <li>Экспорт в TXT, Markdown, JSON и PDF</li>
            <li>Конвертация между всеми форматами</li>
            <li>Автоматическая цензура паролей, ключей и email</li>
            <li>Подсчёт токенов для LLM</li>
            <li>Профили настроек для повторяющихся задач</li>
            <li>Графический интерфейс и командная строка</li>
        </ul>

        <h3 style="margin-bottom: 8px;">Технологии</h3>
        <ul>
            <li><b>Python 3.10+</b></li>
            <li><b>PySide6</b> — графический интерфейс</li>
            <li><b>InquirerPy</b> — интерактивное CLI меню</li>
            <li><b>Rich</b> — красивый консольный вывод</li>
            <li><b>fpdf2</b> — генерация PDF</li>
            <li><b>PyMuPDF</b> — чтение PDF</li>
            <li><b>tiktoken</b> — подсчёт токенов</li>
        </ul>

        <h3 style="margin-bottom: 8px;">Лицензия</h3>
        <p>MIT License — свободное использование, модификация и распространение.</p>
        """)
        layout.addWidget(about_text)

        footer = QLabel("© 2025 Context Builder. MIT License.")
        footer.setProperty("cssClass", "subtitle")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)