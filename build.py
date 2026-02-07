import subprocess
import shutil
import sys
from pathlib import Path


PYTHON = sys.executable


def clean():
    for folder in ["build", "dist"]:
        path = Path(folder)
        if path.exists():
            shutil.rmtree(path)
            print(f"Удалено: {folder}/")

    for spec in Path(".").glob("*.spec"):
        spec.unlink()
        print(f"Удалено: {spec}")


def build_gui():
    print("\n=== Сборка GUI версии ===\n")
    subprocess.run([
        PYTHON, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "ContextBuilder-GUI",
        "--icon", "icon.ico",
        "--add-data", "icon.ico;.",
        "--hidden-import", "src",
        "--hidden-import", "src.menu",
        "--hidden-import", "src.scanner",
        "--hidden-import", "src.session",
        "--hidden-import", "src.exporter",
        "--hidden-import", "src.converter",
        "--hidden-import", "src.redactor",
        "--hidden-import", "src.preview",
        "--hidden-import", "src.config",
        "--hidden-import", "src.clipboard",
        "--hidden-import", "src.chunker",
        "--hidden-import", "src.token_counter",
        "--hidden-import", "src.cli",
        "--hidden-import", "src.utils",
        "--hidden-import", "src.utils.file_filter",
        "--hidden-import", "src.utils.filename",
        "--hidden-import", "src.utils.encoding",
        "--hidden-import", "src.utils.safety",
        "--hidden-import", "gui",
        "--hidden-import", "gui.app",
        "--hidden-import", "gui.main_window",
        "--hidden-import", "gui.scan_tab",
        "--hidden-import", "gui.convert_tab",
        "--hidden-import", "gui.delete_tab",
        "--hidden-import", "gui.files_tab",
        "--hidden-import", "gui.settings_tab",
        "--hidden-import", "gui.widgets",
        "--hidden-import", "gui.workers",
        "--hidden-import", "gui.styles",
        "--hidden-import", "chardet",
        "--hidden-import", "pyperclip",
        "--collect-all", "tiktoken",
        "--collect-all", "tiktoken_ext",
        "main_gui.py",
    ], check=True)
    print("\n✅ GUI версия собрана!")


def build_cli():
    print("\n=== Сборка CLI версии ===\n")
    subprocess.run([
        PYTHON, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--console",
        "--name", "ContextBuilder-CLI",
        "--icon", "icon.ico",
        "--hidden-import", "src",
        "--hidden-import", "src.menu",
        "--hidden-import", "src.scanner",
        "--hidden-import", "src.session",
        "--hidden-import", "src.exporter",
        "--hidden-import", "src.converter",
        "--hidden-import", "src.redactor",
        "--hidden-import", "src.preview",
        "--hidden-import", "src.config",
        "--hidden-import", "src.clipboard",
        "--hidden-import", "src.chunker",
        "--hidden-import", "src.token_counter",
        "--hidden-import", "src.cli",
        "--hidden-import", "src.utils",
        "--hidden-import", "src.utils.file_filter",
        "--hidden-import", "src.utils.filename",
        "--hidden-import", "src.utils.encoding",
        "--hidden-import", "src.utils.safety",
        "--hidden-import", "chardet",
        "--hidden-import", "pyperclip",
        "--collect-all", "tiktoken",
        "--collect-all", "tiktoken_ext",
        "main.py",
    ], check=True)
    print("\n✅ CLI версия собрана!")


if __name__ == "__main__":
    clean()
    build_cli()
    build_gui()

    print("\n" + "=" * 50)
    print("Готово! Файлы в папке dist/")
    print("  dist/ContextBuilder-CLI.exe  — консольная версия")
    print("  dist/ContextBuilder-GUI.exe  — графическая версия")
    print("=" * 50)