from pathlib import Path

from src.exporter import export


def split_scan_result(scan_result, max_size_mb):
    max_size_bytes = max_size_mb * 1024 * 1024
    chunks = []
    current_chunk = {
        "root": scan_result["root"],
        "structure": scan_result["structure"],
        "files": [],
        "skipped": scan_result["skipped"],
        "errors": scan_result["errors"],
    }
    current_size = 0

    for file_data in scan_result["files"]:
        file_size = len(file_data["content"].encode("utf-8"))

        if current_size + file_size > max_size_bytes and current_chunk["files"]:
            chunks.append(current_chunk)
            current_chunk = {
                "root": scan_result["root"],
                "structure": scan_result["structure"],
                "files": [],
                "skipped": [],
                "errors": [],
            }
            current_size = 0

        current_chunk["files"].append(file_data)
        current_size += file_size

    if current_chunk["files"]:
        chunks.append(current_chunk)

    return chunks


def export_chunked(scan_result, filename, fmt, output_dir=None, include_tree=True, max_size_mb=5):
    chunks = split_scan_result(scan_result, max_size_mb)

    if len(chunks) <= 1:
        output_file = export(scan_result, filename, fmt, output_dir, include_tree)
        return [output_file]

    output_files = []

    for i, chunk in enumerate(chunks, 1):
        chunk_name = f"{filename}_part{i}"
        output_file = export(chunk, chunk_name, fmt, output_dir, include_tree)
        output_files.append(output_file)

    if output_dir is None:
        output_dir = scan_result["root"]

    index_path = Path(output_dir) / f"{filename}_index.txt"
    lines = [
        f"Отчёт разбит на {len(chunks)} частей:",
        "",
    ]

    for i, f in enumerate(output_files, 1):
        file_count = len(chunks[i - 1]["files"])
        lines.append(f"  Часть {i}: {Path(f).name} ({file_count} файлов)")

    index_path.write_text("\n".join(lines), encoding="utf-8")
    output_files.append(index_path)

    return output_files