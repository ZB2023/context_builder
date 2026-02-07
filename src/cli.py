import argparse
import sys

from rich.console import Console

from src.scanner import scan_directory
from src.session import save_session
from src.exporter import export
from src.redactor import redact_scan_result
from src.preview import show_preview

console = Console()


def parse_args():
    parser = argparse.ArgumentParser(
        prog="context-builder",
        description="Инструмент для сканирования и экспорта структуры проектов",
    )

    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Путь к директории для сканирования",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Название файла (без расширения)",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["txt", "md", "json"],
        default="txt",
        help="Формат экспорта (по умолчанию: txt)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Директория для сохранения отчёта",
    )

    parser.add_argument(
        "--no-tree",
        action="store_true",
        help="Не включать дерево структуры в отчёт",
    )

    parser.add_argument(
        "--redact",
        action="store_true",
        help="Включить цензуру конфиденциальных данных",
    )

    parser.add_argument(
        "--max-file-size",
        type=int,
        default=10,
        help="Максимальный размер файла в МБ (по умолчанию: 10)",
    )

    parser.add_argument(
        "--split",
        type=int,
        default=0,
        help="Разбить на части по N МБ (0 = без разбиения)",
    )

    parser.add_argument(
        "--silent",
        action="store_true",
        help="Тихий режим (без вывода в консоль)",
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Только предпросмотр (без создания файла)",
    )

    return parser.parse_args()


def run_cli():
    args = parse_args()

    if not args.silent:
        console.print("[bold cyan]Context Builder — CLI Mode[/bold cyan]\n")

    scan_result = scan_directory(args.path, args.max_file_size)

    if scan_result is None:
        console.print("[bold red]Ошибка сканирования[/bold red]")
        sys.exit(1)

    if args.redact:
        scan_result, findings = redact_scan_result(scan_result)
        if not args.silent and findings:
            console.print("[yellow]⚠ Цензура применена[/yellow]")
            for item in findings:
                console.print(f"  [dim]{item['file']}[/dim]")
                for f in item["findings"]:
                    console.print(f"    [red]• {f['pattern']}: {f['count']}[/red]")

    if args.preview:
        show_preview(scan_result)
        sys.exit(0)

    if args.output is None:
        from datetime import datetime
        args.output = f"scan_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    include_tree = not args.no_tree
    output_dir = args.output_dir

    if args.split > 0:
        from src.chunker import export_chunked
        files = export_chunked(
            scan_result, args.output, args.format, output_dir, include_tree, args.split
        )
        for f in files:
            if not args.silent:
                console.print(f"[bold green]✓ {f}[/bold green]")
    else:
        output_file = export(scan_result, args.output, args.format, output_dir, include_tree)
        save_session(scan_result, report_path=output_file)
        if not args.silent:
            console.print(f"[bold green]✓ Отчёт создан: {output_file}[/bold green]")

    sys.exit(0)