"""
Contains utility functions for:
- Building the attack tree graph.
- Propagating values through the tree.
- Aggregating total impact or probability.
"""

import networkx as nx


def build_graph(tree, graph=None, parent=None):
    """
    Recursively builds a directed graph from the parsed attack tree dictionary.

    Parameters:
    - tree (dict): Attack tree in dictionary format.
    - graph (nx.DiGraph): Optional existing graph to add nodes into.
    - parent (str): Parent node's name, if applicable.

    Returns:
    - nx.DiGraph: Fully constructed graph.
    """
    if graph is None:
        graph = nx.DiGraph()

    node = tree["name"]
    graph.add_node(node, value=tree.get("value", 0))  # Default to 0 if missing

    if parent:
        graph.add_edge(parent, node)

    for child in tree.get("children", []):
        build_graph(child, graph, node)

    return graph


def propagate_values(graph, mode):
    """
    Computes values for all internal (non-leaf) nodes based on child node values.

    For monetary mode: sums child values.
    For probability mode: uses complementary probability (1 - product of (1 - p)).

    Parameters:
    - graph (nx.DiGraph): The attack tree graph.
    - mode (str): Either 'monetary' or 'probability'.
    """
    for node in reversed(list(nx.topological_sort(graph))):
        children = list(graph.successors(node))
        if not children:
            continue

        if mode == "monetary":
            graph.nodes[node]['value'] = sum(graph.nodes[c]['value'] for c in children)

        if mode == "probability":
            product = 1.0
            for c in children:
                product *= (1 - graph.nodes[c]['value'])
            graph.nodes[node]['value'] = round(1 - product, 6)


def aggregate_impact(graph, mode):
    """
    Computes the final overall impact or probability for the entire tree.

    Parameters:
    - graph (nx.DiGraph): The attack tree graph.
    - mode (str): Either 'monetary' or 'probability'.

    Returns:
    - float: Total aggregated leaf value (monetary) or root probability.
    """
    if mode == 'monetary':
        leaves = [n for n in graph.nodes if graph.out_degree(n) == 0]
        return sum(graph.nodes[n]['value'] for n in leaves)

    if mode == 'probability':
        roots = [n for n in graph.nodes if graph.in_degree(n) == 0]
        if roots:
            return graph.nodes[roots[0]]['value']
        return 0.0

    return 0.0  # fallback default for unsupported mode
