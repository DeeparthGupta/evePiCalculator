from dataclasses import dataclass
from typing import Any, Dict

from errors import DataIntegrityError


@dataclass(frozen=True)
class Material:
    material_id: str
    material_name: str
    unit_size: int
    icon_id: str
    level: int
    market_group_id: str
    component_dict: Dict[str, int]

    @property
    def name(self):
        return self.material_name

    @property
    def id(self):
        return self.material_id

    @property
    def components(self):
        return self.component_dict

    @property
    def unit_cycle(self):
        return self.unit_size

    @classmethod
    def from_dict(
        cls, material_id: str, material_definition: Dict[str, Any]
    ) -> "Material":
        if not isinstance(material_definition, dict):
            raise DataIntegrityError(
                f"Invalid material definition for {material_id}: expected dictionary."
            )

        try:
            material_name = str(material_definition["typeName"])
            unit_size = int(material_definition["unit_size"])
            icon_id = str(material_definition["iconID"])
            level = int(material_definition["level"])
            market_group_id = str(material_definition["marketGroupID"])
        except (TypeError, ValueError) as error:
            raise DataIntegrityError(
                f"Error converting field types for {material_id}: {error}"
            ) from error
        except KeyError as error:
            raise DataIntegrityError(
                f"Missing required field for {material_id}: {error.args[0]}"
            ) from error

        if unit_size <= 0:
            raise DataIntegrityError(
                f"Invalid unit_size for {material_id}: expected > 0, got {unit_size}"
            )

        components_raw = material_definition.get("components", {})
        if not isinstance(components_raw, dict):
            raise DataIntegrityError(f"Components for {material_id} must be a dictionary.")

        components: Dict[str, int] = {}
        for key, value in components_raw.items():
            try:
                component_quantity = int(value)
            except (TypeError, ValueError) as error:
                raise DataIntegrityError(
                    f"Error converting component quantity for {material_id}->{key}: {error}"
                ) from error
            if component_quantity <= 0:
                raise DataIntegrityError(
                    f"Invalid component quantity for {material_id}->{key}: expected > 0, got {component_quantity}"
                )
            components[str(key)] = component_quantity

        return cls(
            material_id=material_id,
            material_name=material_name,
            unit_size=unit_size,
            icon_id=icon_id,
            level=level,
            market_group_id=market_group_id,
            component_dict=components,
        )

    def __repr__(self):
        return f"Material(id={self.material_id}, name={self.material_name}, unit_cycle={self.unit_size})"
