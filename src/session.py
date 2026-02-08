import json
import hashlib
from pathlib import Path
from datetime import datetime

SESSION_DIR_NAME = ".context_builder"
DEFAULT_SESSIONS_ROOT = Path.home() / ".context_builder_sessions"

_sessions_root = None


def get_sessions_root():
    global _sessions_root
    if _sessions_root is not None:
        return _sessions_root

    config_file = Path.home() / ".context_builder_config.json"

    if config_file.exists():
        try:
            raw = config_file.read_text(encoding="utf-8")
            config = json.loads(raw)
            stored_path = config.get("sessions_root")
            if stored_path:
                path = Path(stored_path)
                if path.exists() and path.is_dir():
                    _sessions_root = path
                    return _sessions_root
        except (json.JSONDecodeError, OSError):
            pass

    return None


def set_sessions_root(directory):
    global _sessions_root
    path = Path(directory).resolve()
    path.mkdir(parents=True, exist_ok=True)

    _sessions_root = path

    config_file = Path.home() / ".context_builder_config.json"
    config = {}
    if config_file.exists():
        try:
            raw = config_file.read_text(encoding="utf-8")
            config = json.loads(raw)
        except (json.JSONDecodeError, OSError):
            config = {}

    config["sessions_root"] = str(path)

    config_file.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return path


def _get_session_dir_for_scan(scan_root):
    sessions_root = get_sessions_root()
    if sessions_root is None:
        sessions_root = DEFAULT_SESSIONS_ROOT
        sessions_root.mkdir(parents=True, exist_ok=True)

    scan_path = Path(scan_root).resolve()
    safe_name = scan_path.name or "root"

    path_hash = hashlib.md5(str(scan_path).encode()).hexdigest()[:8]
    session_name = f"{safe_name}_{path_hash}"

    session_dir = sessions_root / session_name
    session_dir.mkdir(parents=True, exist_ok=True)

    return session_dir


def save_session(scan_result, output_dir=None, report_path=None):
    session_dir = _get_session_dir_for_scan(scan_result["root"])

    session_data = {
        "created_at": datetime.now().isoformat(),
        "scan_root": scan_result["root"],
        "scan_data": scan_result,
    }

    if report_path is not None:
        report_hash = calculate_file_hash(report_path)
        if report_hash:
            session_data["report_hash"] = report_hash
        session_data["report_path"] = str(report_path)

    if output_dir is not None:
        session_data["output_dir"] = str(output_dir)

    session_file = session_dir / "session.json"
    session_file.write_text(
        json.dumps(session_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return session_file


def load_session(session_identifier):
    path = Path(session_identifier)

    session_file = path / "session.json"
    if session_file.exists():
        try:
            raw = session_file.read_text(encoding="utf-8")
            return json.loads(raw)
        except (json.JSONDecodeError, OSError):
            return None

    legacy_session_file = path / SESSION_DIR_NAME / "session.json"
    if legacy_session_file.exists():
        try:
            raw = legacy_session_file.read_text(encoding="utf-8")
            return json.loads(raw)
        except (json.JSONDecodeError, OSError):
            return None

    return None


def calculate_file_hash(filepath):
    try:
        content = Path(filepath).read_bytes()
        return hashlib.sha256(content).hexdigest()
    except OSError:
        return None


def list_all_sessions():
    sessions_root = get_sessions_root()
    if sessions_root is None:
        sessions_root = DEFAULT_SESSIONS_ROOT

    if not sessions_root.exists():
        return []

    sessions = []
    try:
        for entry in sorted(sessions_root.iterdir()):
            if entry.is_dir():
                session_file = entry / "session.json"
                if session_file.exists():
                    try:
                        raw = session_file.read_text(encoding="utf-8")
                        data = json.loads(raw)
                        sessions.append({
                            "path": entry,
                            "scan_root": data.get("scan_root", "Неизвестно"),
                            "created_at": data.get("created_at", "Неизвестно"),
                            "report_path": data.get("report_path"),
                            "name": entry.name,
                        })
                    except (json.JSONDecodeError, OSError):
                        sessions.append({
                            "path": entry,
                            "scan_root": "Ошибка чтения",
                            "created_at": "Неизвестно",
                            "report_path": None,
                            "name": entry.name,
                        })
    except PermissionError:
        pass

    return sessions


def list_sessions_in_directory(directory):
    root = Path(directory).resolve()
    sessions = []

    all_sessions = list_all_sessions()
    for s in all_sessions:
        scan_root = s.get("scan_root", "")
        if scan_root:
            try:
                scan_path = Path(scan_root).resolve()
                if scan_path == root or root in scan_path.parents or scan_path in root.parents:
                    sessions.append(s["path"])
            except (ValueError, OSError):
                pass

    legacy_session = root / SESSION_DIR_NAME / "session.json"
    if legacy_session.exists() and root not in sessions:
        sessions.append(root)

    try:
        for entry in root.iterdir():
            if entry.is_dir() and entry.name != SESSION_DIR_NAME:
                child_session = entry / SESSION_DIR_NAME / "session.json"
                if child_session.exists() and entry not in sessions:
                    sessions.append(entry)
    except PermissionError:
        pass

    return sessions


def delete_session(session_path):
    import shutil
    path = Path(session_path)
    if path.exists() and path.is_dir():
        try:
            shutil.rmtree(path)
            return True
        except OSError:
            return False
    return False


def find_report_files(directory):
    root = Path(directory).resolve()
    report_extensions = {".txt", ".md", ".json", ".pdf"}
    report_files = []

    try:
        for entry in root.iterdir():
            if entry.is_file() and entry.suffix.lower() in report_extensions:
                if entry.parent.name != SESSION_DIR_NAME:
                    report_files.append(entry)
    except PermissionError:
        pass

    return sorted(report_files, key=lambda f: f.name.lower())