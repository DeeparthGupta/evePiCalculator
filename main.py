import json
from Material import Material


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
    materials = {}
    for material_name in data.keys():
        materials[material_name] = create_material_from_definition(data[material_name])

    return materials


def create_totals_dict():
    totals = {}
    return totals
