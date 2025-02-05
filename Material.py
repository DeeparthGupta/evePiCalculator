from ast import Dict
from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    material_name: str
    unit_size: int
    components: Dict[str, int]

    @property
    def name(self):
        return self.material_name

    @property
    def component_names(self):
        return self.components.keys()

    @property
    def components(self):
        return self.components

    @property
    def unit_size(self):
        return self.unit_size

    def __repr__(self):
        return (
            f"Material(name={self.material_name}, unit_size={self.unit_size}, "
            f"components={self.components!r})"
        )
