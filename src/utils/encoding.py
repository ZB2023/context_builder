from pathlib import Path


def detect_file_encoding(filepath, sample_size=8192):
    try:
        raw = Path(filepath).read_bytes()[:sample_size]

        try:
            raw.decode("utf-8")
            return "utf-8"
        except UnicodeDecodeError:
            pass

        try:
            raw.decode("utf-8-sig")
            return "utf-8-sig"
        except UnicodeDecodeError:
            pass

        try:
            import chardet
            detection = chardet.detect(raw)
            encoding = detection.get("encoding")
            confidence = detection.get("confidence", 0)

            if encoding and confidence > 0.7:
                return encoding
        except ImportError:
            pass

        return "utf-8"

    except OSError:
        return "utf-8"


def read_file_safe(filepath, encoding="utf-8"):
    path = Path(filepath)

    encodings_to_try = [encoding, "utf-8", "utf-8-sig", "cp1251", "latin-1"]
    seen = set()

    for enc in encodings_to_try:
        if enc in seen:
            continue
        seen.add(enc)

        try:
            content = path.read_text(encoding=enc)
            content.encode("utf-8")
            return content
        except (UnicodeDecodeError, UnicodeEncodeError, OSError):
            continue

    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None