from collections import defaultdict, Counter
import sys
from material import Material
import json
import argparse
from typing import Any, Optional


def create_master_data(material_dictionary: dict[str, Any]) -> dict[str, Material]:
    # Create Master data
    materials = defaultdict()
    for material_id, material_data in material_dictionary.items():
        materials[material_id] = create_material_from_definition(
            material_id, material_data
        )

    return materials


def calculate_material_requirements(
    material: str, quantity: int, material_map: dict[str, Material]
) -> dict[str, int]:
    accumulator = defaultdict(int)
    material_definition = material_map[material]
    if material_definition.components:
        for component_id, unit_size in material_definition.components.items():
            required_components = calculate_material_requirements(
                component_id, quantity * unit_size, material_map
            )
            accumulator = dict_binary_operation("add", accumulator, required_components)

    else:
        accumulator[material_definition.id] += quantity

    return accumulator


def create_material_from_definition(
    material_id: str, material_definition: dict[str, Any]
) -> Material:
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


def dict_binary_operation(
    operation: str, dict1: dict[str, int], dict2: dict[str, int]
) -> dict[str, int]:
    match operation:
        case "add":
            result = Counter(dict1) + Counter(dict2)

        case "sub":
            _result = Counter(dict1) - Counter(dict2)
            result = {key: value for key, value in _result.items() if value > 0}

        case _:
            raise ValueError(f"Unsupported Operation: {operation}")

    return dict(result)


def material_id_to_name(
    materials: dict[str, int], name_id_map: dict[str, str]
) -> dict[str, int]:
    named_materials = {}
    for material_id, quantity in materials.items():
        named_materials[name_id_map[material_id]] = quantity

    return named_materials


def dict_from_file(file_path: str) -> Optional[dict[Any, Any]]:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise TypeError(f"Expected a dictionary, got {type(data).__name__}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except (IOError, EOFError):
        print(f"Cannot read the file: {file_path}")
    except json.JSONDecodeError:
        print("Malformed JSON")
    except TypeError as error:
        print(f"Invalid data format: {error}")
    except Exception as error:
        print(f"Unexpected Error occurred: {error}")
    else:
        return data


def parse_arguments():
    arg_parser = argparse.ArgumentParser(
        description="Process PI materials from file or from a valid json string"
    )
    arg_parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Input path of the file containing material requirements",
        dest="file",
        default=None,
    )
    arg_parser.add_argument(
        "-n",
        "--named",
        action="store_true",
        help="Specify whether to output material names or IDs.",
    )
    arg_parser.add_argument("-s", "--save", type=str, help="Output file")
    arg_parser.add_argument("input", nargs="?", help="Input string")

    return arg_parser.parse_args()


def main():
    print("Creating material data.")
    try:
        pi_materials = dict_from_file("./data/pi_materials.json")
        if not pi_materials:
            raise ValueError("Input data is empty.")
    except Exception as error:
        print(f"Unable to load Material data: {error}")
        print("Exiting...")
        sys.exit(1)
    else:
        master_data = create_master_data(pi_materials)

    args = parse_arguments()

    if args.file:
        try:
            data = dict_from_file(args.file)
        except Exception as error:
            print(f"An Error has occured: {error}")

    else:
        try:
            data = json.loads(args.input)

            if not isinstance(data, dict):
                raise TypeError(f"Expected a dictionary, got {type(data).__name__}")

        except json.JSONDecodeError:
            print("Malformed JSON")
        except TypeError as error:
            print(f"Invalid data format: {error}")
        except Exception as error:
            print(f"Unexpected Error occurred: {error}")

        else:
            output = defaultdict(int)
            for material_id, quantity in data.items():
                material_requirements = calculate_material_requirements(
                    material_id, quantity, master_data
                )

                output = dict_binary_operation("add", output, material_requirements)

            if args.named:
                try:
                    name_id_map = dict_from_file("/data/name_id_map.json")
                    if not name_id_map:
                        raise ValueError("Unable to read name-id map.")               
                except Exception as error: 
                    print(f"Unable to name materials: {error}")
                else:
                    output = material_id_to_name(output, name_id_map)

            if args.save:
                try:
                    print("Saving output to file")
                    with open(args.save, "w") as outfile:
                        json.dump(output, outfile)
                except Exception as error:
                    print(f"Error saving file: {error}")

            print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
