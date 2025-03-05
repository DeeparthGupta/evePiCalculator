import collections


def build_dependency_map(materials_dict):
    # Creates a dictionary of components and the materials that need them
    dependency_map = collections.defaultdict(list)
    for material_id, material_def in materials_dict.items():
        for component_id, _ in material_def.components.items():
            dependency_map[component_id].append(material_id)

    return dependency_map


def topological_sort(materials_dict):
    # Topologically sort materials using Kahn's Algorithm
    in_degree = {
        material_id: len(material_def.components)
        for material_id, material_def in materials_dict.items()
    }
    queue = collections.deque(
        [material_id for material_id, degree in in_degree.items() if degree == 0]
    )

    dependency_map = build_dependency_map(materials_dict)

    order = list()

    while queue:
        # Pop an item from the queue and put it in the the order list
        node = queue.popleft()
        order.append(node)

        for neighbor in dependency_map[node]:
            in_degree[neighbor] -= 1

            # If indegree becomes 0 push the item to the queue
            if in_degree[neighbor] == 0:
                queue.append(node)

    return order
