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


def adjusted_cycles(quantity: int, unit_size: int) -> int:
    return round(quantity / unit_size)


def quantity_from_cycles(cycles: int, unit_size: int) -> int:
    return cycles * unit_size

def calculate_material_requirements(
    material: str, quantity: int, material_data: Dict[str, Material]
) -> Dict[str, int]:
    accumulator = defaultdict(int)
    material_definition = material_data[material]
    accumulator[material_definition.id] += quantity

    if material_definition.components:
        for (
            component_id,
            material_requirement,
        ) in material_definition.components.items():
            required_components = calculate_material_requirements(
                component_id,
                adjusted_cycles(quantity, material_definition.unit_size) * material_requirement,
                material_data,
            )
            accumulator = dict_binary_operation("add", accumulator, required_components)
            

    return accumulator
