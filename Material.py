from dataclasses import dataclass, field


@dataclass
class Material:
    material_name: str = None
    unit_size: int = 0
    components: dict = field(default_factory=dict)

    def get_name(self):
        return self.material_name

    def get_component_names(self):
        return self.components
