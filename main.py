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
    input_file_path,
    input_filename,
    input_profile_name,
    select_export_format,
    select_convert_format,
    select_output_directory,
    select_pdf_source_mode,
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
    collect_all_files,
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
from src.converter import detect_modification, convert_pdf_to_format
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
        new_name = input_filename()
        if is_back(new_name):
            return BACK_VALUE
        return new_name

    return BACK_VALUE


def handle_post_export(output_file):
    copy_choice = select_copy_to_clipboard()

    if is_back(copy_choice) or not copy_choice:
        return

    if copy_to_clipboard(output_file):
        console.print("[green]✓ Скопировано в буфер обмена[/green]")
    else:
        console.print("[red]✗ Не удалось скопировать[/red]")


def handle_scan(profile_settings=None):
    state = {
        "mode": None,
        "root_path": None,
        "scan_results": None,
        "include_tree": None,
        "processed_results": None,
        "filename": None,
        "export_format": None,
        "output_dir": None,
    }

    if profile_settings:
        state["mode"] = profile_settings.get("mode", "single")
        state["root_path"] = profile_settings.get("root_path")
        state["include_tree"] = profile_settings.get("include_tree", True)
        state["export_format"] = profile_settings.get("export_format", "txt")
        state["output_dir"] = profile_settings.get("output_dir")
        step = 3
    else:
        step = 1

    while True:
        if step == 1:
            mode = select_directory_mode()
            if is_back(mode):
                return
            state["mode"] = mode
            step = 2

        elif step == 2:
            root_path = input_directory_path()
            if is_back(root_path):
                step = 1
                continue
            state["root_path"] = root_path
            step = 3

        elif step == 3:
            scan_results = []

            if state["mode"] == "single":
                result = scan_directory(state["root_path"])
                if result:
                    scan_results.append(result)

            elif state["mode"] == "multi":
                subdirs = get_subdirectories(state["root_path"])
                selected = select_multiple_directories(subdirs)
                if is_back(selected):
                    step = 2
                    continue
                for directory in selected:
                    result = scan_directory(directory)
                    if result:
                        scan_results.append(result)

            elif state["mode"] == "recursive":
                result = scan_directory(state["root_path"])
                if result:
                    scan_results.append(result)

            if not scan_results:
                console.print("[bold red]Нет данных для записи[/bold red]")
                step = 2
                continue

            state["scan_results"] = scan_results

            for result in scan_results:
                tree = build_tree_view(result)
                console.print(tree)
                show_preview(result)

            step = 4

        elif step == 4:
            proceed = confirm_action("Продолжить запись?")
            if is_back(proceed) or not proceed:
                console.print("[yellow]Операция отменена[/yellow]")
                step = 2
                continue
            step = 5

        elif step == 5:
            if state["include_tree"] is None:
                include_tree = toggle_tree_view()
                if is_back(include_tree):
                    step = 4
                    continue
                state["include_tree"] = include_tree
            step = 6

        elif step == 6:
            use_redaction = toggle_redaction()
            if is_back(use_redaction):
                state["include_tree"] = None
                step = 5
                continue

            if not use_redaction:
                state["processed_results"] = list(state["scan_results"])
                step = 7
                continue

            available = get_available_patterns()
            selected_patterns = select_redaction_patterns(available)
            if is_back(selected_patterns):
                state["include_tree"] = None
                step = 5
                continue

            processed_results = []
            for result in state["scan_results"]:
                redacted_result, findings = redact_scan_result(result, selected_patterns)

                if findings:
                    console.print("\n[bold yellow]⚠ Найдены конфиденциальные данные:[/bold yellow]")
                    for item in findings:
                        console.print(f"  [dim]📄 {item['file']}[/dim]")
                        for f in item["findings"]:
                            console.print(f"    [red]• {f['pattern']}: {f['count']} совпадений[/red]")

                processed_results.append(redacted_result)

            if any(
                any(len(r.get("files", [])) > 0 for r in [result])
                for result in state["scan_results"]
            ):
                console.print("[green]Цензура применена[/green]\n")
            else:
                console.print("[green]Конфиденциальных данных не обнаружено[/green]\n")

            state["processed_results"] = processed_results
            step = 7

        elif step == 7:
            filename = input_filename()
            if is_back(filename):
                step = 6
                continue
            state["filename"] = filename
            step = 8

        elif step == 8:
            if state["export_format"] is None:
                export_format = select_export_format()
                if is_back(export_format):
                    step = 7
                    continue
                state["export_format"] = export_format
            step = 9

        elif step == 9:
            if state["output_dir"] is None:
                default_dir = state["processed_results"][0]["root"]
                output_dir = select_output_directory(default_dir)
                if is_back(output_dir):
                    state["export_format"] = None
                    step = 8
                    continue
                state["output_dir"] = output_dir
            step = 10

        elif step == 10:
            output_path = Path(state["output_dir"])
            output_path.mkdir(parents=True, exist_ok=True)

            go_back = False
            for result in state["processed_results"]:
                final_name = handle_filename_conflict(
                    state["output_dir"], state["filename"], state["export_format"]
                )
                if is_back(final_name):
                    go_back = True
                    break

                output_file = export(
                    result, final_name, state["export_format"],
                    state["output_dir"], state["include_tree"]
                )
                save_session(result, report_path=output_file)
                console.print(f"[bold green]✓ Отчёт создан: {output_file}[/bold green]")
                handle_post_export(output_file)

            if go_back:
                state["output_dir"] = None
                step = 9
                continue

            return


