from material import Material
import json


def create_material_from_definition(material_id, material_definition):
    # Creates a material object from given material dictionary

    material_id = material_id
    name = material_definition["typeName"]
    unit = material_definition["unit_size"]
    icon_id = material_definition["iconID"]
    level = material_definition["level"]
    group_id = material_definition["marketGroupID"]
    components = material_definition["components"]

    return Material(material_id=material_id, material_name=name, unit_size=unit, icon_id=icon_id, level=level, market_group_id=group_id, components=components)


def create_materials_from_file(file_name):
    # Creates a dictionary of materials from file containing json formatted data

    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Create material objects from file
    materials = {}
    for material_id, material_data in data.items():
        materials[material_id] = create_material_from_definition(material_id, material_data)

    return materials

def build_dependency_graph(materials_dict):
    dependency_graph = {}
    for material_id, material_def in materials_dict.items():
        dependency_graph[material_id] = list(material_def.components.items())
    
    return dependency_graph

def topological_sort(dependency_graph):
    pass


pi_materials = create_materials_from_file("./data/pi_materials.json")
material_graph = build_dependency_graph(pi_materials)

