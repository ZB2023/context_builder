from pathlib import Path

import chardet


def detect_file_encoding(filepath, sample_size=8192):
    try:
        raw = Path(filepath).read_bytes()[:sample_size]
        detection = chardet.detect(raw)
        encoding = detection.get("encoding", "utf-8")
        confidence = detection.get("confidence", 0)

        if encoding is None or confidence < 0.5:
            return "utf-8"

        return encoding
    except OSError:
        return "utf-8"


def read_file_safe(filepath, encoding="utf-8"):
    try:
        return Path(filepath).read_text(encoding=encoding, errors="replace")
    except OSError:
        return None