import json
import hashlib
from pathlib import Path
from datetime import datetime


SESSION_DIR = ".context_builder"


def save_session(scan_result, output_dir=None):
    if output_dir is None:
        output_dir = scan_result["root"]

    session_path = Path(output_dir) / SESSION_DIR
    session_path.mkdir(exist_ok=True)

    session_data = {
        "created_at": datetime.now().isoformat(),
        "scan_data": scan_result,
    }

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