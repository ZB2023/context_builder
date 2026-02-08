import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel

os.environ["ESCDELAY"] = "25"

console = Console()

BACK_VALUE = "__BACK__"
EXIT_VALUE = "__EXIT__"


def show_welcome():
    console.print(
        Panel(
            "[bold cyan]Context Builder[/bold cyan]\n"
            "[dim]Инструмент для сканирования и экспорта структуры проектов[/dim]\n"
            "[dim]Нажмите Escape или выберите ← Назад для возврата[/dim]",
            border_style="bright_blue",
            padding=(1, 4),
        )
    )


def _bind_escape(prompt, result_holder):
    @prompt.register_kb("escape")
    def _escape(event):
        result_holder["escaped"] = True
        event.app.exit(result=BACK_VALUE)


def _execute_with_escape(prompt):
    result_holder = {"escaped": False}
    _bind_escape(prompt, result_holder)

    try:
        app = prompt._application
        app.timeoutlen = 0.05
        app.ttimeoutlen = 0.05
    except (AttributeError, TypeError):
        pass

    try:
        result = prompt.execute()

        if result_holder["escaped"]:
            return BACK_VALUE

        return result
    except KeyboardInterrupt:
        return BACK_VALUE


def _prompt_select(message, choices, back=True):
    if back:
        choices = choices + [Choice(value=BACK_VALUE, name="← Назад")]

    try:
        prompt = inquirer.select(
            message=message,
            choices=choices,
            pointer="→",
        )
        result = _execute_with_escape(prompt)

        if result is None:
            return BACK_VALUE

        return result
    except KeyboardInterrupt:
        return BACK_VALUE


def _prompt_text(message, default="", validate=None, invalid_message="Некорректный ввод"):
    try:
        prompt = inquirer.text(
            message=message,
            default=default,
            validate=validate,
            invalid_message=invalid_message,
        )
        result = _execute_with_escape(prompt)

        if result is None:
            return BACK_VALUE

        return result
    except KeyboardInterrupt:
        return BACK_VALUE


def _prompt_filepath(message, only_directories=False):
    try:
        prompt = inquirer.filepath(
            message=message,
            only_directories=only_directories,
            validate=lambda path: len(path.strip()) > 0,
            invalid_message="Путь не может быть пустым",
        )
        result = _execute_with_escape(prompt)

        if result is None or result == BACK_VALUE:
            return BACK_VALUE

        if not result.strip():
            return BACK_VALUE

        return result
    except KeyboardInterrupt:
        return BACK_VALUE


def _prompt_confirm(message, default=False):
    try:
        prompt = inquirer.confirm(
            message=message,
            default=default,
        )
        result = _execute_with_escape(prompt)

        if result is None:
            return BACK_VALUE

        return result
    except KeyboardInterrupt:
        return BACK_VALUE


def _prompt_checkbox(message, choices, validate=None, invalid_message="Выберите хотя бы один вариант"):
    try:
        prompt = inquirer.checkbox(
            message=message,
            choices=choices,
            validate=validate,
            invalid_message=invalid_message,
        )
        result = _execute_with_escape(prompt)

        if result is None:
            return BACK_VALUE

        return result
    except KeyboardInterrupt:
        return BACK_VALUE


def main_menu():
    choices = [
        Choice(value="scan", name="Сканирование (Запись)"),
        Choice(value="convert", name="Конвертация"),
        Choice(value="reconvert", name="Переконвертация"),
        Choice(value="delete", name="Удаление записи"),
        Choice(value="files", name="Выбор файлов в директориях"),
        Choice(value="settings", name="Настройки"),
        Choice(value=EXIT_VALUE, name="Выход"),
    ]

    return _prompt_select("Главное меню — выберите действие:", choices, back=False)


def select_directory_mode():
    choices = [
        Choice(value="single", name="Одиночный — выбор одной папки"),
        Choice(value="multi", name="Множественный — выбор нескольких папок"),
        Choice(value="recursive", name="Все вложенные — все папки внутри выбранной"),
    ]

    return _prompt_select("Режим выбора директорий:", choices)


def input_directory_path():
    return _prompt_filepath("Укажите путь к директории:", only_directories=True)


def input_file_path():
    return _prompt_filepath("Укажите путь к файлу:")


def input_filename():
    from datetime import datetime

    default_name = f"scan_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    return _prompt_text(
        "Название файла (без расширения):",
        default=default_name,
        validate=lambda name: len(name.strip()) > 0,
        invalid_message="Название не может быть пустым",
    )


def select_export_format():
    choices = [
        Choice(value="txt", name="TXT — текстовый файл"),
        Choice(value="md", name="MD — Markdown"),
        Choice(value="json", name="JSON — структурированные данные"),
        Choice(value="pdf", name="PDF — документ"),
    ]

    return _prompt_select("Формат экспорта:", choices)


def select_convert_format(current_format):
    all_formats = {
        "txt": "TXT — текстовый файл",
        "md": "MD — Markdown",
        "json": "JSON — структурированные данные",
        "pdf": "PDF — документ",
    }

    choices = [
        Choice(value=fmt, name=name)
        for fmt, name in all_formats.items()
        if fmt != current_format
    ]

    return _prompt_select(
        f"Текущий формат: {current_format.upper()}. Выберите целевой формат:",
        choices,
    )


def confirm_action(message):
    return _prompt_confirm(message)


