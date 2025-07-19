"""
Core logic for the Attack Tree Visualiser & Aggregator application.

Handles:
- Input validation
- Value propagation
- Aggregation of threat data
- User prompting for updates
"""

from utils.graph_utils import build_graph, propagate_values, aggregate_impact
from utils.io_handler import load_attack_tree
from visualisation.plot_tree import draw_graph


def validate_values(graph, mode):
    """
    Validates that all node values are appropriate for the selected interpretation mode.

    Parameters:
    - graph (nx.DiGraph): The attack tree.
    - mode (str): 'monetary' or 'probability'

    Raises:
    - ValueError if any node has invalid values.
    """
    for n in graph.nodes:
        v = graph.nodes[n]['value']
        if mode == "probability":
            if not 0.0 <= v <= 1.0:
                raise ValueError(
                    f"Invalid probability: node '{n}' has value {v}, "
                    "must be between 0 and 1."
                )
        elif mode == "monetary":
            if v < 0 or not float(v).is_integer():
                raise ValueError(
                    f"Invalid monetary value: node '{n}' has value {v}, "
                    "must be a non-negative integer."
                )


def prompt_leaf_values(graph, mode):
    """
    Prompts the user to update values for each leaf node.

    Parameters:
    - graph (nx.DiGraph): The attack tree.
    - mode (str): Interpretation mode ('monetary' or 'probability').

    Notes:
    - Invalid inputs are re-prompted until valid or left blank.
    """
    print("\nEnter updated values for leaf nodes (leave blank to keep current):")
    leaves = [n for n in graph.nodes if graph.out_degree(n) == 0]

    for leaf in leaves:
        current = graph.nodes[leaf]['value']
        prompt_val = f"£{int(current)}" if mode == "monetary" else f"P={current:.2f}"

        while True:
            raw = input(f"{leaf} [current: {prompt_val}]: ").strip()
            if not raw:
                break  # Keep existing value
            try:
                val = float(raw)
                if mode == "probability":
                    if not 0.0 <= val <= 1.0:
                        print("Value must be between 0.0 and 1.0 for probability.")
                        continue
                elif mode == "monetary":
                    if val < 0 or not float(val).is_integer():
                        print("Monetary value must be a non-negative whole number.")
                        continue
                graph.nodes[leaf]['value'] = val
                break  # Valid input
            except ValueError:
                print("Invalid input. Please enter a numeric value or leave blank to skip.")



def run_analysis(file_path, mode):
    """
    Orchestrates the attack tree analysis process from start to finish.

    Parameters:
    - file_path (str): Path to the attack tree file.
    - mode (str): 'monetary' or 'probability'

    Steps:
    - Load tree from file
    - Validate initial values
    - Prompt user for updates
    - Revalidate
    - Propagate and aggregate
    - Draw graph
    - Print summary
    """
    tree_data = load_attack_tree(file_path)
    graph = build_graph(tree_data)

    validate_values(graph, mode)
    prompt_leaf_values(graph, mode)
    validate_values(graph, mode)

    propagate_values(graph, mode)
    total = aggregate_impact(graph, mode)

    title = f"{tree_data['name']} Attack Tree"
    draw_graph(graph, title, mode, total)

    if mode == 'monetary':
        print(f"\nTotal Aggregated Leaf Impact: £{total:.2f}")
    else:
        print(f"\nOverall Probability of Attack Success: {total:.2%}")
