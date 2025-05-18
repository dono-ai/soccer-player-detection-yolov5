# Soccer Player Detection in Match Videos

## 1. Brief:

The main objective of this project is to develop an intelligent desktop application that automatically detects soccer players in recorded match videos using deep learning techniques. Built on the YOLOv5 architecture, the system provides accurate, real-time detection (above 98% accuracy), marking players with bounding boxes. This solution benefits coaches, analysts, referees, and media professionals by enabling tactical analysis, performance review, and enhanced visual content generation. Designed with a modular and scalable approach, it ensures efficient data handling, user-friendly interaction, and robust prediction performance—supporting future expansion into comprehensive sports analytics systems.

## 2. Project Structure:

SoccerPlayerDetection/
├── .gitignore
├── app.py # GUI launcher
├── requirement.txt # Project dependencies
├── readme.md # Project overview and guide
│
├── notebooks/
│ ├── create_dataset.ipynb # Create custom dataset (labels & images)
│ └── test.ipynb # Test model predictions and functions
│
├── src/
│ ├── style.css # GUI styling
│ └── ... # GUI components (modularized)
│
├── models/ # Trained model weights and files
│ └── yolov5_weights.pt
│
├── test_data/
│ └── test/ # Test images and videos
│
└── images/ # Miscellaneous media or output visuals

## 3. Run Project:

Follow these steps to set up and run the project locally:

- **Create virtual environment:**

  - Windows: `python -m venv venv`
  - Mac/Linux: `python3 -m venv venv`

- **Activate virtual environment:**

  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`

- **Install required packages:**

  ```bash
  pip install -r requirements.txt

  ```

- run the GUI application:
  python app.py

- To test model inference:
  Run notebooks/test.ipynb.

## Libraries:

Deep Learning & CV: PyTorch, OpenCV, YOLOv5

Data Handling: NumPy, Pandas

GUI: PySide6 / PyQt

Visualization: Matplotlib, OpenCV

Others: OS, Glob, Pickle

## Requirements:

PyTorch version: 2.3.0+cu121
Cuda version: 12.8
NVIDIA-SMI: 570.133.07
