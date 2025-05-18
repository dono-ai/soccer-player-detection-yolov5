import os
import cv2
from .data_classes import ValidationPathResult
from pathlib import Path
from datetime import datetime

def validate_file(path: str, max_chars: int = 150) -> ValidationPathResult:
    result: ValidationPathResult = {
        "is_valid": False,
        "display_path": "",
        "original_path": "",
        "file_name": "",
        "message": ""
    }

    if not path:
        result["message"] = "No file selected."
        return result

    extension = os.path.splitext(path)[1].lower()
    result["file_name"] = os.path.basename(path)
    result["original_path"] = path
    result["display_path"] = path if len(path) <= max_chars else "..." + path[-max_chars:]

    if extension not in [".jpg", ".mp4"]:
        result["message"] = "Invalid file type. Only .jpg and .mp4 are allowed."
        return result

    if extension == ".mp4":
        try:
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                result["message"] = "Could not open video file."
                return result

            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frame_count / fps if fps else 0
            cap.release()

            if duration == 0:
                result["message"] = "Skipped video — duration is 0 seconds."
                return result
            if duration > 60:
                result["message"] = "Video exceeds 60 seconds."
                return result
        except Exception as e:
            result["message"] = f"Error reading video: {e}"
            return result

    result["is_valid"] = True
    return result


def create_output_path(output_root, file_path):
    name = Path(file_path).stem
    ext = Path(file_path).suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_name = f"{name}_{timestamp}{ext}"
    output_path = os.path.join(output_root, output_name)
    return output_path