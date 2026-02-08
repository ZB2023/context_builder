from pathlib import Path

from rich.console import Console

from src.session import load_session, calculate_file_hash

console = Console()


def convert_from_session(session_dir, filename, target_format, output_dir=None):
    session_data = load_session(session_dir)

    if session_data is None:
        console.print("[bold red]Сессия не найдена в указанной директории[/bold red]")
        return None

    scan_result = session_data["scan_data"]

    if output_dir is None:
        output_dir = scan_result["root"]

    from src.exporter import export
    output_file = export(scan_result, filename, target_format, output_dir)
    return output_file


def get_available_sessions(directory):
    root = Path(directory).resolve()
    session_file = root / ".context_builder" / "session.json"

    if session_file.exists():
        return root

    return None


def detect_modification(original_path, session_dir):
    session_data = load_session(session_dir)

    if session_data is None:
        return "no_session"

    stored_hash = session_data.get("report_hash")

    if stored_hash is None:
        return "no_hash"

    current_hash = calculate_file_hash(original_path)

    if current_hash is None:
        return "file_missing"

    if current_hash != stored_hash:
        return "modified"

    return "unchanged"


def parse_pdf_to_text(pdf_path):
    try:
        import fitz

        doc = fitz.open(str(pdf_path))
        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()
        return text
    except ImportError:
        console.print("[bold red]Библиотека PyMuPDF не установлена. Выполните: pip install pymupdf[/bold red]")
        return None
    except Exception as e:
        console.print(f"[bold red]Ошибка чтения PDF: {e}[/bold red]")
        return None


def convert_pdf_to_format(pdf_path, filename, target_format, output_dir=None):
    pdf_path = Path(pdf_path)

    if output_dir is None:
        output_dir = str(pdf_path.parent)

    text = parse_pdf_to_text(pdf_path)

    if text is None:
        return None

    output_path = Path(output_dir) / f"{filename}.{target_format}"

    if target_format == "txt":
        output_path.write_text(text, encoding="utf-8")

    elif target_format == "md":
        md_content = f"# Конвертировано из PDF\n\n"
        md_content += f"- **Источник:** `{pdf_path.name}`\n"
        md_content += f"- **Дата:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += "---\n\n"
        md_content += "```\n"
        md_content += text
        md_content += "\n```\n"
        output_path.write_text(md_content, encoding="utf-8")

    elif target_format == "json":
        import json

        json_data = {
            "metadata": {
                "source": str(pdf_path),
                "converted_at": __import__('datetime').datetime.now().isoformat(),
                "format": "pdf_to_json",
            },
            "content": text,
        }
        output_path.write_text(
            json.dumps(json_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    else:
        console.print(f"[bold red]Неподдерживаемый формат: {target_format}[/bold red]")
        return None

    return output_path