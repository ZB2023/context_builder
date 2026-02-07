from rich.console import Console
from rich.table import Table

from src.token_counter import get_scan_tokens, format_token_count

console = Console()


def show_preview(scan_result):
    total_files = len(scan_result["files"])
    total_dirs = sum(
        1 for item in scan_result["structure"] if item["type"] == "directory"
    )
    total_skipped = len(scan_result["skipped"])
    total_errors = len(scan_result["errors"])
    total_size = sum(len(f["content"].encode("utf-8")) for f in scan_result["files"])
    token_count = get_scan_tokens(scan_result)

    table = Table(title="Предпросмотр сканирования", border_style="bright_blue")
    table.add_column("Параметр", style="cyan")
    table.add_column("Значение", style="green")

    table.add_row("Корневая директория", scan_result["root"])
    table.add_row("Директорий", str(total_dirs))
    table.add_row("Файлов (читаемых)", str(total_files))
    table.add_row("Пропущено", str(total_skipped))
    table.add_row("Ошибок", str(total_errors))
    table.add_row("Общий размер", _format_size(total_size))
    table.add_row("Токенов (≈)", format_token_count(token_count))

    console.print(table)

    if token_count > 128000:
        console.print("[bold red]⚠ Превышает контекст GPT-4 (128K)[/bold red]")
    elif token_count > 32000:
        console.print("[yellow]⚠ Большой объём для некоторых моделей[/yellow]")

    if scan_result["skipped"]:
        console.print("\n[bold yellow]Пропущенные файлы:[/bold yellow]")
        for item in scan_result["skipped"]:
            console.print(f"  [dim]⚠ {item['path']} — {item['reason']}[/dim]")

    if scan_result["errors"]:
        console.print("\n[bold red]Ошибки:[/bold red]")
        for item in scan_result["errors"]:
            console.print(f"  [dim]✗ {item['path']} — {item['reason']}[/dim]")


def _format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"