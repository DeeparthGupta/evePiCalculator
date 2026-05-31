import argparse
import json
import pathlib
import sys
from typing import Any

from errors import (
    CliUsageError,
    DataIntegrityError,
    DataLoadError,
    InputParseError,
    InputValidationError,
    PiCalcError,
    UnknownMaterialError,
    UnknownMaterialNameError,
)
from helper_functions import dict_from_file
from material_operations import (
    adjusted_cycles,
    calculate_material_requirements,
    create_master_data,
)

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
    arg_parser.add_argument(
        "--cycles",
        "-c",
        dest="calc_cycles",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument("-s", "--save", type=str, help="Output file")
    arg_parser.add_argument("input", nargs="?", help="Input string")

    return arg_parser.parse_args()


def get_master_data() -> dict:
    # Returns master data if it already exists or generates it from file.
    global master_data

    if master_data is None:
        pi_materials = dict_from_file(DATA_DIR / "pi_materials.json")
        if not pi_materials:
            raise DataLoadError(f"Input data is empty: {DATA_DIR / 'pi_materials.json'}")
        master_data = create_master_data(pi_materials)

    return master_data


def get_name_id_map() -> dict:
    global name_id_map

    if name_id_map is None:
        name_id_map = dict_from_file(DATA_DIR / "name_id_map.json")
    return name_id_map


def get_id_name_map() -> dict:
    global id_name_map

    if id_name_map is None:
        id_name_map = dict_from_file(DATA_DIR / "id_name_map.json")
    return id_name_map


def _validate_input_payload(input_data: Any) -> dict[str, int]:
    if not isinstance(input_data, dict):
        raise InputValidationError(
            f"Expected input payload as dictionary, got {type(input_data).__name__}"
        )

    normalized: dict[str, int] = {}
    for key, value in input_data.items():
        material_key = str(key)
        try:
            quantity = int(value)
        except (TypeError, ValueError) as error:
            raise InputValidationError(
                f"Invalid quantity for {material_key}: {value}"
            ) from error
        if quantity <= 0:
            raise InputValidationError(
                f"Invalid quantity for {material_key}: expected > 0, got {quantity}"
            )
        normalized[material_key] = quantity

    return normalized


def _validate_input_source(args: argparse.Namespace) -> None:
    has_file = args.file is not None
    has_inline_input = args.input is not None
    if has_file == has_inline_input:
        raise CliUsageError(
            "Provide exactly one input source: either --file FILE or inline JSON."
        )


def _parse_input_data(args: argparse.Namespace) -> dict[str, int]:
    _validate_input_source(args)

    if args.file:
        return _validate_input_payload(dict_from_file(args.file))

    try:
        parsed = json.loads(args.input)
    except json.JSONDecodeError as error:
        raise InputParseError(f"Malformed JSON input: {error.msg}") from error

    return _validate_input_payload(parsed)


def process_materials(
    input_data: dict[str, int],
    named_input: bool = False,
    named_output: bool = False,
    cycles: bool = False,
) -> dict[str, dict[str, int]]:
    input_data = _validate_input_payload(input_data)

    if named_input:
        name_id_map = get_name_id_map()
        missing_names = sorted([name for name in input_data if name not in name_id_map])
        if missing_names:
            raise UnknownMaterialNameError(
                f"Unknown material name(s): {', '.join(missing_names)}"
            )
        input_data = {name_id_map[k]: v for k, v in input_data.items()}

    master_data = get_master_data()

    output: dict[str, dict[str, int]] = {}
    for material_id, quantity in input_data.items():
        material_requirements = calculate_material_requirements(
            material_id, quantity, master_data
        )
        for level, requirements in material_requirements.items():
            if level not in output:
                output[level] = {}
            for requirement_id, quantity in requirements.items():
                output[level][requirement_id] = (
                    output[level].get(requirement_id, 0) + quantity
                )

    if cycles:
        for level, materials in output.items():
            for material_id in list(materials.keys()):
                materials[material_id] = adjusted_cycles(
                    materials[material_id], master_data[material_id].unit_size
                )

    if named_output:
        id_name_map = get_id_name_map()
        for level, materials in output.items():
            output[level] = {
                id_name_map.get(material_id, material_id): quantity
                for material_id, quantity in materials.items()
            }

    return output


def _save_output(output: dict[str, dict[str, int]], save_path: str) -> None:
    try:
        with open(save_path, "w", encoding="utf-8") as outfile:
            json.dump(output, outfile, indent=2)
    except OSError as error:
        raise DataLoadError(f"Error saving file {save_path}: {error}") from error


def _exit_code_for_error(error: PiCalcError) -> int:
    if isinstance(error, CliUsageError):
        return 2
    if isinstance(
        error,
        (InputParseError, InputValidationError, UnknownMaterialError, UnknownMaterialNameError),
    ):
        return 3
    if isinstance(error, (DataLoadError, DataIntegrityError)):
        return 4
    return 1


def main() -> int:
    args = parse_arguments()

    try:
        data = _parse_input_data(args)
        output = process_materials(data, args.named_in, args.named_out, args.calc_cycles)
        if args.save:
            _save_output(output, args.save)
        print(json.dumps(output, indent=2))
        return 0
    except PiCalcError as error:
        print(str(error), file=sys.stderr)
        return _exit_code_for_error(error)
    except Exception as error:
        print(f"Unexpected internal error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
