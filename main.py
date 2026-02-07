from pathlib import Path

from rich.console import Console

from src.menu import (
    show_welcome,
    main_menu,
    select_directory_mode,
    input_directory_path,
    input_filename,
    select_export_format,
    select_convert_format,
    confirm_action,
    select_multiple_directories,
    select_session,
    select_modification_action,
)
from src.scanner import scan_directory, get_subdirectories, build_tree_view
from src.session import save_session, load_session, list_sessions_in_directory
from src.preview import show_preview
from src.exporter import export
from src.converter import convert_from_session, detect_modification

console = Console()


def handle_scan():
    mode = select_directory_mode()

    if mode == "back":
        return

    root_path = input_directory_path()
    scan_results = []

    if mode == "single":
        result = scan_directory(root_path)
        if result:
            scan_results.append(result)

    elif mode == "multi":
        subdirs = get_subdirectories(root_path)
        selected = select_multiple_directories(subdirs)
        for directory in selected:
            result = scan_directory(directory)
            if result:
                scan_results.append(result)

    elif mode == "recursive":
        result = scan_directory(root_path)
        if result:
            scan_results.append(result)

    if not scan_results:
        console.print("[bold red]Нет данных для записи[/bold red]")
        return

    for result in scan_results:
        tree = build_tree_view(result)
        console.print(tree)
        show_preview(result)

    if not confirm_action("Продолжить запись?"):
        console.print("[yellow]Операция отменена[/yellow]")
        return

    filename = input_filename()
    export_format = select_export_format()

    if export_format == "back":
        return

    for result in scan_results:
        output_file = export(result, filename, export_format)
        save_session(result, report_path=output_file)
        console.print(f"[bold green]✓ Отчёт создан: {output_file}[/bold green]")


def handle_convert():
    console.print("[bold cyan]Конвертация из существующей сессии[/bold cyan]\n")

    root_path = input_directory_path()
    sessions = list_sessions_in_directory(root_path)

    if not sessions:
        console.print("[bold red]Сессии не найдены. Сначала выполните сканирование.[/bold red]")
        return

    selected = select_session(sessions)

    if selected == "back" or selected is None:
        return

    session_data = load_session(selected)

    if session_data is None:
        console.print("[bold red]Не удалось загрузить сессию[/bold red]")
        return

    report_path = session_data.get("report_path")

    if report_path:
        status = detect_modification(report_path, selected)

        if status == "modified":
            console.print("[bold yellow]⚠ Отчёт был изменён вручную[/bold yellow]")
            action = select_modification_action()

            if action == "back":
                return

            if action == "rescan":
                scan_result = scan_directory(session_data["scan_data"]["root"])
                if scan_result is None:
                    console.print("[bold red]Ошибка пересканирования[/bold red]")
                    return
                session_data["scan_data"] = scan_result

        elif status == "file_missing":
            console.print("[bold yellow]⚠ Исходный файл отчёта не найден[/bold yellow]")

    current_format = "txt"
    if report_path:
        current_format = Path(report_path).suffix.lstrip(".")

    target_format = select_convert_format(current_format)

    if target_format == "back":
        return

    filename = input_filename()
    output_file = export(session_data["scan_data"], filename, target_format, str(selected))

    save_session(session_data["scan_data"], str(selected), output_file)
    console.print(f"[bold green]✓ Конвертация завершена: {output_file}[/bold green]")


def handle_reconvert():
    console.print("[bold cyan]Переконвертация существующего отчёта[/bold cyan]\n")
    handle_convert()


def handle_delete():
    console.print("[bold cyan]Удаление записи[/bold cyan]\n")

    root_path = input_directory_path()
    sessions = list_sessions_in_directory(root_path)

    if not sessions:
        console.print("[bold red]Сессии не найдены[/bold red]")
        return

    selected = select_session(sessions)

    if selected == "back" or selected is None:
        return

    from src.session import find_report_files
    from src.menu import select_report_files

    report_files = find_report_files(selected)

    if not report_files:
        console.print("[bold yellow]Файлы отчётов не найдены в директории[/bold yellow]")
    else:
        console.print(f"\n[bold]Найдено файлов: {len(report_files)}[/bold]\n")

        for f in report_files:
            size_kb = f.stat().st_size / 1024
            console.print(f"  [dim]📄 {f.name} ({size_kb:.1f} KB)[/dim]")

        console.print("")

        selected_files = select_report_files(report_files)

        for file in selected_files:
            if confirm_action(f"Удалить файл {file.name}?"):
                try:
                    file.unlink()
                    console.print(f"[green]✓ Удалён: {file.name}[/green]")
                except OSError as e:
                    console.print(f"[bold red]Ошибка удаления {file.name}: {e}[/bold red]")
            else:
                console.print(f"[yellow]Пропущен: {file.name}[/yellow]")

    session_dir = Path(selected) / ".context_builder"

    if session_dir.exists():
        if confirm_action("Удалить также данные сессии (.context_builder)?"):
            try:
                for file in session_dir.iterdir():
                    file.unlink()
                session_dir.rmdir()
                console.print("[green]✓ Сессия удалена[/green]")
            except OSError as e:
                console.print(f"[bold red]Ошибка удаления сессии: {e}[/bold red]")
        else:
            console.print("[yellow]Данные сессии сохранены[/yellow]")


def main():
    show_welcome()

    while True:
        choice = main_menu()

        if choice == "Сканирование (Запись)":
            handle_scan()
        elif choice == "Конвертация":
            handle_convert()
        elif choice == "Переконвертация":
            handle_reconvert()
        elif choice == "Удаление записи":
            handle_delete()
        elif choice == "Выбор файлов в директориях":
            console.print("[yellow]Будет доступно в Фазе 3[/yellow]")
        elif choice == "Настройки":
            console.print("[yellow]Будет доступно в Фазе 3[/yellow]")
        elif choice == "Выход":
            console.print("[bold cyan]До свидания![/bold cyan]")
            break


if __name__ == "__main__":
    main()