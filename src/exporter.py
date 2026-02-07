from pathlib import Path
from datetime import datetime


def export_txt(scan_result, filename, output_dir=None):
    if output_dir is None:
        output_dir = scan_result["root"]

    output_path = Path(output_dir) / f"{filename}.txt"
    lines = []

    lines.append("=" * 70)
    lines.append(f"  ОТЧЁТ О СТРУКТУРЕ ПРОЕКТА")
    lines.append(f"  Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  Корневая директория: {scan_result['root']}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("-" * 70)
    lines.append("  ДЕРЕВО СТРУКТУРЫ")
    lines.append("-" * 70)
    lines.append("")

    for item in scan_result["structure"]:
        depth = item["path"].count("\\") + item["path"].count("/")
        indent = "    " * depth

        if item["type"] == "directory":
            lines.append(f"{indent}📁 {Path(item['path']).name}/")
        else:
            lines.append(f"{indent}📄 {Path(item['path']).name}")

    lines.append("")

    lines.append("-" * 70)
    lines.append("  СОДЕРЖИМОЕ ФАЙЛОВ")
    lines.append("-" * 70)

    for file_data in scan_result["files"]:
        lines.append("")
        lines.append("=" * 70)
        lines.append(f"  Файл: {file_data['path']}")
        lines.append(f"  Кодировка: {file_data['encoding']}")
        lines.append("=" * 70)
        lines.append("")
        lines.append(file_data["content"])
        lines.append("")

    if scan_result["skipped"]:
        lines.append("-" * 70)
        lines.append("  ПРОПУЩЕННЫЕ ФАЙЛЫ")
        lines.append("-" * 70)
        lines.append("")
        for item in scan_result["skipped"]:
            lines.append(f"  ⚠ {item['path']} — {item['reason']}")
        lines.append("")

    if scan_result["errors"]:
        lines.append("-" * 70)
        lines.append("  ОШИБКИ")
        lines.append("-" * 70)
        lines.append("")
        for item in scan_result["errors"]:
            lines.append(f"  ✗ {item['path']} — {item['reason']}")
        lines.append("")

    lines.append("=" * 70)
    lines.append(f"  Конец отчёта")
    lines.append("=" * 70)

    content = "\n".join(lines)
    output_path.write_text(content, encoding="utf-8")

    return output_path


def export_md(scan_result, filename, output_dir=None):
    if output_dir is None:
        output_dir = scan_result["root"]

    output_path = Path(output_dir) / f"{filename}.md"
    lines = []

    lines.append(f"# Отчёт о структуре проекта")
    lines.append("")
    lines.append(f"- **Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **Корневая директория:** `{scan_result['root']}`")
    lines.append("")

    lines.append("## Дерево структуры")
    lines.append("")
    lines.append("```")

    for item in scan_result["structure"]:
        depth = item["path"].count("\\") + item["path"].count("/")
        indent = "  " * depth

        if item["type"] == "directory":
            lines.append(f"{indent}📁 {Path(item['path']).name}/")
        else:
            lines.append(f"{indent}📄 {Path(item['path']).name}")

    lines.append("```")
    lines.append("")

    lines.append("## Содержимое файлов")
    lines.append("")

    for file_data in scan_result["files"]:
        extension = Path(file_data["path"]).suffix.lstrip(".")
        lines.append(f"### `{file_data['path']}`")
        lines.append("")
        lines.append(f"```{extension}")
        lines.append(file_data["content"])
        lines.append("```")
        lines.append("")

    if scan_result["skipped"]:
        lines.append("## Пропущенные файлы")
        lines.append("")
        for item in scan_result["skipped"]:
            lines.append(f"- ⚠ `{item['path']}` — {item['reason']}")
        lines.append("")

    if scan_result["errors"]:
        lines.append("## Ошибки")
        lines.append("")
        for item in scan_result["errors"]:
            lines.append(f"- ✗ `{item['path']}` — {item['reason']}")
        lines.append("")

    content = "\n".join(lines)
    output_path.write_text(content, encoding="utf-8")

    return output_path


def export_json(scan_result, filename, output_dir=None):
    import json

    if output_dir is None:
        output_dir = scan_result["root"]

    output_path = Path(output_dir) / f"{filename}.json"

    export_data = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "root": scan_result["root"],
            "total_files": len(scan_result["files"]),
            "total_skipped": len(scan_result["skipped"]),
            "total_errors": len(scan_result["errors"]),
        },
        "structure": scan_result["structure"],
        "files": scan_result["files"],
        "skipped": scan_result["skipped"],
        "errors": scan_result["errors"],
    }

    output_path.write_text(
        json.dumps(export_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return output_path


def export(scan_result, filename, fmt, output_dir=None):
    exporters = {
        "txt": export_txt,
        "md": export_md,
        "json": export_json,
    }

    exporter = exporters.get(fmt)

    if exporter is None:
        raise ValueError(f"Неподдерживаемый формат: {fmt}")

    return exporter(scan_result, filename, output_dir)