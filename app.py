"""
GUI Launcher for NLP Intent Classification App

This script initializes and displays the main window of the application using PySide6.
It applies external CSS styling and launches the event loop.

Structure:
- Loads and applies `style.css` if available.
- Instantiates and shows `MainWindow`, which must be defined in `app_components/main_window.py`.

Dependencies:
- PySide6
"""


import sys
from PySide6.QtWidgets import QApplication
from src.main_window import MainWindow
import os
# === Initialize QApplication ===
app = QApplication(sys.argv)
# === Load CSS Style ===
css_file = os.path.join(os.path.dirname(__file__), "src/style.css")  # Get absolute path
if os.path.exists(css_file):  # Check if file exists
    print("CSS is loaded Successfully")
    with open(css_file, "r") as f:
        app.setStyleSheet(f.read())  # Apply CSS
# === Create and show main window ===
window = MainWindow(app)
window.show()
# === Run application event loop ===
app.exec()
