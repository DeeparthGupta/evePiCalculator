material_totals = dict()


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
    pass
