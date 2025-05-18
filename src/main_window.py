import json
import pickle
import random
from PySide6 import QtWidgets, QtCore
import uuid
import datetime
from .input import Input
from .output import Output

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Starbuck Chatbot")
        self.resize(1000, 600)
        
        container = QtWidgets.QWidget()
        self.setCentralWidget(container)
        
        self.input_section = Input(self)
        self.output_section = Output(self)
        self.input_section.file_selected.connect(self.output_section.check_path)
        
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        layout.addWidget(self.input_section, 1)
        layout.addWidget(self.output_section, 9)
    

        