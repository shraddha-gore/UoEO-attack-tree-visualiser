"""
Unit tests for validation and input handling in core.py.
"""

import pytest
import networkx as nx
from core import validate_values, prompt_leaf_values


@pytest.fixture
def monetary_graph():
    """
    Creates a sample attack tree graph for monetary mode.
    """
    G = nx.DiGraph()
    G.add_node("Leaf1", value=500)
    G.add_node("Leaf2", value=1000)
    G.add_node("Root", value=0)
    G.add_edge("Root", "Leaf1")
    G.add_edge("Root", "Leaf2")
    return G


@pytest.fixture
def probability_graph():
    """
    Creates a sample attack tree graph for probability mode.
    """
    G = nx.DiGraph()
    G.add_node("Leaf1", value=0.4)
    G.add_node("Leaf2", value=0.6)
    G.add_node("Root", value=0.0)
    G.add_edge("Root", "Leaf1")
    G.add_edge("Root", "Leaf2")
    return G


def test_validate_values_monetary_valid(monetary_graph):
    """
    Ensure monetary values are accepted when valid.
    """
    validate_values(monetary_graph, "monetary")


def test_validate_values_probability_valid(probability_graph):
    """
    Ensure probability values are accepted when within range.
    """
    validate_values(probability_graph, "probability")


def test_validate_values_invalid_monetary():
    """
    Negative or non-integer values should fail for monetary mode.
    """
    G = nx.DiGraph()
    G.add_node("Leaf", value=-500)
    with pytest.raises(ValueError, match="Invalid monetary value"):
        validate_values(G, "monetary")


def test_validate_values_invalid_probability():
    """
    Probability values outside [0,1] should raise error.
    """
    G = nx.DiGraph()
    G.add_node("Leaf", value=1.5)
    with pytest.raises(ValueError, match="Invalid probability"):
        validate_values(G, "probability")