def handle_convert():
    console.print("[bold cyan]Конвертация[/bold cyan]\n")

    step = 1
    state = {
        "source_mode": None,
        "root_path": None,
        "selected_session": None,
        "session_data": None,
        "pdf_path": None,
        "target_format": None,
        "include_tree": None,
        "scan_data": None,
        "filename": None,
        "output_dir": None,
    }

    while True:
        if step == 1:
            source_mode = select_pdf_source_mode()
            if is_back(source_mode):
                return
            state["source_mode"] = source_mode

            if source_mode == "file":
                step = 20
            else:
                step = 2

        elif step == 2:
            root_path = input_directory_path()
            if is_back(root_path):
                step = 1
                continue
            state["root_path"] = root_path
            step = 3

        elif step == 3:
            sessions = list_sessions_in_directory(state["root_path"])

            if not sessions:
                console.print("[bold red]Сессии не найдены. Сначала выполните сканирование.[/bold red]")
                step = 2
                continue

            selected = select_session(sessions)
            if is_back(selected):
                step = 2
                continue

            session_data = load_session(selected)

            if session_data is None:
                console.print("[bold red]Не удалось загрузить сессию[/bold red]")
                step = 2
                continue

            state["selected_session"] = selected
            state["session_data"] = session_data

            report_path = session_data.get("report_path")

            if report_path:
                status = detect_modification(report_path, selected)

                if status == "modified":
                    console.print("[bold yellow]⚠ Отчёт был изменён вручную[/bold yellow]")
                    action = select_modification_action()
                    if is_back(action):
                        step = 2
                        continue

                    if action == "rescan":
                        scan_result = scan_directory(session_data["scan_data"]["root"])
                        if scan_result is None:
                            console.print("[bold red]Ошибка пересканирования[/bold red]")
                            step = 2
                            continue
                        state["session_data"]["scan_data"] = scan_result

                elif status == "file_missing":
                    console.print("[bold yellow]⚠ Исходный файл отчёта не найден[/bold yellow]")

            step = 4

        elif step == 4:
            current_format = "txt"
            report_path = state["session_data"].get("report_path")
            if report_path:
                current_format = Path(report_path).suffix.lstrip(".")

            target_format = select_convert_format(current_format)
            if is_back(target_format):
                step = 3
                continue
            state["target_format"] = target_format
            step = 5

        elif step == 5:
            include_tree = toggle_tree_view()
            if is_back(include_tree):
                step = 4
                continue
            state["include_tree"] = include_tree
            step = 6

        elif step == 6:
            use_redaction = toggle_redaction()
            if is_back(use_redaction):
                step = 5
                continue

            scan_data = state["session_data"]["scan_data"]

            if not use_redaction:
                state["scan_data"] = scan_data
                step = 7
                continue

            available = get_available_patterns()
            selected_patterns = select_redaction_patterns(available)
            if is_back(selected_patterns):
                step = 5
                continue

            redacted_result, findings = redact_scan_result(scan_data, selected_patterns)

            if findings:
                console.print("\n[bold yellow]⚠ Найдены конфиденциальные данные:[/bold yellow]")
                for item in findings:
                    console.print(f"  [dim]📄 {item['file']}[/dim]")
                    for f in item["findings"]:
                        console.print(f"    [red]• {f['pattern']}: {f['count']} совпадений[/red]")
                console.print("[green]Цензура применена[/green]\n")
            else:
                console.print("[green]Конфиденциальных данных не обнаружено[/green]\n")

            state["scan_data"] = redacted_result
            step = 7

        elif step == 7:
            filename = input_filename()
            if is_back(filename):
                step = 6
                continue
            state["filename"] = filename
            step = 8

        elif step == 8:
            default_dir = str(state["selected_session"])
            output_dir = select_output_directory(default_dir)
            if is_back(output_dir):
                step = 7
                continue
            state["output_dir"] = output_dir
            step = 9

        elif step == 9:
            output_path = Path(state["output_dir"])
            output_path.mkdir(parents=True, exist_ok=True)

            final_name = handle_filename_conflict(
                state["output_dir"], state["filename"], state["target_format"]
            )
            if is_back(final_name):
                step = 8
                continue

            output_file = export(
                state["scan_data"], final_name, state["target_format"],
                state["output_dir"], state["include_tree"]
            )
            save_session(state["scan_data"], state["output_dir"], output_file)
            console.print(f"[bold green]✓ Конвертация завершена: {output_file}[/bold green]")
            handle_post_export(output_file)
            return

        elif step == 20:
            pdf_path = input_file_path()
            if is_back(pdf_path):
                step = 1
                continue

            pdf_file = Path(pdf_path)
            if not pdf_file.exists() or pdf_file.suffix.lower() != ".pdf":
                console.print("[bold red]Файл не найден или это не PDF[/bold red]")
                continue

            state["pdf_path"] = pdf_path
            step = 21

        elif step == 21:
            target_format = select_convert_format("pdf")
            if is_back(target_format):
                step = 20
                continue
            state["target_format"] = target_format
            step = 22

        elif step == 22:
            filename = input_filename()
            if is_back(filename):
                step = 21
                continue
            state["filename"] = filename
            step = 23

        elif step == 23:
            default_dir = str(Path(state["pdf_path"]).parent)
            output_dir = select_output_directory(default_dir)
            if is_back(output_dir):
                step = 22
                continue
            state["output_dir"] = output_dir
            step = 24

        elif step == 24:
            output_path = Path(state["output_dir"])
            output_path.mkdir(parents=True, exist_ok=True)

            final_name = handle_filename_conflict(
                state["output_dir"], state["filename"], state["target_format"]
            )
            if is_back(final_name):
                step = 23
                continue

            output_file = convert_pdf_to_format(
                state["pdf_path"], final_name,
                state["target_format"], state["output_dir"]
            )

            if output_file:
                console.print(f"[bold green]✓ PDF конвертирован: {output_file}[/bold green]")
                handle_post_export(output_file)
            else:
                console.print("[bold red]Ошибка конвертации PDF[/bold red]")

            return


