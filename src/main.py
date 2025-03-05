from material import Material
import json
import pickle
from directed_acyclic_graph import topological_sort


material_totals = dict()


def create_material_from_definition(material_id, material_definition):
    # Creates a material object from given material dictionary

    material_id = material_id
    name = material_definition["typeName"]
    unit = material_definition["unit_size"]
    icon_id = material_definition["iconID"]
    level = material_definition["level"]
    group_id = material_definition["marketGroupID"]
    components = material_definition["components"]

    return Material(
        material_id=material_id,
        material_name=name,
        unit_size=unit,
        icon_id=icon_id,
        level=level,
        market_group_id=group_id,
        component_dict=components,
    )


def create_materials_from_file(file_name):
    # Creates a dictionary of materials from file containing json formatted data

    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Create material objects from file
    materials = {}
    for material_id, material_data in data.items():
        materials[material_id] = create_material_from_definition(
            material_id, material_data
        )

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
    try:
        with open("./data/pi_materials.pkl", "rb") as file:
            pi_materials = pickle.load(file)

    except (FileNotFoundError, IOError, EOFError):
        pi_materials = create_materials_from_file("./data/pi_materials.json")
        with open("./data/pi_materials.pkl", "wb+") as file:
            pickle.dump(pi_materials, file)
    
    try:
        with open("./data/topological_order.json") as file:
            order = json.load(file)
        
    except (FileNotFoundError, IOError):
        order = topological_sort(pi_materials)
        with open("./data/topological_order.json") as file:
            json.dump(order, file)


if __name__ == "__main__":
    main()