from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QTreeWidget,
    QTreeWidgetItem,
)
from PySide6.QtCore import Qt


class DirectoryPicker(QWidget):
    def __init__(self, placeholder="Выберите директорию..."):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(placeholder)

        self.browse_button = QPushButton("Обзор")
        self.browse_button.setFixedWidth(100)
        self.browse_button.clicked.connect(self._browse)

        layout.addWidget(self.path_input)
        layout.addWidget(self.browse_button)

    def _browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Выберите директорию")
        if directory:
            self.path_input.setText(directory)

    def get_path(self):
        return self.path_input.text().strip()

    def set_path(self, path):
        self.path_input.setText(path)


class FileTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabels(["Имя", "Тип", "Размер"])
        self.setColumnWidth(0, 350)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 100)
        self.setAlternatingRowColors(True)

    def load_scan_result(self, scan_result):
        self.clear()
        nodes = {}

        root_item = QTreeWidgetItem(self, [scan_result["root"], "Корень", ""])
        root_item.setExpanded(True)
        nodes["."] = root_item

        for item in scan_result["structure"]:
            path = Path(item["path"])
            parent_key = str(path.parent) if str(path.parent) != "." else "."
            parent_node = nodes.get(parent_key, root_item)

            if item["type"] == "directory":
                icon = "📁"
                type_text = "Папка"
            else:
                icon = "📄"
                type_text = path.suffix or "Файл"

            node = QTreeWidgetItem(parent_node, [f"{icon} {path.name}", type_text, ""])

            if item["type"] == "directory":
                nodes[str(path)] = node
                node.setExpanded(True)

        for file_data in scan_result["files"]:
            path = Path(file_data["path"])
            size = len(file_data["content"].encode("utf-8"))

            for i in range(root_item.childCount()):
                found = self._find_node(root_item.child(i), path.name)
                if found:
                    found.setText(2, self._format_size(size))
                    break

    def _find_node(self, node, name):
        if name in node.text(0):
            return node
        for i in range(node.childCount()):
            result = self._find_node(node.child(i), name)
            if result:
                return result
        return None

    def _format_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        if size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        return f"{size_bytes / (1024 * 1024):.1f} MB"