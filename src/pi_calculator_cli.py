import argparse
import json
import sys
from collections import defaultdict

from material_operations import (
    calculate_material_requirements,
    create_master_data,
)
from helper_functions import dict_binary_operation, dict_from_file


def parse_arguments() -> argparse.Namespace:
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
        "--named-in",
        action="store_true",
        help="Specify whether the input file contains material names or ids",
        dest="named_in",
        default=True,
    )
    arg_parser.add_argument(
        "--named-out",
        action="store_true",
        help="Specify whether to output material names or IDs.",
        dest="named_out",
        default=True,
    )
    arg_parser.add_argument("-s", "--save", type=str, help="Output file")
    arg_parser.add_argument("input", nargs="?", help="Input string")

    return arg_parser.parse_args()


def main() -> None:
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
                sys.exit(1)

        else:
            try:
                data = json.loads(args.input)

                if not isinstance(data, dict):
                    raise TypeError(f"Expected a dictionary, got {type(data).__name__}")

            except json.JSONDecodeError:
                print("Malformed JSON")
                sys.exit(1)
            except TypeError as error:
                print(f"Invalid data format: {error}")
                sys.exit(1)
            except Exception as error:
                print(f"Unexpected Error occurred: {error}")
                sys.exit(1)

        if args.named_in:
            try:
                name_id_map = dict_from_file("/data/name_id_map.json")
            except Exception as error:
                print(f"Unable to process material names: {error}")
            else:
                data = {name_id_map[k]: v for k, v in data.items()}

        output = defaultdict(int)
        for material_id, quantity in data.items():
            material_requirements = calculate_material_requirements(
                material_id, quantity, master_data
            )
            output = dict_binary_operation("add", output, material_requirements)

        if args.named_out:
            try:
                id_name_map = dict_from_file("/data/id_name_map.json")
            except Exception as error:
                print(f"Unable to create material names: {error}")
            else:
                output = {id_name_map[k]: v for k, v in output.items()}

        if args.save:
            try:
                print("Saving output to file")
                with open(args.save, "w") as outfile:
                    json.dump(output, outfile, indent=2)
            except Exception as error:
                print(f"Error saving file: {error}")

        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
