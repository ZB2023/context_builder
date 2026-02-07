from pathlib import Path

from rich.console import Console
from rich.tree import Tree

from src.utils.file_filter import is_binary_extension, is_within_size_limit
from src.utils.encoding import detect_file_encoding, read_file_safe
from src.utils.safety import check_access

console = Console()

SKIP_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".context_builder",
    ".idea",
    ".vs",
    ".vscode",
}


def scan_directory(path, max_file_size_mb=10):
    root = Path(path).resolve()

    if not root.exists():
        console.print(f"[bold red]Директория не найдена: {root}[/bold red]")
        return None

    if not root.is_dir():
        console.print(f"[bold red]Это не директория: {root}[/bold red]")
        return None

    result = {
        "root": str(root),
        "structure": [],
        "files": [],
        "skipped": [],
        "errors": [],
    }

    _scan_recursive(root, root, result, max_file_size_mb)
    return result


def _scan_recursive(current_path, root, result, max_file_size_mb):
    if not check_access(current_path):
        result["errors"].append(
            {"path": str(current_path.relative_to(root)), "reason": "Access Denied"}
        )
        return

    try:
        entries = sorted(current_path.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    except PermissionError:
        result["errors"].append(
            {"path": str(current_path.relative_to(root)), "reason": "Permission Error"}
        )
        return

    for entry in entries:
        relative = entry.relative_to(root)

        if entry.is_dir():
            if entry.name in SKIP_DIRECTORIES:
                result["skipped"].append(
                    {"path": str(relative), "reason": "Excluded directory"}
                )
                continue

            result["structure"].append(
                {"path": str(relative), "type": "directory"}
            )
            _scan_recursive(entry, root, result, max_file_size_mb)

        elif entry.is_file():
            result["structure"].append(
                {"path": str(relative), "type": "file"}
            )

            if is_binary_extension(entry):
                result["skipped"].append(
                    {"path": str(relative), "reason": "Binary file"}
                )
                continue

            if not is_within_size_limit(entry, max_file_size_mb):
                result["skipped"].append(
                    {"path": str(relative), "reason": f"File too large (>{max_file_size_mb}MB)"}
                )
                continue

            encoding = detect_file_encoding(entry)
            content = read_file_safe(entry, encoding)

            if content is not None:
                result["files"].append(
                    {
                        "path": str(relative),
                        "encoding": encoding,
                        "content": content,
                    }
                )
            else:
                result["errors"].append(
                    {"path": str(relative), "reason": "Failed to read file"}
                )


def get_subdirectories(path):
    root = Path(path).resolve()

    if not root.exists() or not root.is_dir():
        return []

    return [
        entry
        for entry in sorted(root.iterdir())
        if entry.is_dir() and entry.name not in SKIP_DIRECTORIES
    ]


def build_tree_view(scan_result):
    root_path = scan_result["root"]
    tree = Tree(f"[bold blue]{root_path}[/bold blue]")
    nodes = {}

    for item in scan_result["structure"]:
        path = Path(item["path"])
        parts = path.parts

        parent_key = str(path.parent) if len(parts) > 1 else None
        current_key = str(path)

        if item["type"] == "directory":
            label = f"[bold yellow]📁 {path.name}[/bold yellow]"
        else:
            label = f"[dim]📄 {path.name}[/dim]"

        if parent_key and parent_key in nodes:
            node = nodes[parent_key].add(label)
        else:
            node = tree.add(label)

        if item["type"] == "directory":
            nodes[current_key] = node

    return tree