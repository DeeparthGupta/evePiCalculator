import json

from Material import Material

material_totals = dict(None)


def create_material_from_definition(material_definition):
    # Creates a material object from given material dictionary

    material_id = material_definition.key()
    name = material_definition["typeName"]
    unit = material_definition["unit_size"]
    icon_id = material_definition["iconID"]
    level = material_definition["level"]
    group_id = material_definition["marketGroupID"]
    components = material_definition["components"]

    return Material(material_id, name, unit, icon_id, level, group_id, components)


def create_materials_from_file(file_name):
    # Creates a dictionary of materials from file containing json formatted data

    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Create material objects from file
    materials = {}
    for material_name in data:
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
    # Removes a key value pair from material_totals if it exists

    if name in material_totals:
        material_totals.pop(name)


def main():
    materials_data_path = "data/pi_materials.json"
    pi_materials = create_materials_from_file(materials_data_path)
