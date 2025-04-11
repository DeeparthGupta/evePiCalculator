from collections import Counter, defaultdict
import json
from typing import Any, Optional


def material_id_to_name(
    materials: dict[str, int], name_id_map: dict[str, str]
) -> Optional[dict[str, int]]:
    materials_dict = defaultdict(int)
    for material_id, quantity in materials.items():
        materials_dict[name_id_map[material_id]] = quantity

    return materials_dict


def material_name_to_id(
    materials: dict[str, int], id_name_map: dict[str, str]
) -> Optional[dict[str, int]]:
    materials_dict = defaultdict(int)
    for material_name, quantity in materials.items():
        materials_dict[id_name_map[material_name]] = quantity

    return materials_dict

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