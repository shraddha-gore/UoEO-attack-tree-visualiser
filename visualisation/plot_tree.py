"""
Provides the visualisation logic for rendering attack trees using Matplotlib
and Graphviz (via pygraphviz). Nodes are coloured by their value to indicate
threat severity.

Author: [Your Name]
Date: [2025-07-15]
"""

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import colors
from networkx.drawing.nx_agraph import graphviz_layout


def draw_graph(graph, title, mode, total):
    """
    Draws the attack tree with colour-coded nodes and displays the impact or probability.

    Parameters:
    - graph (nx.DiGraph): The attack tree graph.
    - title (str): Name of the tree (used as suptitle).
    - mode (str): 'monetary' or 'probability'.
    - total (float): Total leaf impact or root probability.
    """
    # Try Graphviz layout first, fallback to spring layout
    try:
        pos = graphviz_layout(graph, prog="dot")
    except (ImportError, ValueError):
        print("Graphviz layout not available. Using spring layout.")
        pos = nx.spring_layout(graph, seed=42)

    # Normalise values for colouring
    values = [graph.nodes[n]['value'] for n in graph.nodes]
    norm = colors.Normalize(vmin=min(values), vmax=max(values))
    cmap = plt.colormaps['RdYlGn_r']
    node_colors = [cmap(norm(graph.nodes[n]['value'])) for n in graph.nodes]

    # Node labels and impact summary text
    if mode == "monetary":
        labels = {n: f"{n}\n£{int(graph.nodes[n]['value'])}" for n in graph.nodes}
        summary_text = f"Total Aggregated Leaf Impact: £{total:.2f}"
    else:
        labels = {n: f"{n}\nP={graph.nodes[n]['value']:.2f}" for n in graph.nodes}
        summary_text = f"Overall Probability of Attack Success: {total:.2%}"

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.canvas.manager.set_window_title(title)

    # Title and subtitle
    plt.suptitle(title, fontsize=16, y=0.98)
    plt.title(summary_text, fontsize=12, pad=30)

    # Draw the attack tree
    nx.draw(
        graph,
        pos,
        ax=ax,
        labels=labels,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        font_size=9,
        font_weight='bold',
        edge_color='gray',
        arrows=True
    )

    plt.subplots_adjust(top=0.85)  # Space between plot and title
    plt.tight_layout()
    plt.show()
