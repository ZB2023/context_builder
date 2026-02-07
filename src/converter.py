from pathlib import Path

from rich.console import Console

from src.session import load_session, calculate_file_hash
from src.exporter import export

console = Console()


def convert_from_session(session_dir, filename, target_format, output_dir=None):
    session_data = load_session(session_dir)

    if session_data is None:
        console.print("[bold red]Сессия не найдена в указанной директории[/bold red]")
        return None

    scan_result = session_data["scan_data"]

    if output_dir is None:
        output_dir = scan_result["root"]

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