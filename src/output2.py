from PySide6 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
import os, torch, cv2
import numpy as np
from PIL import Image
class Output(QtWidgets.QFrame):
    def __init__(self, MainWindow):
        super().__init__()
        self.media_player = None
        self.video_widget = None
        self.image_label = None
        self.slider = None
        self.setup_ui()
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt')
        self.model.conf = 0.1
        self.model.iou = 0.3
        self.model.agnostic = True  
        
        # self.media_box = 

    def setup_ui(self):
        # === Image Widget ===
        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedSize(1000, 500)
        self.image_label.setStyleSheet("background-color: black;")
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # === Video Container ===
        self.video_container = QtWidgets.QFrame()
        self.video_container.setFixedSize(1000, 500)
        self.video_container.setStyleSheet("background-color: black;")

        self.video_widget = QtMultimediaWidgets.QVideoWidget(self.video_container)
        self.video_widget.setGeometry(0, 0, 1000, 500)

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

        # === Stacked display: video or image ===
        self.stack = QtWidgets.QStackedLayout()
        self.stack.addWidget(self.video_container)
        self.stack.addWidget(self.image_label)
        
        self.process_btn = QtWidgets.QPushButton("Process File")
        self.process_btn.clicked.connect(self.process_file)


        # === Container layout ===
        container = QtWidgets.QGroupBox("Output Section")
        container_layout = QtWidgets.QVBoxLayout()
        container_layout.addLayout(self.stack)
        container_layout.addWidget(self.process_btn)
        container_layout.addWidget(self.controls_widget)
        container.setLayout(container_layout)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def load_file(self, file_path: str):
        self.current_file = file_path
        ext = os.path.splitext(file_path)[1].lower()
        is_image = ext == ".jpg"

        if is_image:
            if self.media_player:
                self.media_player.stop()
                self.media_player.deleteLater()
                self.media_player = None

            self.slider.setRange(0, 0)
            self.image_label.clear()

            pixmap = QtGui.QPixmap(file_path)
            target_size = self.image_label.size()
            scaled = pixmap.scaled(
                target_size,
                QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
            offset_x = (scaled.width() - target_size.width()) // 2
            offset_y = (scaled.height() - target_size.height()) // 2
            cropped = scaled.copy(offset_x, offset_y, target_size.width(), target_size.height())

            self.image_label.setPixmap(cropped)
            self.stack.setCurrentWidget(self.image_label)
            self.controls_widget.setVisible(False)  # <-- hide controls

        else:
            self.stack.setCurrentWidget(self.video_container)
            self.controls_widget.setVisible(True)  # <-- show controls

            if self.media_player:
                self.media_player.stop()
                self.media_player.deleteLater()

            self.media_player = QtMultimedia.QMediaPlayer(self)
            self.media_player.setVideoOutput(self.video_widget)
            self.media_player.setSource(QtCore.QUrl.fromLocalFile(file_path))

            self.media_player.positionChanged.connect(self.update_slider_position)
            self.media_player.durationChanged.connect(self.update_slider_range)

            self.media_player.play()


    def update_slider_position(self, position: int):
        self.slider.setValue(position)

    def update_slider_range(self, duration: int):
        self.slider.setRange(0, duration)

    def set_position(self, position: int):
        if self.media_player:
            self.media_player.setPosition(position)

    def process_file(self):
        if not hasattr(self, "current_file") or not os.path.exists(self.current_file):
            QtWidgets.QMessageBox.warning(self, "Error", "No valid file loaded.")
            return

        input_path = self.current_file
        file_name = os.path.basename(input_path)
        name, ext = os.path.splitext(file_name)
        ext = ext.lower()

        os.makedirs("output", exist_ok=True)

        try:
            if ext == ".jpg":
                # === IMAGE PROCESSING ===
                results = self.model(input_path, size=640)
                results.render()  # update results.imgs with annotations

                # Convert rendered image to PIL format and save
                annotated = results.ims[0] if hasattr(results, "ims") else results.imgs[0]
                if isinstance(annotated, np.ndarray):
                    img = Image.fromarray(annotated)
                    output_path = os.path.join("output", f"processed_{file_name}")
                    img.save(output_path)

            elif ext == ".mp4":
                # === VIDEO PROCESSING ===
                cap = cv2.VideoCapture(input_path)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)

                output_path = os.path.join("output", f"processed_{name}.mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Run inference
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.model(frame_rgb, size=640)
                    results.render()
                    annotated = results.ims[0] if hasattr(results, "ims") else results.imgs[0]
                    if isinstance(annotated, np.ndarray):
                        out.write(annotated)
                    torch.cuda.empty_cache()


                    # Get annotated frame
                    annotated = results.ims[0] if hasattr(results, "ims") else results.imgs[0]
                    if isinstance(annotated, np.ndarray):
                        out.write(annotated)

                cap.release()
                out.release()

            else:
                QtWidgets.QMessageBox.warning(self, "Unsupported", "Only .jpg and .mp4 are supported.")
                return

            # ✅ Notify success
            QtWidgets.QMessageBox.information(
                self,
                "File Processed",
                f"Processed file saved to:\n{os.path.abspath('output')}"
            )

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Processing failed:\n{str(e)}")
