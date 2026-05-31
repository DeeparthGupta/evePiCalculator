from math import ceil
from typing import Any, Dict

from errors import DataIntegrityError, UnknownMaterialError
from material_model import Material

LEVEL_MAP: Dict[int, str] = {
    0: "Raw Materials",
    1: "Processed Materials",
    2: "Refined Commodities",
    3: "Specialized Commodities",
    4: "Advanced Commodities",
}


def create_master_data(material_dictionary: Dict[str, Any]) -> Dict[str, Material]:
    materials: Dict[str, Material] = {}
    for material_id, material_data in material_dictionary.items():
        materials[material_id] = Material.from_dict(material_id, material_data)

    validate_master_data(materials)
    return materials


def adjusted_cycles(quantity: int, unit_size: int) -> int:
    if unit_size <= 0:
        raise DataIntegrityError(
            f"Invalid unit_size for cycle calculation: expected > 0, got {unit_size}"
        )
    return ceil(quantity / unit_size)


def quantity_from_cycles(cycles: int, unit_size: int) -> int:
    return cycles * unit_size


def level_name(level: int) -> str:
    if level not in LEVEL_MAP:
        raise DataIntegrityError(
            f"Unsupported material level: {level}. Allowed levels: {sorted(LEVEL_MAP.keys())}"
        )
    return LEVEL_MAP[level]


def _validate_levels_and_unit_sizes(material_data: Dict[str, Material]) -> None:
    for material in material_data.values():
        if material.level not in LEVEL_MAP:
            raise DataIntegrityError(
                f"Material {material.id} has unsupported level {material.level}. "
                f"Allowed levels: {sorted(LEVEL_MAP.keys())}"
            )
        if material.unit_size <= 0:
            raise DataIntegrityError(
                f"Material {material.id} has invalid unit_size {material.unit_size}. Expected > 0."
            )


def _detect_cycle_path(material_data: Dict[str, Material]) -> list[str] | None:
    visited: set[str] = set()
    in_stack: set[str] = set()
    stack: list[str] = []

    def dfs(node_id: str) -> list[str] | None:
        visited.add(node_id)
        in_stack.add(node_id)
        stack.append(node_id)

        for component_id in material_data[node_id].components:
            if component_id not in material_data:
                continue
            if component_id not in visited:
                cycle_path = dfs(component_id)
                if cycle_path:
                    return cycle_path
            elif component_id in in_stack:
                cycle_start = stack.index(component_id)
                return stack[cycle_start:] + [component_id]

        stack.pop()
        in_stack.remove(node_id)
        return None

    for material_id in material_data:
        if material_id not in visited:
            cycle_path = dfs(material_id)
            if cycle_path:
                return cycle_path
    return None


def _validate_cycles(material_data: Dict[str, Material]) -> None:
    cycle_path = _detect_cycle_path(material_data)
    if cycle_path:
        raise DataIntegrityError(
            f"Cyclic dependency detected in master data: {' -> '.join(cycle_path)}"
        )


def validate_master_data(material_data: Dict[str, Material]) -> None:
    _validate_levels_and_unit_sizes(material_data)
    _validate_cycles(material_data)


def calculate_material_requirements(
    material: str, quantity: int, material_data: Dict[str, Material]
) -> Dict[str, Dict[str, int]]:
    if material not in material_data:
        raise UnknownMaterialError(f"Unknown material ID: {material}")

    if quantity <= 0:
        raise DataIntegrityError(
            f"Invalid quantity for material {material}: expected > 0, got {quantity}"
        )

    accumulator: Dict[str, Dict[str, int]] = {}
    material_definition = material_data[material]
    lvl = level_name(material_definition.level)
    if lvl not in accumulator:
        accumulator[lvl] = {}
    accumulator[lvl][material_definition.id] = (
        accumulator[lvl].get(material_definition.id, 0) + quantity
    )

    if material_definition.components:
        for (
            component_id,
            material_requirement,
        ) in material_definition.components.items():
            if component_id not in material_data:
                raise DataIntegrityError(
                    f"Unknown component reference in material {material_definition.id}: {component_id}"
                )
            required_components = calculate_material_requirements(
                component_id,
                adjusted_cycles(quantity, material_definition.unit_size)
                * material_requirement,
                material_data,
            )

            for lvl, reqs in required_components.items():
                if lvl not in accumulator:
                    accumulator[lvl] = {}
                for mat_id, qty in reqs.items():
                    accumulator[lvl][mat_id] = accumulator[lvl].get(mat_id, 0) + qty

    return accumulator
