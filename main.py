import sys
from pathlib import Path

from rich.console import Console

from src.menu import (
    BACK_VALUE,
    EXIT_VALUE,
    show_welcome,
    main_menu,
    select_directory_mode,
    input_directory_path,
    input_filename,
    input_profile_name,
    select_export_format,
    select_convert_format,
    select_output_directory,
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
    select_files_from_list,
    select_file_filter_mode,
    input_extensions,
    input_search_query,
)
from src.scanner import (
    scan_directory,
    get_subdirectories,
    build_tree_view,
    collect_text_files,
    scan_selected_files,
    filter_by_extensions,
    filter_by_name,
)
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


def is_back(value):
    return value is None or value == BACK_VALUE


def handle_filename_conflict(directory, filename, extension):
    resolved = resolve_filename(directory, filename, extension)

    if resolved is not None:
        return resolved

    existing = Path(directory) / f"{filename}.{extension}"
    action = select_overwrite_action(existing.name)

    if is_back(action):
        return BACK_VALUE

    if action == "overwrite":
        return filename

    if action == "rename":
        return generate_unique_filename(directory, filename, extension)

    if action == "new_name":
        return input_filename()

    return BACK_VALUE


def apply_redaction(scan_result):
    use_redaction = toggle_redaction()

    if is_back(use_redaction):
        return BACK_VALUE

    if not use_redaction:
        return scan_result

    available = get_available_patterns()
    selected_patterns = select_redaction_patterns(available)

    if is_back(selected_patterns):
        return BACK_VALUE

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
    copy_choice = select_copy_to_clipboard()

    if is_back(copy_choice) or not copy_choice:
        return

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
        output_dir = profile_settings.get("output_dir")
    else:
        mode = select_directory_mode()
        if is_back(mode):
            return

        root_path = input_directory_path()
        if is_back(root_path):
            return

        include_tree = None
        export_format = None
        output_dir = None

    scan_results = []

    if mode == "single":
        result = scan_directory(root_path)
        if result:
            scan_results.append(result)

    elif mode == "multi":
        subdirs = get_subdirectories(root_path)
        selected = select_multiple_directories(subdirs)
        if is_back(selected):
            return
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

    proceed = confirm_action("Продолжить запись?")
    if is_back(proceed) or not proceed:
        console.print("[yellow]Операция отменена[/yellow]")
        return

    if include_tree is None:
        include_tree = toggle_tree_view()
        if is_back(include_tree):
            return

    processed_results = []
    for result in scan_results:
        processed = apply_redaction(result)
        if is_back(processed):
            return
        processed_results.append(processed)

    filename = input_filename()
    if is_back(filename):
        return

    if export_format is None:
        export_format = select_export_format()
        if is_back(export_format):
            return

    if output_dir is None:
        default_dir = processed_results[0]["root"]
        output_dir = select_output_directory(default_dir)
        if is_back(output_dir):
            return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for result in processed_results:
        final_name = handle_filename_conflict(output_dir, filename, export_format)
        if is_back(final_name):
            return

        output_file = export(result, final_name, export_format, output_dir, include_tree)
        save_session(result, report_path=output_file)
        console.print(f"[bold green]✓ Отчёт создан: {output_file}[/bold green]")
        handle_post_export(output_file)


def handle_convert():
    console.print("[bold cyan]Конвертация из существующей сессии[/bold cyan]\n")

    root_path = input_directory_path()
    if is_back(root_path):
        return

    sessions = list_sessions_in_directory(root_path)

    if not sessions:
        console.print("[bold red]Сессии не найдены. Сначала выполните сканирование.[/bold red]")
        return

    selected = select_session(sessions)
    if is_back(selected):
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
            if is_back(action):
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
    if is_back(target_format):
        return

    include_tree = toggle_tree_view()
    if is_back(include_tree):
        return

    scan_data = apply_redaction(session_data["scan_data"])
    if is_back(scan_data):
        return

    filename = input_filename()
    if is_back(filename):
        return

    default_dir = str(selected)
    output_dir = select_output_directory(default_dir)
    if is_back(output_dir):
        return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    final_name = handle_filename_conflict(output_dir, filename, target_format)
    if is_back(final_name):
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
    if is_back(root_path):
        return

    sessions = list_sessions_in_directory(root_path)

    if not sessions:
        console.print("[bold red]Сессии не найдены[/bold red]")
        return

    selected = select_session(sessions)
    if is_back(selected):
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
        if is_back(selected_files):
            return

        for file in selected_files:
            confirm = confirm_action(f"Удалить файл {file.name}?")
            if is_back(confirm):
                return

            if confirm:
                try:
                    file.unlink()
                    console.print(f"[green]✓ Удалён: {file.name}[/green]")
                except OSError as e:
                    console.print(f"[bold red]Ошибка удаления {file.name}: {e}[/bold red]")
            else:
                console.print(f"[yellow]Пропущен: {file.name}[/yellow]")

    session_dir = Path(selected) / ".context_builder"

    if session_dir.exists():
        confirm = confirm_action("Удалить также данные сессии (.context_builder)?")
        if is_back(confirm):
            return

        if confirm:
            try:
                for file in session_dir.iterdir():
                    file.unlink()
                session_dir.rmdir()
                console.print("[green]✓ Сессия удалена[/green]")
            except OSError as e:
                console.print(f"[bold red]Ошибка удаления сессии: {e}[/bold red]")
        else:
            console.print("[yellow]Данные сессии сохранены[/yellow]")


