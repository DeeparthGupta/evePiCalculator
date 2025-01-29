import json
from Material import Material

def create_material_from_definition(material_definition):
    name = material_definition.name
    components = material_definition.components
    unit_size = material_definition.unit_size
    
    return Material(name, unit_size, components)

def create_materials_from_file(file_name):
    
    # Read materials and their relationships from file
    with open(file_name, 'r') as file:
        data = json.load(file)
    
    # Create material objects from file
    materials = {}
    for material in data.keys():
        materials[material] = create_material_from_definition(data[material])
    
    return materials
