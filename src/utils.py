import json
from collections import Counter
from typing import Any, Optional


def dict_binary_operation(
    operation: str, dict1: dict[str, int], dict2: dict[str, int]
) -> dict[str, int]:
    match operation:
        case "add":
            result = Counter(dict1) + Counter(dict2)

        case "sub":
            _result = Counter(dict1) - Counter(dict2)
            result = {key: value for key, value in _result.items() if value > 0}

        case _:
            raise ValueError(f"Unsupported Operation: {operation}")

    return dict(result)


def dict_from_file(file_path: str) -> Optional[dict[Any, Any]]:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise TypeError(f"Expected a dictionary, got {type(data).__name__}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except (IOError, EOFError):
        print(f"Cannot read the file: {file_path}")
    except json.JSONDecodeError:
        print("Malformed JSON")
    except TypeError as error:
        print(f"Invalid data format: {error}")
    except Exception as error:
        print(f"Unexpected Error occurred: {error}")
    else:
        return data
