from collections import defaultdict
from typing import Any, Dict

from material_model import Material
from helper_functions import dict_binary_operation


def create_master_data(material_dictionary: Dict[str, Any]) -> Dict[str, Material]:
    # Create Master data
    materials = defaultdict()
    for material_id, material_data in material_dictionary.items():
        materials[material_id] = Material.from_dict(material_id, material_data)

    return materials


def calculate_material_requirements(
    material: str, quantity: int, material_map: Dict[str, Material]
) -> Dict[str, int]:
    accumulator = defaultdict(int)
    material_definition = material_map[material]
    accumulator[material_definition.id] += quantity
    
    if material_definition.components:
        for component_id, unit_size in material_definition.components.items():
            required_components = calculate_material_requirements(
                component_id, quantity * unit_size, material_map
            )
            accumulator = dict_binary_operation("add", accumulator, required_components)

    else:
        accumulator[material_definition.id] += quantity

    return accumulator
