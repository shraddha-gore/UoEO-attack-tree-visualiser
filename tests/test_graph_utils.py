"""
Unit tests for graph utility functions in graph_utils.py.
"""

import pytest
import networkx as nx
from utils.graph_utils import build_graph, propagate_values, aggregate_impact


@pytest.fixture
def sample_prob_tree():
    return {
        "name": "Root",
        "children": [
            {"name": "Node A", "value": 0.6},
            {
                "name": "Node B",
                "children": [
                    {"name": "Node B1", "value": 0.7},
                    {"name": "Node B2", "value": 0.8}
                ]
            }
        ]
    }


@pytest.fixture
def sample_monetary_tree():
    return {
        "name": "Root",
        "children": [
            {"name": "Node A", "value": 1000},
            {
                "name": "Node B",
                "children": [
                    {"name": "Node B1", "value": 2000},
                    {"name": "Node B2", "value": 3000}
                ]
            }
        ]
    }


def test_build_graph():
    tree = {"name": "A", "children": [{"name": "B"}]}
    graph = build_graph(tree)
    assert isinstance(graph, nx.DiGraph)
    assert set(graph.nodes) == {"A", "B"}
    assert ("A", "B") in graph.edges


def test_propagate_probability_values(sample_prob_tree):
    graph = build_graph(sample_prob_tree)
    propagate_values(graph, "probability")
    expected_root_prob = 1 - (1 - 0.6) * (1 - (1 - (1 - 0.7) * (1 - 0.8)))
    assert round(graph.nodes["Root"]["value"], 6) == round(expected_root_prob, 6)


def test_propagate_monetary_values(sample_monetary_tree):
    graph = build_graph(sample_monetary_tree)
    propagate_values(graph, "monetary")
    assert graph.nodes["Root"]["value"] == 1000 + (2000 + 3000)


def test_aggregate_probability(sample_prob_tree):
    graph = build_graph(sample_prob_tree)
    propagate_values(graph, "probability")
    total = aggregate_impact(graph, "probability")
    assert 0.0 <= total <= 1.0


def test_aggregate_monetary(sample_monetary_tree):
    graph = build_graph(sample_monetary_tree)
    propagate_values(graph, "monetary")
    total = aggregate_impact(graph, "monetary")
    assert total == 1000 + 2000 + 3000
