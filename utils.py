import re


def get_components(material, material_data, id_name_mapping, names=False):
    if re.match(r"^\d$", material):
        mat_info = (
            f"{material} : {material_data[material]['typeName']}" if names else material
        )
        components = material_data[material]["components"]
    else:
        mat_info = f"{material} : {id_name_mapping[material]}" if names else material
        components = material_data[id_name_mapping[material]]["components"]

    print(mat_info)

    if names:
        result = [material_data[key]["typeName"] for key in components.keys()]
        print(result)

    else:
        print(components.keys())


def get_ids(names: list, name_map: dict) -> list:
    names[:] = map(str, names)
    return [name_map[name] for name in names]
