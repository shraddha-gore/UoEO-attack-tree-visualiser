"""
Unit tests for XML parsing in io_handler.py.
"""

from utils.io_handler import _xml_to_dict
import xml.etree.ElementTree as ET


def test_xml_to_dict_flat():
    xml_str = '<node name="Leaf" value="0.8" />'
    element = ET.fromstring(xml_str)
    result = _xml_to_dict(element)
    assert result["name"] == "Leaf"
    assert result["value"] == 0.8


def test_xml_to_dict_nested():
    xml_str = """
    <node name="Root">
        <node name="Child1" value="0.3"/>
        <node name="Child2">
            <node name="Grandchild" value="0.5"/>
        </node>
    </node>
    """
    element = ET.fromstring(xml_str)
    result = _xml_to_dict(element)
    assert result["name"] == "Root"
    assert len(result["children"]) == 2
    assert result["children"][1]["children"][0]["name"] == "Grandchild"
