from PySide6 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
import os, torch, cv2
from .functions import create_output_path

class VideoPlayer(QtWidgets.QFrame):
    def __init__(self, width, height, model):
        super().__init__()
        self.height = height
        self.width = width
        self.path = None
        self.media_player = None
        self.model = model
        
        self.setup_ui()
        
    def setup_ui(self):
        # === Video Widget ===
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.video_widget.setFixedSize(1000, 500)

        # === Controls ===
        self.play_btn = QtWidgets.QPushButton("Play")
        self.pause_btn = QtWidgets.QPushButton("Pause")
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)

        self.play_btn.clicked.connect(lambda: self.media_player.play() if self.media_player else None)
        self.pause_btn.clicked.connect(lambda: self.media_player.pause() if self.media_player else None)
        self.slider.sliderMoved.connect(self.set_position)

        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.addWidget(self.play_btn)
        controls_layout.addWidget(self.pause_btn)
        controls_layout.addWidget(self.slider)

        self.controls_widget = QtWidgets.QWidget()
        self.controls_widget.setLayout(controls_layout)

        # === Process Button ===
        self.process_btn = QtWidgets.QPushButton("Process Video")
        self.process_btn.clicked.connect(self.process_video)


        self.progress_bar = QtWidgets.QProgressBar()


        # === Layout Setup ===
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.controls_widget)
        layout.addWidget(self.process_btn)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
      
    def load_file(self, path):
        print(f"Loading video: {path}")
        self.path = path

        self.media_player = QtMultimedia.QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)
        self.video_widget.show()

        self.media_player.setSource(QtCore.QUrl.fromLocalFile(path))
        self.media_player.positionChanged.connect(self.update_slider_position)
        self.media_player.durationChanged.connect(self.update_slider_range)
        self.media_player.play()

        self.controls_widget.setVisible(True)

    def process_video(self):
        output_path = create_output_path("./output", self.path)

        try: 
            cap = cv2.VideoCapture(self.path)
            # Get original video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            current_frame = 0
            self.progress_bar.setValue(0)
            with torch.no_grad():
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        break
                    frame_resized = cv2.resize(frame, (1920, 600))
                    results = self.model(frame_resized, size=1920)
                    results.render()
                    annotated = results.ims[0] if hasattr(results, "ims") else results.imgs[0]

                    # Resize to match output video resolution
                    annotated_resized = cv2.resize(annotated, (width, height))
                    out.write(annotated_resized)
                    
                    current_frame += 1
                    progress = int((current_frame / total_frames) * 100)
                    self.progress_bar.setValue(progress)

                    QtWidgets.QApplication.processEvents() 

                    # Clean up to avoid CUDA OOM
                    del results
                    torch.cuda.empty_cache()

            # Release everything
            cap.release()
            out.release()
            cv2.destroyAllWindows() 
            self.progress_bar.setValue(100) 
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Processing failed:\n{str(e)}")
        
        success = os.path.isfile(output_path) and os.path.getsize(output_path) > 0

        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save image to: {output_path}")
        else: 
            QtWidgets.QMessageBox.information(
                    self,
                    "File Processed",
                    f"Processed file saved to:\n{output_path}"
                )

        
    def clean_up(self):
        if self.media_player:
            self.media_player.stop()
            self.media_player.deleteLater()
            self.media_player = None
            self.controls_widget.setVisible(False)
            
    def update_slider_position(self, position: int):
        self.slider.setValue(position)

    def update_slider_range(self, duration: int):
        self.slider.setRange(0, duration)

    def set_position(self, position: int):
        if self.media_player:
            self.media_player.setPosition(position)