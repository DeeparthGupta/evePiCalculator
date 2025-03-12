from collections import defaultdict, Counter
from material import Material
import json
import pickle
from typing import Any, Dict


material_totals = dict()


def create_material_from_definition(
    material_id: str, material_definition: dict[str, Any]
) -> Material:
    # Creates a material object from given material dictionary

    material_id = material_id
    name = material_definition["typeName"]
    unit = material_definition["unit_size"]
    icon_id = material_definition["iconID"]
    level = material_definition["level"]
    group_id = material_definition["marketGroupID"]
    components = material_definition["components"]

    return Material(
        material_id=material_id,
        material_name=name,
        unit_size=unit,
        icon_id=icon_id,
        level=level,
        market_group_id=group_id,
        component_dict=components,
    )


def create_materials_from_file(file_path: str) -> dict[str, Material]:
    # Creates a dictionary of materials from file containing json formatted data

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Create material objects from file
    materials = {}
    for material_id, material_data in data.items():
        materials[material_id] = create_material_from_definition(
            material_id, material_data
        )

    return materials


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


def calculate_material_requirements(
    material: Material, quantity: int, material_map: dict[str, Material]
) -> Dict[str, int]:
    accumulator = defaultdict(int)
    if material.components:
        for component_id, unit_size in material.components.items():
            required_components = calculate_material_requirements(
                material_map[component_id], quantity * unit_size, material_map
            )
            accumulator = dict_binary_operation("add", accumulator, required_components)

    else:
        accumulator[material.id] += quantity

    return accumulator


def main():
    try:
        with open("./data/pi_materials.pkl", "rb") as file:
            pi_materials = pickle.load(file)

    except (FileNotFoundError, IOError, EOFError):
        pi_materials = create_materials_from_file("./data/pi_materials.json")
        with open("./data/pi_materials.pkl", "wb+") as file:
            pickle.dump(pi_materials, file)


if __name__ == "__main__":
    main()
