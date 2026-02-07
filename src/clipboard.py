from pathlib import Path

from rich.console import Console

console = Console()

MAX_CLIPBOARD_SIZE = 10 * 1024 * 1024


def copy_to_clipboard(filepath):
    try:
        import pyperclip
    except ImportError:
        console.print("[bold red]Библиотека pyperclip не установлена[/bold red]")
        return False

    path = Path(filepath)

    if not path.exists():
        console.print(f"[bold red]Файл не найден: {path}[/bold red]")
        return False

    file_size = path.stat().st_size

    if file_size > MAX_CLIPBOARD_SIZE:
        size_mb = file_size / (1024 * 1024)
        console.print(
            f"[bold red]Файл слишком большой для буфера ({size_mb:.1f} MB > 10 MB)[/bold red]"
        )
        return False

    try:
        content = path.read_text(encoding="utf-8")
        pyperclip.copy(content)
        return True
    except OSError as e:
        console.print(f"[bold red]Ошибка чтения файла: {e}[/bold red]")
        return False