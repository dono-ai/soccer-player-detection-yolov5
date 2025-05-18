from PySide6 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
import os, torch, cv2
import numpy as np
from .functions import create_output_path


class ImageFrame(QtWidgets.QFrame):
    def __init__(self, width, height, model):
        super().__init__()
        self.height = height
        self.width = width
        self.image = None
        self.model = model
        self.setup_ui()
        
    def setup_ui(self):
        self.image = QtWidgets.QLabel()
        self.image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.process_btn = QtWidgets.QPushButton("Process Image")
        self.process_btn.clicked.connect(self.process_image)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.image)
        layout.addWidget(self.process_btn)
                
        self.setLayout(layout)
        self.setFixedSize(self.width, self.height)

    
    def load_file(self, path):
        self.path = path
        pixmap = QtGui.QPixmap(path)
        scaled = pixmap.scaled(
            self.width, self.height,
            QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        offset_x = (scaled.width() - self.width) // 2
        offset_y = (scaled.height() - self.height) // 2
        cropped = scaled.copy(offset_x, offset_y, self.width, self.height)

        self.image.setPixmap(cropped)

    def process_image(self):
        output_path = create_output_path("./output", self.path)
        try:
            img = cv2.imread(self.path)
            height, width = img.shape[:2]
            with torch.no_grad():
                results = self.model(self.path, size = width)
                results.render()
                annotated = results.ims[0] if hasattr(results, "ims") else results.imgs[0]
                annotated_bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
                if isinstance(annotated, np.ndarray):
                    success = cv2.imwrite(output_path, annotated_bgr)
                del results
                torch.cuda.empty_cache()
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Processing failed:\n{str(e)}")
        
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save image to: {output_path}")
        else: 
            QtWidgets.QMessageBox.information(
                    self,
                    "File Processed",
                    f"Processed file saved to:\n{output_path}"
                )