def handle_reconvert():
    console.print("[bold cyan]Переконвертация существующего отчёта[/bold cyan]\n")
    handle_convert()


def handle_delete():
    console.print("[bold cyan]Удаление записи[/bold cyan]\n")

    step = 1
    state = {
        "root_path": None,
        "selected_session": None,
    }

    while True:
        if step == 1:
            root_path = input_directory_path()
            if is_back(root_path):
                return
            state["root_path"] = root_path
            step = 2

        elif step == 2:
            sessions = list_sessions_in_directory(state["root_path"])

            if not sessions:
                console.print("[bold red]Сессии не найдены[/bold red]")
                step = 1
                continue

            selected = select_session(sessions)
            if is_back(selected):
                step = 1
                continue

            state["selected_session"] = selected
            step = 3

        elif step == 3:
            report_files = find_report_files(state["selected_session"])

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
                    step = 2
                    continue

                for file in selected_files:
                    confirm = confirm_action(f"Удалить файл {file.name}?")
                    if is_back(confirm):
                        step = 2
                        break

                    if confirm:
                        try:
                            file.unlink()
                            console.print(f"[green]✓ Удалён: {file.name}[/green]")
                        except OSError as e:
                            console.print(f"[bold red]Ошибка удаления {file.name}: {e}[/bold red]")
                    else:
                        console.print(f"[yellow]Пропущен: {file.name}[/yellow]")

            session_dir = Path(state["selected_session"]) / ".context_builder"

            if session_dir.exists():
                confirm = confirm_action("Удалить также данные сессии (.context_builder)?")
                if is_back(confirm):
                    step = 2
                    continue

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

            return


