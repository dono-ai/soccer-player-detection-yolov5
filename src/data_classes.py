from typing import TypedDict

class ValidationPathResult(TypedDict):
    is_valid: bool
    display_path: str
    original_path: str
    file_name: str
    message: str
