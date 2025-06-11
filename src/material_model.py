from dataclasses import dataclass
from typing import Any, Dict


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
        # Type validation and conversion of fields
        try:
            material_name = str(material_definition["typeName"])
            unit_size = int(material_definition["unit_size"])
            icon_id = str(material_definition["iconID"])
            level = int(material_definition["level"])
            market_group_id = str(material_definition["marketGroupID"])

        except KeyError as error:
            raise KeyError(f"Missing required field: {error.args[0]}") from error
        except (TypeError, ValueError) as error:
            raise ValueError(f"Error converting field types: {error}") from error

        # Type validation and conversion of components
        components_raw = material_definition.get("components", {})
        if not isinstance(components_raw, dict):
            raise TypeError("Components has to be a dictionary.")

        components: Dict[str, int] = {}
        for key, value in components_raw.items():
            try:
                components[str(key)] = int(value)
            except (TypeError, ValueError) as error:
                raise ValueError(f"Error converting component {key}: {error}")

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
        return f"Material(id={self.material_id}, name={self.material_name}, unit_cycle={self.unit_size}"
