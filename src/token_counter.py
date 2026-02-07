from rich.console import Console

console = Console()


def count_tokens(text):
    try:
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except ImportError:
        return estimate_tokens(text)
    except Exception:
        return estimate_tokens(text)


def estimate_tokens(text):
    return len(text) // 4


def format_token_count(token_count):
    if token_count < 1000:
        return f"{token_count}"
    if token_count < 1000000:
        return f"{token_count / 1000:.1f}K"
    return f"{token_count / 1000000:.1f}M"


def get_scan_tokens(scan_result):
    total_text = ""

    for file_data in scan_result["files"]:
        total_text += file_data["content"] + "\n"

    return count_tokens(total_text)


def show_token_info(scan_result):
    token_count = get_scan_tokens(scan_result)
    formatted = format_token_count(token_count)

    console.print(f"\n[bold cyan]🔢 Примерное количество токенов: {formatted}[/bold cyan]")

    if token_count > 128000:
        console.print("[bold red]⚠ Превышает контекст GPT-4 (128K токенов)[/bold red]")
        console.print("[dim]Рекомендация: исключите лишние папки или используйте разбиение[/dim]")
    elif token_count > 32000:
        console.print("[yellow]⚠ Большой объём — может не поместиться в некоторые модели[/yellow]")
    else:
        console.print("[green]✓ Объём подходит для большинства LLM[/green]")

    console.print("")