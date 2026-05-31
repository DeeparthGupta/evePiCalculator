# EVE PI Calculator

Python tool for EVE Online planetary interaction (PI) material planning.

## Functionality

In EVE Online, Planetary interaction involves multi stage chains of production where extracted materials are progressively processed to prodice higher tier materials.

- Loads PI material definitions and production recipes from `data/pi_materials.json`
- Accepts desired materials as `{material_id: quantity}` pairs.
- Supports mixed tier inputs in one request.
- Computes all intermediate and raw materials required for production.
- Supports material IDs or material names for input and output.
- Optionally adjusts quantities to production batch sizes (number of cycles).
- Outputs results as nested JSON grouped by production tier.

## Usage

From project root:

```sh
python src/pi_calculator.py -f input.json --named-in --named-out --cycles -s output.json
```

Or pass inline JSON:

```sh
python src/pi_calculator.py '{"44": 10, "2344": 2}'
python src/pi_calculator.py '{"Cryoprotectant Solution": 20}'
```

## Options

- `-f FILE` : read input from a JSON file.
- `--named-in` : interpret input keys as material names.
- `--named-out` : return output keys as material names.
- `-c, --cycles` : apply batch-size adjustments.
- `-s FILE` : save output JSON to a file.

## Planned Enhancements

- Eliminate repeated traversals of the same subtree.
- Repeated traversals create multiple dependency accumulators of the same structure which are then combined.
- A better idea is to merge multiple instances of a material and then create a dependency accumulator on the combined value.
