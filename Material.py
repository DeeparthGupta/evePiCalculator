class Material:
    def __init__(self, material_name: str = None, unit_size: int = 0, components: dict = None):
        self.name = material_name
        self.unit_size = unit_size
        self.components = {} if components is None else components