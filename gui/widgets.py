from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QTreeWidget,
    QTreeWidgetItem,
    QHeaderView,
    QFrame,
)
from PySide6.QtCore import Qt


class DirectoryPicker(QWidget):
    def __init__(self, placeholder="Выберите директорию..."):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.container = QFrame()
        self.container.setObjectName("InputGroup")

        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.path_input = QLineEdit()
        self.path_input.setObjectName("GroupInput")
        self.path_input.setPlaceholderText(placeholder)

        self.browse_button = QPushButton("Обзор")
        self.browse_button.setObjectName("GroupBtn")
        self.browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.browse_button.setMinimumWidth(80)

        self.browse_button.clicked.connect(self._browse)
        container_layout.addWidget(self.path_input)
        container_layout.addWidget(self.browse_button)
        layout.addWidget(self.container)

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
        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        self.setAlternatingRowColors(True)
        self.setAnimated(True)
        self.setIndentation(20)

    def load_scan_result(self, scan_result):
        self.clear()
        nodes = {}
        root_path_str = scan_result.get("root", "")
        root_name = Path(root_path_str).name if root_path_str else "Project"

        root_item = QTreeWidgetItem(self, [root_name, "Корень", ""])
        root_item.setExpanded(True)
        nodes["."] = root_item

        if "structure" in scan_result:
            for item in scan_result["structure"]:
                path = Path(item["path"])

                try:
                    parent_path = path.parent
                    parent_key = str(parent_path) if str(parent_path) != "." else "."
                except ValueError:
                    parent_key = "."

                parent_node = nodes.get(parent_key, root_item)

                if item["type"] == "directory":
                    type_text = "📁  Папка"
                else:
                    type_text = path.suffix or "Файл"

                node = QTreeWidgetItem(parent_node, [path.name, type_text, ""])

                if item["type"] == "directory":
                    nodes[str(path)] = node
                    node.setExpanded(True)

        if "files" in scan_result:
            for file_data in scan_result["files"]:
                path = Path(file_data["path"])
                size = len(file_data.get("content", "").encode("utf-8"))

                found = self._find_node_by_name(root_item, path.name)
                if found:
                    found.setText(2, self._format_size(size))

    def _find_node_by_name(self, parent_item, name):
        if parent_item.text(0) == name:
            return parent_item
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if child.text(0) == name:
                return child
            found = self._find_node_by_name(child, name)
            if found:
                return found
        return None

    def _format_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        if size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        return f"{size_bytes / (1024 * 1024):.1f} MB"