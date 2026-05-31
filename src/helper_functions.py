import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict

from errors import DataLoadError

# Perform operations on values of matching keys between 2 dictionaries
def dict_binary_operation(
    operation: str, dict1: Dict[str, int], dict2: Dict[str, int]
) -> Dict[str, int]:
    match operation:
        case "add":
            result = Counter(dict1) + Counter(dict2)

        case "sub":
            _result = Counter(dict1) - Counter(dict2)
            result = {key: value for key, value in _result.items() if value > 0}

        case _:
            raise ValueError(f"Unsupported Operation: {operation}")

    return dict(result)


def dict_from_file(file_path: str | Path) -> Dict[Any, Any]:
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.exists():
        raise DataLoadError(f"File not found: {file_path}")
    if not file_path.is_file():
        raise DataLoadError(f"Not a valid file path: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise DataLoadError(f"Malformed JSON in {file_path}: {error.msg}") from error
    except OSError as error:
        raise DataLoadError(f"Cannot read file {file_path}: {error}") from error

    if not isinstance(data, dict):
        raise DataLoadError(
            f"Invalid data format in {file_path}: expected a dictionary, got {type(data).__name__}"
        )

    return data
