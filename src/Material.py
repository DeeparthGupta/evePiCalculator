from typing import Dict
from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    material_id: str
    material_name: str
    unit_size: int
    icon_id: str
    level: int
    market_group_id: int
    components: Dict[str, int]

    @property
    def name(self):
        return self.material_name
    
    @property
    def id(self):
        return self.material_id

    @property
    def components(self):
        return self.components

    @property
    def unit_size(self):
        return self.unit_size   

    def __repr__(self):
        return (
            f"Material(id={self.material_id}, name={self.material_name}, unit_size={self.unit_size}, "
            f"components={self.components!r})"
        )
