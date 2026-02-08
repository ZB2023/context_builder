from pathlib import Path
from datetime import datetime


def export_txt(scan_result, filename, output_dir=None, include_tree=True):
    if output_dir is None:
        output_dir = scan_result["root"]

    output_path = Path(output_dir) / f"{filename}.txt"
    lines = []

    lines.append("=" * 70)
    lines.append("  ОТЧЁТ О СТРУКТУРЕ ПРОЕКТА")
    lines.append(f"  Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  Корневая директория: {scan_result['root']}")
    lines.append("=" * 70)
    lines.append("")

    if include_tree:
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
    lines.append("  Конец отчёта")
    lines.append("=" * 70)

    content = "\n".join(lines)
    output_path.write_text(content, encoding="utf-8")

    return output_path


def export_md(scan_result, filename, output_dir=None, include_tree=True):
    if output_dir is None:
        output_dir = scan_result["root"]

    output_path = Path(output_dir) / f"{filename}.md"
    lines = []

    lines.append("# Отчёт о структуре проекта")
    lines.append("")
    lines.append(f"- **Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **Корневая директория:** `{scan_result['root']}`")
    lines.append("")

    if include_tree:
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


def export_json(scan_result, filename, output_dir=None, include_tree=True):
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
            "include_tree": include_tree,
        },
        "files": scan_result["files"],
        "skipped": scan_result["skipped"],
        "errors": scan_result["errors"],
    }

    if include_tree:
        export_data["structure"] = scan_result["structure"]

    output_path.write_text(
        json.dumps(export_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return output_path


def export_pdf(scan_result, filename, output_dir=None, include_tree=True):
    from fpdf import FPDF

    if output_dir is None:
        output_dir = scan_result["root"]

    output_path = Path(output_dir) / f"{filename}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    font_dir = Path(__file__).parent / "fonts"
    regular_font = font_dir / "DejaVuSans.ttf"
    bold_font = font_dir / "DejaVuSans-Bold.ttf"
    mono_font = font_dir / "DejaVuSansMono.ttf"

    if regular_font.exists() and bold_font.exists() and mono_font.exists():
        pdf.add_font("DejaVu", "", str(regular_font), uni=True)
        pdf.add_font("DejaVu", "B", str(bold_font), uni=True)
        pdf.add_font("DejaVuMono", "", str(mono_font), uni=True)
        font_regular = "DejaVu"
        font_mono = "DejaVuMono"
    else:
        pdf.add_font("DejaVu", "", "", uni=True)
        font_regular = "Helvetica"
        font_mono = "Courier"

    pdf.add_page()

    pdf.set_font(font_regular, "B", 18)
    pdf.cell(0, 12, "Отчёт о структуре проекта", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    pdf.set_font(font_regular, "", 10)
    pdf.cell(0, 7, f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Директория: {scan_result['root']}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    if include_tree and scan_result["structure"]:
        pdf.set_font(font_regular, "B", 14)
        pdf.cell(0, 10, "Дерево структуры", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_font(font_mono, "", 8)

        for item in scan_result["structure"]:
            depth = item["path"].count("\\") + item["path"].count("/")
            indent = "    " * depth
            name = Path(item["path"]).name

            if item["type"] == "directory":
                line = f"{indent}[D] {name}/"
            else:
                line = f"{indent}[F] {name}"

            pdf.cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")

        pdf.ln(6)

    if scan_result["files"]:
        pdf.set_font(font_regular, "B", 14)
        pdf.cell(0, 10, "Содержимое файлов", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        for file_data in scan_result["files"]:
            pdf.set_font(font_regular, "B", 11)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 8, f"  {file_data['path']}", new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.ln(2)

            pdf.set_font(font_mono, "", 7)

            content_lines = file_data["content"].split("\n")
            for line in content_lines:
                safe_line = line.replace("\r", "").replace("\t", "    ")
                if len(safe_line) > 120:
                    safe_line = safe_line[:120] + "..."
                pdf.cell(0, 4, safe_line, new_x="LMARGIN", new_y="NEXT")

            pdf.ln(4)

    if scan_result["skipped"]:
        pdf.set_font(font_regular, "B", 14)
        pdf.cell(0, 10, "Пропущенные файлы", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_font(font_regular, "", 9)
        for item in scan_result["skipped"]:
            pdf.cell(0, 6, f"  ! {item['path']} - {item['reason']}", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(4)

    if scan_result["errors"]:
        pdf.set_font(font_regular, "B", 14)
        pdf.cell(0, 10, "Ошибки", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_font(font_regular, "", 9)
        for item in scan_result["errors"]:
            pdf.cell(0, 6, f"  X {item['path']} - {item['reason']}", new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(output_path))

    return output_path


def export(scan_result, filename, fmt, output_dir=None, include_tree=True):
    exporters = {
        "txt": export_txt,
        "md": export_md,
        "json": export_json,
        "pdf": export_pdf,
    }

    exporter = exporters.get(fmt)

    if exporter is None:
        raise ValueError(f"Неподдерживаемый формат: {fmt}")

    return exporter(scan_result, filename, output_dir, include_tree)