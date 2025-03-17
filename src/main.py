from collections import defaultdict, Counter
import sys
from material import Material
import json
import argparse
from typing import Any


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


def create_materials_from_file(file_path: str) -> dict[str, Material] | None:
    # Creates a dictionary of materials from file containing json formatted data
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (FileNotFoundError, IOError, EOFError):
        print(f"Cannot read file: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Malformed JSON:{file_path}")
        return None
    except Exception as error:
        print(f"An unexpected error occured:{error}")
        return None
    else:
        # Create material objects from file
        materials = {}
        for material_id, material_data in data.items():
            materials[material_id] = create_material_from_definition(
                material_id, material_data
            )

        return materials


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


def main():
    print("Creating material data.")
    pi_materials = create_materials_from_file("./data/pi_materials.json")
    if pi_materials is None:
        print("Failed to load material data. Exiting...")
        sys.exit(1)

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
    arg_parser.add_argument("-s", "--save", type=str, help="Output file")
    arg_parser.add_argument("-n", "--named", action="store_true", help="Specify whether to output material names or IDs.")
    arg_parser.add_argument("input", nargs="?", help="Input string")

    args = arg_parser.parse_args()

    if args.file:
        try:
            with open(args.file) as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise TypeError(f"Expected a dictionary, got {type(data).__name__}")

        except FileNotFoundError:
            print(f"File not found: {args.file}")
        except (IOError, EOFError):
            print(f"Cannot read the file: {args.file}")
        except json.JSONDecodeError:
            print("Malformed JSON")
        except TypeError as error:
            print(f"Invalid data format: {error}")
        except Exception as error:
            print(f"Unexpected Error occurred: {error}")
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
                    material_id, quantity, pi_materials
                )

                output = dict_binary_operation("add", output, material_requirements)
        
            if args.save:
                try:
                    print('Saving output to file')
                    with open(args.save, 'w') as outfile:
                        json.dump(output, outfile)
                except Exception as error:
                    print(f'Error saving file: {error}')
            
            print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
