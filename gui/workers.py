from PySide6.QtCore import QThread, Signal


class ScanWorker(QThread):
    progress = Signal(str)
    finished_signal = Signal(dict)
    error = Signal(str)

    def __init__(self, path, max_file_size=10):
        super().__init__()
        self.path = path
        self.max_file_size = max_file_size

    def run(self):
        try:
            from src.scanner import scan_directory
            self.progress.emit("Сканирование начато...")
            result = scan_directory(self.path, self.max_file_size)

            if result is None:
                self.error.emit("Директория не найдена или недоступна")
                return

            self.progress.emit(f"Найдено файлов: {len(result['files'])}")
            self.finished_signal.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ExportWorker(QThread):
    finished_signal = Signal(str)
    error = Signal(str)

    def __init__(self, scan_result, filename, fmt, output_dir, include_tree, redact, patterns):
        super().__init__()
        self.scan_result = scan_result
        self.filename = filename
        self.fmt = fmt
        self.output_dir = output_dir
        self.include_tree = include_tree
        self.redact = redact
        self.patterns = patterns

    def run(self):
        try:
            from src.exporter import export
            from src.session import save_session
            from src.redactor import redact_scan_result

            data = self.scan_result

            if self.redact:
                data, _ = redact_scan_result(data, self.patterns)

            output_file = export(data, self.filename, self.fmt, self.output_dir, self.include_tree)
            save_session(data, report_path=output_file)
            self.finished_signal.emit(str(output_file))
        except Exception as e:
            self.error.emit(str(e))