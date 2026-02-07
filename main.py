from pathlib import Path

from rich.console import Console

from src.menu import (
    show_welcome,
    main_menu,
    select_directory_mode,
    input_directory_path,
    input_filename,
    input_profile_name,
    select_export_format,
    select_convert_format,
    confirm_action,
    select_multiple_directories,
    select_session,
    select_modification_action,
    select_report_files,
    toggle_tree_view,
    toggle_redaction,
    select_redaction_patterns,
    select_overwrite_action,
    select_profile,
    settings_menu,
    select_copy_to_clipboard,
)
from src.scanner import scan_directory, get_subdirectories, build_tree_view
from src.session import (
    save_session,
    load_session,
    list_sessions_in_directory,
    find_report_files,
)
from src.preview import show_preview
from src.exporter import export
from src.converter import detect_modification
from src.redactor import redact_scan_result, get_available_patterns
from src.clipboard import copy_to_clipboard
from src.config import save_profile, load_profile, list_profiles, delete_profile
from src.utils.filename import resolve_filename, generate_unique_filename

console = Console()


def handle_filename_conflict(directory, filename, extension):
    resolved = resolve_filename(directory, filename, extension)

    if resolved is not None:
        return resolved

    existing = Path(directory) / f"{filename}.{extension}"
    action = select_overwrite_action(existing.name)

    if action == "overwrite":
        return filename

    if action == "rename":
        return generate_unique_filename(directory, filename, extension)

    if action == "new_name":
        return input_filename()

    return None


def apply_redaction(scan_result):
    use_redaction = toggle_redaction()

    if not use_redaction:
        return scan_result

    available = get_available_patterns()
    selected_patterns = select_redaction_patterns(available)

    redacted_result, findings = redact_scan_result(scan_result, selected_patterns)

    if findings:
        console.print("\n[bold yellow]⚠ Найдены конфиденциальные данные:[/bold yellow]")
        for item in findings:
            console.print(f"  [dim]📄 {item['file']}[/dim]")
            for f in item["findings"]:
                console.print(f"    [red]• {f['pattern']}: {f['count']} совпадений[/red]")
        console.print("[green]Все совпадения заменены на ***REDACTED***[/green]\n")
    else:
        console.print("[green]Конфиденциальных данных не обнаружено[/green]\n")

    return redacted_result


def handle_post_export(output_file):
    if select_copy_to_clipboard():
        if copy_to_clipboard(output_file):
            console.print("[green]✓ Скопировано в буфер обмена[/green]")
        else:
            console.print("[red]✗ Не удалось скопировать[/red]")


def handle_scan(profile_settings=None):
    if profile_settings:
        mode = profile_settings.get("mode", "single")
        root_path = profile_settings.get("root_path")
        include_tree = profile_settings.get("include_tree", True)
        export_format = profile_settings.get("export_format", "txt")
    else:
        mode = select_directory_mode()
        if mode == "back":
            return
        root_path = input_directory_path()
        include_tree = None
        export_format = None

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

    if include_tree is None:
        include_tree = toggle_tree_view()

    processed_results = []
    for result in scan_results:
        processed = apply_redaction(result)
        processed_results.append(processed)

    filename = input_filename()

    if export_format is None:
        export_format = select_export_format()

    if export_format == "back":
        return

    for result in processed_results:
        output_dir = result["root"]
        final_name = handle_filename_conflict(output_dir, filename, export_format)

        if final_name is None:
            console.print("[yellow]Операция отменена[/yellow]")
            return

        output_file = export(result, final_name, export_format, include_tree=include_tree)
        save_session(result, report_path=output_file)
        console.print(f"[bold green]✓ Отчёт создан: {output_file}[/bold green]")
        handle_post_export(output_file)


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

    include_tree = toggle_tree_view()

    scan_data = apply_redaction(session_data["scan_data"])

    filename = input_filename()

    output_dir = str(selected)
    final_name = handle_filename_conflict(output_dir, filename, target_format)

    if final_name is None:
        console.print("[yellow]Операция отменена[/yellow]")
        return

    output_file = export(scan_data, final_name, target_format, output_dir, include_tree)
    save_session(scan_data, output_dir, output_file)
    console.print(f"[bold green]✓ Конвертация завершена: {output_file}[/bold green]")
    handle_post_export(output_file)


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


def handle_settings():
    while True:
        choice = settings_menu()

        if choice == "← Назад":
            break

        elif choice == "Сохранить текущий профиль":
            name = input_profile_name()
            settings = {
                "mode": "single",
                "root_path": "",
                "include_tree": True,
                "export_format": "txt",
            }

            root = input_directory_path()
            settings["root_path"] = root

            mode = select_directory_mode()
            if mode != "back":
                settings["mode"] = mode

            settings["include_tree"] = toggle_tree_view()
            fmt = select_export_format()
            if fmt != "back":
                settings["export_format"] = fmt

            path = save_profile(name, settings)
            console.print(f"[bold green]✓ Профиль сохранён: {path}[/bold green]")

        elif choice == "Загрузить профиль":
            profiles = list_profiles()
            selected = select_profile(profiles)

            if selected and selected != "back":
                settings = load_profile(selected)
                if settings:
                    console.print(f"[green]✓ Профиль '{selected}' загружен[/green]")
                    handle_scan(profile_settings=settings)
                else:
                    console.print("[red]Ошибка загрузки профиля[/red]")

        elif choice == "Удалить профиль":
            profiles = list_profiles()
            selected = select_profile(profiles)

            if selected and selected != "back":
                if confirm_action(f"Удалить профиль '{selected}'?"):
                    if delete_profile(selected):
                        console.print(f"[green]✓ Профиль '{selected}' удалён[/green]")
                    else:
                        console.print("[red]Профиль не найден[/red]")

        elif choice == "Список профилей":
            profiles = list_profiles()
            if profiles:
                console.print("\n[bold]Сохранённые профили:[/bold]")
                for p in profiles:
                    console.print(f"  [cyan]• {p}[/cyan]")
                console.print("")
            else:
                console.print("[yellow]Нет сохранённых профилей[/yellow]")


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
            console.print("[yellow]Будет доступно позже[/yellow]")
        elif choice == "Настройки":
            handle_settings()
        elif choice == "Выход":
            console.print("[bold cyan]До свидания![/bold cyan]")
            break


if __name__ == "__main__":
    main()