def handle_select_files():
    console.print("[bold cyan]Выбор файлов в директориях[/bold cyan]\n")

    root_path = input_directory_path()
    if is_back(root_path):
        return

    console.print("[dim]Сканирование файлов...[/dim]")
    all_files = collect_text_files(root_path)

    if not all_files:
        console.print("[bold red]Текстовые файлы не найдены[/bold red]")
        return

    console.print(f"[green]Найдено файлов: {len(all_files)}[/green]\n")

    filter_mode = select_file_filter_mode()
    if is_back(filter_mode):
        return

    if filter_mode == "all":
        filtered = all_files

    elif filter_mode == "extension":
        raw = input_extensions()
        if is_back(raw):
            return

        extensions = [e.strip() for e in raw.split(",")]
        filtered = filter_by_extensions(all_files, extensions)

        if not filtered:
            console.print("[bold red]Файлы с указанными расширениями не найдены[/bold red]")
            return

        console.print(f"[green]После фильтрации: {len(filtered)} файлов[/green]\n")

    elif filter_mode == "search":
        query = input_search_query()
        if is_back(query):
            return

        filtered = filter_by_name(all_files, query)

        if not filtered:
            console.print(f"[bold red]Файлы с '{query}' в имени не найдены[/bold red]")
            return

        console.print(f"[green]Найдено по запросу: {len(filtered)} файлов[/green]\n")

    else:
        return

    selected_files = select_files_from_list(filtered)
    if is_back(selected_files):
        return

    console.print(f"\n[bold]Выбрано файлов: {len(selected_files)}[/bold]")

    scan_result = scan_selected_files(selected_files, root_path)

    tree = build_tree_view(scan_result)
    console.print(tree)
    show_preview(scan_result)

    proceed = confirm_action("Продолжить запись?")
    if is_back(proceed) or not proceed:
        console.print("[yellow]Операция отменена[/yellow]")
        return

    include_tree = toggle_tree_view()
    if is_back(include_tree):
        return

    scan_result = apply_redaction(scan_result)
    if is_back(scan_result):
        return

    filename = input_filename()
    if is_back(filename):
        return

    export_format = select_export_format()
    if is_back(export_format):
        return

    output_dir = select_output_directory(root_path)
    if is_back(output_dir):
        return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    final_name = handle_filename_conflict(output_dir, filename, export_format)
    if is_back(final_name):
        return

    output_file = export(scan_result, final_name, export_format, output_dir, include_tree)
    save_session(scan_result, report_path=output_file)
    console.print(f"[bold green]✓ Отчёт создан: {output_file}[/bold green]")
    handle_post_export(output_file)


def handle_settings():
    while True:
        choice = settings_menu()

        if is_back(choice):
            break

        elif choice == "save":
            name = input_profile_name()
            if is_back(name):
                continue

            settings = {
                "mode": "single",
                "root_path": "",
                "include_tree": True,
                "export_format": "txt",
                "output_dir": None,
            }

            root = input_directory_path()
            if is_back(root):
                continue
            settings["root_path"] = root

            mode = select_directory_mode()
            if not is_back(mode):
                settings["mode"] = mode

            tree = toggle_tree_view()
            if not is_back(tree):
                settings["include_tree"] = tree

            fmt = select_export_format()
            if not is_back(fmt):
                settings["export_format"] = fmt

            out_dir = select_output_directory(root)
            if not is_back(out_dir):
                settings["output_dir"] = out_dir

            path = save_profile(name, settings)
            console.print(f"[bold green]✓ Профиль сохранён: {path}[/bold green]")

        elif choice == "load":
            profiles = list_profiles()
            selected = select_profile(profiles)

            if not is_back(selected):
                settings = load_profile(selected)
                if settings:
                    console.print(f"[green]✓ Профиль '{selected}' загружен[/green]")
                    handle_scan(profile_settings=settings)
                else:
                    console.print("[red]Ошибка загрузки профиля[/red]")

        elif choice == "delete":
            profiles = list_profiles()
            selected = select_profile(profiles)

            if not is_back(selected):
                confirm = confirm_action(f"Удалить профиль '{selected}'?")
                if not is_back(confirm) and confirm:
                    if delete_profile(selected):
                        console.print(f"[green]✓ Профиль '{selected}' удалён[/green]")
                    else:
                        console.print("[red]Профиль не найден[/red]")

        elif choice == "list":
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

        if choice == "scan":
            handle_scan()
        elif choice == "convert":
            handle_convert()
        elif choice == "reconvert":
            handle_reconvert()
        elif choice == "delete":
            handle_delete()
        elif choice == "files":
            handle_select_files()
        elif choice == "settings":
            handle_settings()
        elif choice == EXIT_VALUE or is_back(choice):
            console.print("[bold cyan]До свидания![/bold cyan]")
            break


if __name__ == "__main__":
    if "--gui" in sys.argv:
        from gui import run_gui
        run_gui()
    elif len(sys.argv) > 1:
        from src.cli import run_cli
        run_cli()
    else:
        main()