def select_multiple_directories(directories):
    if not directories:
        console.print("[bold red]Нет доступных директорий[/bold red]")
        return BACK_VALUE

    choices = [Choice(value=d, name=str(d)) for d in directories]

    return _prompt_checkbox(
        "Выберите директории (Пробел — отметить, Enter — подтвердить):",
        choices,
        validate=lambda result: len(result) > 0,
        invalid_message="Выберите хотя бы одну директорию",
    )


def select_session(sessions):
    if not sessions:
        console.print("[bold red]Нет доступных сессий[/bold red]")
        return BACK_VALUE

    choices = [Choice(value=s, name=str(s)) for s in sessions]

    return _prompt_select("Выберите сессию:", choices)


def select_modification_action():
    choices = [
        Choice(value="rescan", name="Пересканировать директорию"),
        Choice(value="use_old", name="Использовать старые данные"),
    ]

    return _prompt_select("Файл отчёта был изменён вручную. Что делать?", choices)


def select_report_files(files):
    if not files:
        console.print("[bold red]Нет файлов для выбора[/bold red]")
        return BACK_VALUE

    choices = [
        Choice(value=f, name=f"{f.name} ({f.suffix})")
        for f in files
    ]

    return _prompt_checkbox(
        "Выберите файлы для удаления (Пробел — отметить, Enter — подтвердить):",
        choices,
        validate=lambda result: len(result) > 0,
        invalid_message="Выберите хотя бы один файл",
    )


def toggle_tree_view():
    return _prompt_confirm("Включить дерево структуры в отчёт?", default=True)


def toggle_redaction():
    return _prompt_confirm(
        "Включить цензуру конфиденциальных данных (пароли, ключи, email)?",
        default=False,
    )


def select_redaction_patterns(patterns):
    choices = [
        Choice(value=p, name=p, enabled=True)
        for p in patterns
    ]

    result = _prompt_checkbox(
        "Выберите типы данных для цензуры (Пробел — переключить, Enter — подтвердить):",
        choices,
    )

    if result == BACK_VALUE:
        return BACK_VALUE

    if not result:
        return patterns

    return result


def select_overwrite_action(filepath):
    choices = [
        Choice(value="overwrite", name="Перезаписать файл"),
        Choice(value="rename", name="Добавить номер к имени"),
        Choice(value="new_name", name="Ввести другое имя"),
    ]

    return _prompt_select(f"Файл {filepath} уже существует. Что делать?", choices)


def select_output_directory(default_dir):
    choices = [
        Choice(value="default", name=f"В сканируемую директорию ({default_dir})"),
        Choice(value="custom", name="Указать другую директорию"),
    ]

    result = _prompt_select("Куда сохранить отчёт?", choices)

    if result == BACK_VALUE:
        return BACK_VALUE

    if result == "default":
        return str(default_dir)

    if result == "custom":
        return _prompt_filepath("Укажите директорию для сохранения:", only_directories=True)

    return BACK_VALUE


def select_profile(profiles):
    if not profiles:
        console.print("[bold red]Нет сохранённых профилей[/bold red]")
        return BACK_VALUE

    choices = [Choice(value=p, name=p) for p in profiles]

    return _prompt_select("Выберите профиль:", choices)


def input_profile_name():
    return _prompt_text(
        "Название профиля:",
        validate=lambda name: len(name.strip()) > 0,
        invalid_message="Название не может быть пустым",
    )


def settings_menu():
    choices = [
        Choice(value="save", name="Сохранить текущий профиль"),
        Choice(value="load", name="Загрузить профиль"),
        Choice(value="delete", name="Удалить профиль"),
        Choice(value="list", name="Список профилей"),
    ]

    return _prompt_select("Настройки:", choices)


def select_copy_to_clipboard():
    return _prompt_confirm("Скопировать результат в буфер обмена?", default=False)


def select_files_from_list(files):
    if not files:
        console.print("[bold red]Нет файлов для выбора[/bold red]")
        return BACK_VALUE

    choices = [
        Choice(
            value=f,
            name=f"📄 {f.relative_to(f.parent.parent) if len(f.parts) > 2 else f.name} ({f.suffix})",
        )
        for f in files
    ]

    return _prompt_checkbox(
        "Выберите файлы (Пробел — отметить, Enter — подтвердить):",
        choices,
        validate=lambda result: len(result) > 0,
        invalid_message="Выберите хотя бы один файл",
    )


def select_file_filter_mode():
    choices = [
        Choice(value="all_text", name="Все текстовые файлы"),
        Choice(value="all_files", name="Все файлы (включая бинарные)"),
        Choice(value="extension", name="Фильтр по расширению (.py, .docx, ...)"),
        Choice(value="search", name="Поиск по имени"),
    ]

    return _prompt_select("Как отфильтровать файлы?", choices)


def input_extensions():
    return _prompt_text(
        "Введите расширения через запятую (например: .py, .js, .txt):",
        validate=lambda val: len(val.strip()) > 0,
        invalid_message="Введите хотя бы одно расширение",
    )


def input_search_query():
    return _prompt_text(
        "Введите часть имени файла для поиска:",
        validate=lambda val: len(val.strip()) > 0,
        invalid_message="Поисковый запрос не может быть пустым",
    )


def select_pdf_source_mode():
    choices = [
        Choice(value="session", name="Из сохранённой сессии (структурированная конвертация)"),
        Choice(value="file", name="Из PDF файла (извлечение текста)"),
    ]

    return _prompt_select("Источник для конвертации:", choices)