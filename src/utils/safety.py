import os
from pathlib import Path


def check_access(filepath):
    try:
        path = Path(filepath)
        return path.exists() and os.access(path, os.R_OK)
    except OSError:
        return False