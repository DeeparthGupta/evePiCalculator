import argparse
import json
import pathlib
import sys
from collections import defaultdict

from helper_functions import dict_binary_operation, dict_from_file
from material_operations import calculate_material_requirements, create_master_data

# Paths
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Global variables for data
master_data = None
name_id_map = None
id_name_map = None


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
        default=False,
    )
    arg_parser.add_argument(
        "--named-out",
        action="store_true",
        help="Specify whether to output material names or IDs.",
        dest="named_out",
        default=False,
    )
    arg_parser.add_argument("-s", "--save", type=str, help="Output file")
    arg_parser.add_argument("input", nargs="?", help="Input string")

    return arg_parser.parse_args()


def get_master_data() -> dict | None:
    # Returns master data if it already exists or genereates it from file
    global master_data

    if not master_data:
        print("Creating material data.")
        try:
            pi_materials = dict_from_file(DATA_DIR / "pi_materials.json")
            if not pi_materials:
                raise ValueError("Input data is empty.")

        except Exception as error:
            print(f"Unable to load Material data: {error}")
            return None

        else:
            # Creates a dictionary of Material objects
            master_data = create_master_data(pi_materials)

    return master_data


def get_name_id_map() -> dict | None:
    # Return id_name_map if it already exists or load it from file
    global name_id_map

    if not name_id_map:
        try:
            name_id_map = dict_from_file(DATA_DIR / "name_id_map.json")

        except Exception as exception:
            print(f"Unable to load name to ID mapping: {exception}")
            return None

        else:
            return name_id_map


def get_id_name_map() -> dict | None:
    # Return id_name_map if it already exists or load it from file
    global id_name_map

    if not id_name_map:
        try:
            id_name_map = dict_from_file(DATA_DIR / "id_name_map.json")

        except Exception as exception:
            print(f"Unable to load ID to name mapping: {exception}")
            return None

        else:
            return id_name_map


def process_materials(input, named_input=False, named_output=False) -> dict | None:
    # Process input materials
    master_data = get_master_data()
    name_id_map = get_name_id_map()
    id_name_map = get_id_name_map()

    if master_data:
        if named_input and name_id_map:
            input = {name_id_map[k]: v for k, v in input.items()}

        output = defaultdict(int)
        for material_id, quantity in input.items():
            material_requirements = calculate_material_requirements(
                material_id, quantity, master_data
            )
            output = dict_binary_operation("add", output, material_requirements)

        if named_output and id_name_map:
            output = {id_name_map[k]: v for k, v in output.items()}

        return output

    else:
        return None


def main() -> None:
    args = parse_arguments()

    # If source is a file
    if args.file:
        try:
            data = dict_from_file(args.file)
        except Exception as error:
            print(f"An Error has occured: {error}")
            sys.exit(1)
    # Else try to load a dict from terminal
    else:
        try:
            data = json.loads(args.input)

            if not isinstance(data, dict):
                raise TypeError(f"Expected a dictionary, got {type(data).__name__}")

        except json.JSONDecodeError as error:
            print(f"Malformed JSON: {error.msg}")
            sys.exit(1)
        except TypeError as error:
            print(f"Invalid data format: {error}")
            sys.exit(1)
        except Exception as error:
            print(f"Unexpected Error occurred: {error}")
            sys.exit(1)

    output = process_materials(data, args.named_in, args.named_out)
    if not output:
        print("An Error has occured.")
        sys.exit(1)

    # Save output to file
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