def handle_select_files():
    console.print("[bold cyan]Выбор файлов в директориях[/bold cyan]\n")

    step = 1
    state = {
        "root_path": None,
        "all_files": None,
        "filtered": None,
        "selected_files": None,
        "scan_result": None,
        "include_tree": None,
        "filename": None,
        "export_format": None,
        "output_dir": None,
    }

    while True:
        if step == 1:
            root_path = input_directory_path()
            if is_back(root_path):
                return
            state["root_path"] = root_path

            console.print("[dim]Сканирование файлов...[/dim]")
            all_files = collect_text_files(root_path)

            if not all_files:
                all_files = collect_all_files(root_path)

            if not all_files:
                console.print("[bold red]Файлы не найдены[/bold red]")
                return

            state["all_files"] = all_files
            console.print(f"[green]Найдено файлов: {len(all_files)}[/green]\n")
            step = 2

        elif step == 2:
            filter_mode = select_file_filter_mode()
            if is_back(filter_mode):
                step = 1
                continue

            if filter_mode == "all_text":
                filtered = state["all_files"]

            elif filter_mode == "all_files":
                filtered = collect_all_files(state["root_path"])
                if not filtered:
                    console.print("[bold red]Файлы не найдены[/bold red]")
                    continue
                console.print(f"[green]Найдено всего файлов: {len(filtered)}[/green]\n")

            elif filter_mode == "extension":
                raw = input_extensions()
                if is_back(raw):
                    continue

                extensions = [e.strip() for e in raw.split(",")]
                all_for_filter = collect_all_files(state["root_path"])
                filtered = filter_by_extensions(all_for_filter, extensions)

                if not filtered:
                    console.print("[bold red]Файлы с указанными расширениями не найдены[/bold red]")
                    continue

                console.print(f"[green]После фильтрации: {len(filtered)} файлов[/green]\n")

            elif filter_mode == "search":
                query = input_search_query()
                if is_back(query):
                    continue

                all_for_search = collect_all_files(state["root_path"])
                filtered = filter_by_name(all_for_search, query)

                if not filtered:
                    console.print(f"[bold red]Файлы с '{query}' в имени не найдены[/bold red]")
                    continue

                console.print(f"[green]Найдено по запросу: {len(filtered)} файлов[/green]\n")

            else:
                continue

            state["filtered"] = filtered
            step = 3

        elif step == 3:
            selected_files = select_files_from_list(state["filtered"])
            if is_back(selected_files):
                step = 2
                continue

            state["selected_files"] = selected_files
            console.print(f"\n[bold]Выбрано файлов: {len(selected_files)}[/bold]")

            scan_result = scan_selected_files(selected_files, state["root_path"])
            state["scan_result"] = scan_result

            tree = build_tree_view(scan_result)
            console.print(tree)
            show_preview(scan_result)

            step = 4

        elif step == 4:
            proceed = confirm_action("Продолжить запись?")
            if is_back(proceed) or not proceed:
                console.print("[yellow]Операция отменена[/yellow]")
                step = 3
                continue
            step = 5

        elif step == 5:
            include_tree = toggle_tree_view()
            if is_back(include_tree):
                step = 4
                continue
            state["include_tree"] = include_tree
            step = 6

        elif step == 6:
            use_redaction = toggle_redaction()
            if is_back(use_redaction):
                step = 5
                continue

            if not use_redaction:
                step = 7
                continue

            available = get_available_patterns()
            selected_patterns = select_redaction_patterns(available)
            if is_back(selected_patterns):
                step = 5
                continue

            redacted_result, findings = redact_scan_result(state["scan_result"], selected_patterns)

            if findings:
                console.print("\n[bold yellow]⚠ Найдены конфиденциальные данные:[/bold yellow]")
                for item in findings:
                    console.print(f"  [dim]📄 {item['file']}[/dim]")
                    for f in item["findings"]:
                        console.print(f"    [red]• {f['pattern']}: {f['count']} совпадений[/red]")
                console.print("[green]Цензура применена[/green]\n")
            else:
                console.print("[green]Конфиденциальных данных не обнаружено[/green]\n")

            state["scan_result"] = redacted_result
            step = 7

        elif step == 7:
            filename = input_filename()
            if is_back(filename):
                step = 6
                continue
            state["filename"] = filename
            step = 8

        elif step == 8:
            export_format = select_export_format()
            if is_back(export_format):
                step = 7
                continue
            state["export_format"] = export_format
            step = 9

        elif step == 9:
            output_dir = select_output_directory(state["root_path"])
            if is_back(output_dir):
                step = 8
                continue
            state["output_dir"] = output_dir
            step = 10

        elif step == 10:
            output_path = Path(state["output_dir"])
            output_path.mkdir(parents=True, exist_ok=True)

            final_name = handle_filename_conflict(
                state["output_dir"], state["filename"], state["export_format"]
            )
            if is_back(final_name):
                step = 9
                continue

            output_file = export(
                state["scan_result"], final_name, state["export_format"],
                state["output_dir"], state["include_tree"]
            )
            save_session(state["scan_result"], report_path=output_file)
            console.print(f"[bold green]✓ Отчёт создан: {output_file}[/bold green]")
            handle_post_export(output_file)
            return


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