from pathlib import Path

BINARY_EXTENSIONS = {
    ".exe", ".dll", ".so", ".dylib",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".svg",
    ".mp3", ".wav", ".flac", ".aac", ".ogg",
    ".mp4", ".avi", ".mkv", ".mov", ".wmv",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",
    ".pdf",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".db", ".sqlite", ".sqlite3",
    ".pyc", ".pyo", ".class", ".o", ".obj",
    ".woff", ".woff2", ".ttf", ".eot",
}


def is_binary_extension(filepath):
    return Path(filepath).suffix.lower() in BINARY_EXTENSIONS


def is_within_size_limit(filepath, max_size_mb=10):
    try:
        size_mb = Path(filepath).stat().st_size / (1024 * 1024)
        return size_mb <= max_size_mb
    except OSError:
        return False