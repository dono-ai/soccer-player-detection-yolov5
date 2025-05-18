from PySide6 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
import os, torch, cv2
from .image_frame import ImageFrame
from .video_player import VideoPlayer
from pathlib import Path
class Output(QtWidgets.QFrame):
    def __init__(self, MainWindow):
        super().__init__()
        self.current_file = None

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt')
        self.model.conf = 0.1
        self.model.iou = 0.3
        self.model.agnostic = True  
 
        self.video_player = VideoPlayer(1000, 500, self.model)
        self.image_frame = ImageFrame(1000, 500, self.model)
        
        self.setup_ui()
        
    def setup_ui(self): 
        self.stack_layout = QtWidgets.QStackedLayout()
        self.stack_layout.addWidget(self.video_player)
        self.stack_layout.addWidget(self.image_frame)
        
        container = QtWidgets.QGroupBox("Output Section")
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.addLayout(self.stack_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(container)

    def check_path(self, file_path: str):
        self.current_file = file_path
        ext = Path(self.current_file).suffix.lower()
        is_image = ext == ".jpg"
        self.video_player.clean_up()
        if is_image:
            self.stack_layout.setCurrentWidget(self.image_frame)
            self.image_frame.load_file(file_path)
        else:
            self.stack_layout.setCurrentWidget(self.video_player)
            self.video_player.load_file(file_path)
        