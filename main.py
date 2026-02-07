from rich.console import Console

from src.menu import (
    show_welcome,
    main_menu,
    select_directory_mode,
    input_directory_path,
    input_filename,
    select_export_format,
    confirm_action,
    select_multiple_directories,
)
from src.scanner import scan_directory, get_subdirectories, build_tree_view
from src.session import save_session
from src.preview import show_preview

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
        session_file = save_session(result)
        console.print(f"[green]✓ Сессия сохранена: {session_file}[/green]")

    console.print(
        f"[bold green]✓ Запись завершена: {filename}.{export_format}[/bold green]"
    )


def main():
    show_welcome()

    while True:
        choice = main_menu()

        if choice == "Сканирование (Запись)":
            handle_scan()
        elif choice == "Конвертация":
            console.print("[yellow]Будет доступно в Фазе 2[/yellow]")
        elif choice == "Переконвертация":
            console.print("[yellow]Будет доступно в Фазе 2[/yellow]")
        elif choice == "Удаление записи":
            console.print("[yellow]Будет доступно в Фазе 2[/yellow]")
        elif choice == "Выбор файлов в директориях":
            console.print("[yellow]Будет доступно в Фазе 3[/yellow]")
        elif choice == "Настройки":
            console.print("[yellow]Будет доступно в Фазе 3[/yellow]")
        elif choice == "Выход":
            console.print("[bold cyan]До свидания![/bold cyan]")
            break


if __name__ == "__main__":
    main()