import json
import pickle
import random
from PySide6 import QtWidgets, QtCore
from .SideBar.sidebar import MenuBar
from .ConversationArea.conversation_area import ConversationArea
import uuid
import datetime
from functions import clean_text

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Starbuck Chatbot")
        self.resize(1000, 600)
        
        self.load_packages()
        
        container = QtWidgets.QWidget()
        self.setCentralWidget(container)
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)

        layout.setSpacing(10)

        # layout.addWidget(self.menu_bar, 1)
    
    def load_packages(self):
        pass


        