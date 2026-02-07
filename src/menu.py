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


def input_file_path():
    return inquirer.filepath(
        message="Укажите путь к файлу:",
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


def select_convert_format(current_format):
    all_formats = {
        "txt": "TXT — текстовый файл",
        "md": "MD — Markdown",
        "json": "JSON — структурированные данные",
    }

    choices = [
        {"name": name, "value": fmt}
        for fmt, name in all_formats.items()
        if fmt != current_format
    ]
    choices.append({"name": "← Назад", "value": "back"})

    return inquirer.select(
        message=f"Текущий формат: {current_format.upper()}. Выберите целевой формат:",
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


def select_session(sessions):
    if not sessions:
        console.print("[bold red]Нет доступных сессий[/bold red]")
        return None

    choices = [{"name": str(s), "value": s} for s in sessions]
    choices.append({"name": "← Назад", "value": "back"})

    return inquirer.select(
        message="Выберите сессию:",
        choices=choices,
        pointer="→",
    ).execute()


def select_modification_action():
    choices = [
        {"name": "Пересканировать директорию", "value": "rescan"},
        {"name": "Использовать старые данные", "value": "use_old"},
        {"name": "← Назад", "value": "back"},
    ]

    return inquirer.select(
        message="Файл отчёта был изменён вручную. Что делать?",
        choices=choices,
        pointer="→",
    ).execute()


def select_report_files(files):
    if not files:
        console.print("[bold red]Нет файлов для выбора[/bold red]")
        return []

    choices = [{"name": f"{f.name} ({f.suffix})", "value": f} for f in files]

    return inquirer.checkbox(
        message="Выберите файлы для удаления (Пробел — отметить, Enter — подтвердить):",
        choices=choices,
        validate=lambda result: len(result) > 0,
        invalid_message="Выберите хотя бы один файл",
    ).execute()


def toggle_tree_view():
    return inquirer.confirm(
        message="Включить дерево структуры в отчёт?",
        default=True,
    ).execute()


def select_overwrite_action(filepath):
    choices = [
        {"name": "Перезаписать файл", "value": "overwrite"},
        {"name": "Добавить номер к имени", "value": "rename"},
        {"name": "Ввести другое имя", "value": "new_name"},
        {"name": "← Отмена", "value": "cancel"},
    ]

    return inquirer.select(
        message=f"Файл {filepath} уже существует. Что делать?",
        choices=choices,
        pointer="→",
    ).execute()


def toggle_redaction():
    return inquirer.confirm(
        message="Включить цензуру конфиденциальных данных (пароли, ключи, email)?",
        default=False,
    ).execute()


def select_redaction_patterns(patterns):
    choices = [{"name": p, "value": p, "enabled": True} for p in patterns]

    return inquirer.checkbox(
        message="Выберите типы данных для цензуры (Пробел — переключить):",
        choices=choices,
        validate=lambda result: len(result) > 0,
        invalid_message="Выберите хотя бы один тип",
    ).execute()


def select_profile(profiles):
    if not profiles:
        console.print("[bold red]Нет сохранённых профилей[/bold red]")
        return None

    choices = [{"name": p, "value": p} for p in profiles]
    choices.append({"name": "← Назад", "value": "back"})

    return inquirer.select(
        message="Выберите профиль:",
        choices=choices,
        pointer="→",
    ).execute()


def input_profile_name():
    return inquirer.text(
        message="Название профиля:",
        validate=lambda name: len(name.strip()) > 0,
        invalid_message="Название не может быть пустым",
    ).execute()


def settings_menu():
    choices = [
        "Сохранить текущий профиль",
        "Загрузить профиль",
        "Удалить профиль",
        "Список профилей",
        "← Назад",
    ]

    return inquirer.select(
        message="Настройки:",
        choices=choices,
        pointer="→",
    ).execute()


def select_copy_to_clipboard():
    return inquirer.confirm(
        message="Скопировать результат в буфер обмена?",
        default=False,
    ).execute()