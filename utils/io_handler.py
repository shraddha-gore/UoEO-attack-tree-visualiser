"""
Handles input parsing for attack tree files in various supported formats.

This module is responsible for loading attack tree data from industry-standard formats
including JSON, YAML, and XML. It converts the raw input into a nested Python dictionary
structure that is compatible with the rest of the application's analysis and visualisation logic.

Functions:
- load_attack_tree(filepath): Detects file type and returns the parsed tree.
- _xml_to_dict(element): Converts XML elements recursively into dictionary format.

Supported Extensions:
- .json
- .yaml / .yml
- .xml
"""

import json
import xml.etree.ElementTree as ET
import yaml


def load_attack_tree(filepath):
    """
    Loads an attack tree from a file in JSON, YAML, or XML format.

    Parameters:
        filepath (str): Path to the input file.

    Returns:
        dict: Parsed tree structure in dictionary format.

    Raises:
        ValueError: If file extension is unsupported or data is invalid.
    """
    ext = filepath.lower().split('.')[-1]

    with open(filepath, 'r', encoding='utf-8') as file:
        if ext == 'json':
            return json.load(file)
        if ext in ['yaml', 'yml']:
            return yaml.safe_load(file)
        if ext == 'xml':
            tree = ET.parse(file)
            return _xml_to_dict(tree.getroot())

    raise ValueError("Unsupported file format. Please use JSON, YAML or XML.")


def _xml_to_dict(element):
    """
    Recursively converts an XML element into a dictionary format.

    Parameters:
        element (Element): Root XML node.

    Returns:
        dict: Node with optional children and value.
    """
    node = {"name": element.get("name")}
    value = element.get("value")
    if value:
        node["value"] = float(value)
    children = list(element)
    if children:
        node["children"] = [_xml_to_dict(child) for child in children]
    return node
