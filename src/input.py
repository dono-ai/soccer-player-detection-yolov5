from PySide6 import QtWidgets, QtCore
from .functions import validate_file
from PySide6.QtCore import Signal

class Input(QtWidgets.QFrame):
    file_selected = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        container = QtWidgets.QGroupBox("Input Section")
        container_layout = QtWidgets.QHBoxLayout()
        container.setLayout(container_layout)

        # === LEFT SECTION ===
        left_layout = QtWidgets.QVBoxLayout()

        # Title line
        path_layout = QtWidgets.QHBoxLayout()
        path_label = QtWidgets.QLabel("Path:")
        path_label.setFixedWidth(100)
        self.path_value = QtWidgets.QLabel("Please select file.")
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_value)

        # File line
        file_layout = QtWidgets.QHBoxLayout()
        file_label = QtWidgets.QLabel("File Name:")
        file_label.setFixedWidth(100)
        self.file_value = QtWidgets.QLabel("No file selected.")
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_value)

        left_layout.addLayout(path_layout)
        left_layout.addLayout(file_layout)

        # === RIGHT SECTION ===
        self.browse_button = QtWidgets.QPushButton("Browse File")
        self.browse_button.clicked.connect(self.select_file)
        self.browse_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.browse_button)
        
        # Assemble layouts
        container_layout.addLayout(left_layout, 3)
        container_layout.addLayout(right_layout, 1)

        # Add container to main layout
        main_layout.addWidget(container)
        
    def select_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File")
        result = validate_file(file_path, 150)
        if result["is_valid"]:
            self.path_value.setText(result["display_path"])
            self.file_value.setText(result["file_name"])
            self.file_selected.emit(result["original_path"])
        else: 
            QtWidgets.QMessageBox.warning(self, "Invalid File", result["message"])

