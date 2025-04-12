from collections import defaultdict
from typing import Any, Optional

from material import Material
from utils import dict_binary_operation


def create_master_data(material_dictionary: dict[str, Any]) -> dict[str, Material]:
    # Create Master data
    materials = defaultdict()
    for material_id, material_data in material_dictionary.items():
        materials[material_id] = create_material_from_definition(
            material_id, material_data
        )

    return materials


def calculate_material_requirements(
    material: str, quantity: int, material_map: dict[str, Material]
) -> dict[str, int]:
    accumulator = defaultdict(int)
    material_definition = material_map[material]
    if material_definition.components:
        for component_id, unit_size in material_definition.components.items():
            required_components = calculate_material_requirements(
                component_id, quantity * unit_size, material_map
            )
            accumulator = dict_binary_operation("add", accumulator, required_components)

    else:
        accumulator[material_definition.id] += quantity

    return accumulator


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
