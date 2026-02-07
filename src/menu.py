from InquirerPy import inquirer
from rich.console import Console
from rich.panel import Panel

console = Console()


def show_welcome():
    console.print(
        Panel(
            "[bold cyan]Context Builder[/bold cyan]\n"
            "[dim]Инструмент для сканирования и экспорта структуры проектов[/dim]",
            border_style="bright_blue",
            padding=(1, 4),
        )
    )


def main_menu():
    choices = [
        "Сканирование (Запись)",
        "Конвертация",
        "Переконвертация",
        "Удаление записи",
        "Выбор файлов в директориях",
        "Настройки",
        "Выход",
    ]

    return inquirer.select(
        message="Главное меню — выберите действие:",
        choices=choices,
        pointer="→",
    ).execute()


def select_directory_mode():
    choices = [
        {"name": "Одиночный — выбор одной папки", "value": "single"},
        {"name": "Множественный — выбор нескольких папок", "value": "multi"},
        {"name": "Все вложенные — все папки внутри выбранной", "value": "recursive"},
        {"name": "← Назад", "value": "back"},
    ]

    return inquirer.select(
        message="Режим выбора директорий:",
        choices=choices,
        pointer="→",
    ).execute()


def input_directory_path():
    return inquirer.filepath(
        message="Укажите путь к директории:",
        only_directories=True,
        validate=lambda path: len(path) > 0,
        invalid_message="Путь не может быть пустым",
    ).execute()


def input_filename():
    from datetime import datetime

    default_name = f"scan_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    return inquirer.text(
        message="Название файла (без расширения):",
        default=default_name,
        validate=lambda name: len(name.strip()) > 0,
        invalid_message="Название не может быть пустым",
    ).execute()


def select_export_format():
    choices = [
        {"name": "TXT — текстовый файл", "value": "txt"},
        {"name": "MD — Markdown", "value": "md"},
        {"name": "JSON — структурированные данные", "value": "json"},
        {"name": "← Назад", "value": "back"},
    ]

    return inquirer.select(
        message="Формат экспорта:",
        choices=choices,
        pointer="→",
    ).execute()


def confirm_action(message):
    return inquirer.confirm(
        message=message,
        default=False,
    ).execute()


def select_multiple_directories(directories):
    if not directories:
        console.print("[bold red]Нет доступных директорий[/bold red]")
        return []

    choices = [{"name": str(d), "value": d} for d in directories]

    return inquirer.checkbox(
        message="Выберите директории (Пробел — отметить, Enter — подтвердить):",
        choices=choices,
        validate=lambda result: len(result) > 0,
        invalid_message="Выберите хотя бы одну директорию",
    ).execute()