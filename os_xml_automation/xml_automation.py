import os_xml_handler.xml_handler as xh

from os_xml_automation.file_manipulation import _file_manipulation_mapper as file_manipulator
from os_xml_automation.text_manipulation import _text_manipulation_mapper as text_manipulator


def manipulate_files_by_xml(xml_path, place_holder_map=None):
    """
    Will copy/delete files/directories defined by an xml map file.

    param xml_path: the path to your XML file
    place_holder_map: a map holding the place holders that appear in the xml file, with their respective definitions.
    The map could be like {'$dynamic_src': '/Users/home/my_dyn_src',
                       '$dynamic_dst': '/Users/home/my_dyn_dst'}
    """
    if place_holder_map is None:
        place_holder_map = {}
    xml = xh.read_xml_file(xml_path)
    file_manipulator.manipulate(xml_path, xml, place_holder_map)


def set_texts_by_xml(xml_path, place_holder_map=None):
    """
    Will copy/append text defined by an xml map file.

    NOTICE: It doesn't matter what the tag names of root/the text nodes or the new line.
    Just make sure you have the 'original' tags where they should be and that the attribute 'src' and 'dst' is satisfied for each sub node of the root.

    param xml_path: the path to your XML file
    place_holder_map: a map holding the place holders that appear in the xml file, with their respective definitions.
    The map could be like {'$dynamic_src': '/Users/home/my_dyn_src',
                       '$dynamic_dst': '/Users/home/my_dyn_dst'}
    """
    if place_holder_map is None:
        place_holder_map = {}
    xml = xh.read_xml_file(xml_path)

    text_manipulator.manipulate(xml_path, xml, place_holder_map)

