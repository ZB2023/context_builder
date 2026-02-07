import json
from pathlib import Path

from rich.console import Console

console = Console()

CONFIG_DIR = Path.home() / ".context_builder_profiles"


def save_profile(name, settings):
    CONFIG_DIR.mkdir(exist_ok=True)

    profile_path = CONFIG_DIR / f"{name}.json"
    profile_path.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return profile_path


def load_profile(name):
    profile_path = CONFIG_DIR / f"{name}.json"

    if not profile_path.exists():
        return None

    try:
        raw = profile_path.read_text(encoding="utf-8")
        return json.loads(raw)
    except (json.JSONDecodeError, OSError):
        return None


def list_profiles():
    if not CONFIG_DIR.exists():
        return []

    return [
        p.stem
        for p in sorted(CONFIG_DIR.iterdir())
        if p.suffix == ".json"
    ]


def delete_profile(name):
    profile_path = CONFIG_DIR / f"{name}.json"

    if profile_path.exists():
        profile_path.unlink()
        return True

    return False