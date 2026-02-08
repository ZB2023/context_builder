from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 36, 48, 36)
        layout.setSpacing(16)

        title = QLabel("О программе")
        title.setProperty("cssClass", "title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title)

        about = QTextEdit()
        about.setReadOnly(True)
        about.setFrameShape(QFrame.Shape.NoFrame)

        html_content = """
        <style>
            body {
                font-family: 'Segoe UI', 'Inter', sans-serif;
            }
            h3 {
                margin-top: 22px;
                margin-bottom: 6px;
                color: #89b4fa;
                font-family: 'Segoe UI', sans-serif;
                font-size: 17px;
                font-weight: 600;
            }
            p, li {
                line-height: 1.7;
                font-size: 14px;
                margin-bottom: 8px;
                color: #cdd6f4;
            }
            ul {
                margin-bottom: 12px;
                margin-left: -16px;
            }
            li {
                margin-bottom: 4px;
            }
            b {
                color: #89b4fa;
            }
            .tech {
                color: #a6adc8;
                font-size: 13px;
                font-family: 'Cascadia Code', 'Consolas', monospace;
            }
            .footer {
                margin-top: 32px;
                color: #6c7086;
                font-size: 12px;
            }
            .divider {
                border: none;
                border-top: 1px solid #313244;
                margin: 20px 0;
            }
        </style>

        <h3>🔍 Для чего создан Context Builder?</h3>
        <p>Context Builder — инструмент для разработчиков, аналитиков и всех,
        кто работает с проектами, содержащими множество файлов и папок.</p>
        <p>Программа позволяет быстро создать полный снимок структуры проекта —
        от дерева папок до содержимого каждого файла — и сохранить его
        в удобном формате.</p>

        <hr class="divider">

        <h3>🎯 Зачем это нужно?</h3>
        <ul>
            <li><b>Документирование</b> — отчёты о структуре кодовой базы</li>
            <li><b>Работа с ИИ</b> — подготовка контекста для LLM</li>
            <li><b>Аудит безопасности</b> — поиск и маскировка конфиденциальных данных</li>
            <li><b>Архивирование</b> — снимок состояния проекта</li>
            <li><b>Код-ревью</b> — передача структуры коллегам</li>
        </ul>

        <h3>⚡ Возможности</h3>
        <ul>
            <li>Сканирование директорий (3 режима)</li>
            <li>Экспорт в TXT, Markdown, JSON, PDF</li>
            <li>Конвертация между форматами</li>
            <li>Цензура паролей, ключей, email</li>
            <li>Подсчёт токенов для LLM</li>
            <li>Профили настроек</li>
        </ul>

        <hr class="divider">

        <h3>🛠 Технологии</h3>
        <p class="tech">Python 3.10+  ·  PySide6  ·  InquirerPy  ·  Rich  ·  fpdf2  ·  PyMuPDF  ·  tiktoken</p>

        <h3>📄 Лицензия</h3>
        <p>MIT License — свободное использование и распространение.</p>

        <p class="footer">© 2026 Context Builder v1.2.0</p>
        """

        about.setHtml(html_content)
        layout.addWidget(about)