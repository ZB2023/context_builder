import json
import hashlib
from pathlib import Path
from datetime import datetime


SESSION_DIR = ".context_builder"


def save_session(scan_result, output_dir=None, report_path=None):
    if output_dir is None:
        output_dir = scan_result["root"]

    session_path = Path(output_dir) / SESSION_DIR
    session_path.mkdir(exist_ok=True)

    session_data = {
        "created_at": datetime.now().isoformat(),
        "scan_data": scan_result,
    }

    if report_path is not None:
        report_hash = calculate_file_hash(report_path)
        if report_hash:
            session_data["report_hash"] = report_hash
            session_data["report_path"] = str(report_path)

    session_file = session_path / "session.json"
    session_file.write_text(
        json.dumps(session_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return session_file


def load_session(directory):
    session_file = Path(directory) / SESSION_DIR / "session.json"

    if not session_file.exists():
        return None

    try:
        raw = session_file.read_text(encoding="utf-8")
        return json.loads(raw)
    except (json.JSONDecodeError, OSError):
        return None


def calculate_file_hash(filepath):
    try:
        content = Path(filepath).read_bytes()
        return hashlib.sha256(content).hexdigest()
    except OSError:
        return None


def list_sessions_in_directory(directory):
    root = Path(directory).resolve()
    sessions = []

    session_file = root / SESSION_DIR / "session.json"
    if session_file.exists():
        sessions.append(root)

    try:
        for entry in root.iterdir():
            if entry.is_dir() and entry.name != SESSION_DIR:
                child_session = entry / SESSION_DIR / "session.json"
                if child_session.exists():
                    sessions.append(entry)
    except PermissionError:
        pass

    return sessions

def find_report_files(directory):
    root = Path(directory).resolve()
    report_extensions = {".txt", ".md", ".json"}
    report_files = []

    try:
        for entry in root.iterdir():
            if entry.is_file() and entry.suffix.lower() in report_extensions:
                if entry.parent.name != SESSION_DIR:
                    report_files.append(entry)
    except PermissionError:
        pass

    return sorted(report_files, key=lambda f: f.name.lower())