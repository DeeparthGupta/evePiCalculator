import json
from Material import Material

material_totals = dict(None)

def create_material_from_definition(material_definition):
    # Creates a material object from given material dictionary

    name = material_definition.name
    components = material_definition.components
    unit_size = material_definition.unit_size

    return Material(name, unit_size, components)


def create_materials_from_file(file_name):
    # Creates a dictionary of materials from file containing json formatted data

    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Create material objects from file
    materials = dict(None)
    for material_name in data.keys():
        materials[material_name] = create_material_from_definition(data[material_name])

    return materials


def add_to_quantity(name, quantity):
# Adds a key value pair if the key doesn't exist and adds to the existing value if it does

    if name not in material_totals.keys():
        material_totals[name] = quantity
    
    else:
        existing_quantity = material_totals[name]
        material_totals[name] = existing_quantity + quantity


def subtract_from_quantity(name, quantity):
    if name in material_totals:
        new_quantity = material_totals[name] - quantity

        if new_quantity < 0:
            remove_material(name)
        
        else:
            material_totals[name] = new_quantity


def remove_material(name):
# Removes a key value pair if it exists in totals
    if name in material_totals.keys():
        material_totals.pop(name)
