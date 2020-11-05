import os_xml_handler.xml_handler as xh
from os_file_stream_handler import file_stream_handler as fsh

from os_file_automation.xml_mapper import _shared_res as shared_res
from os_file_automation.xml_mapper.text_manipulation import _text_manipulation_bank as finals


# manipulate the files by the text mapper
def manipulate(xml_path, xml, place_holder_map):
    file_nodes = xh.get_all_direct_child_nodes(xh.get_root_node(xml))

    # run on all of the root's direction children
    for file_node in file_nodes:

        # get the <file_src> and <file_dst> nodes paths
        src_file_path = shared_res.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_FILE_SRC)
        dst_file_path = shared_res.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_FILE_DST, src_file_path)

        texts_node = xh.get_child_nodes(file_node, finals.NODE_TEXTS)[0]
        text_nodes = xh.get_child_nodes(texts_node, finals.NODE_TEXT)

        for text_node in text_nodes:
            init_text_node_cycle(text_node, place_holder_map, src_file_path, dst_file_path)


# will do a specific text node
def init_text_node_cycle(text_node, place_holder_map, src_file_path, dst_file_path):
    # get the current action and text
    action = str(xh.get_node_att(text_node, shared_res.ACTION))
    original_text = xh.get_text_from_child_node(text_node, shared_res.NODE_ORIGINAL_TEXT)
    cancel_if_already_present = False
    new_text = ''

    # if no delete line
    if action != finals.NODE_TEXT_ATT_ACTION_VAL_DELETE_LINE:
        new_text_node = xh.get_child_nodes(text_node, shared_res.NODE_NEW_TEXT)[0]
        new_text = xh.get_text_from_node(new_text_node)
        cancel_if_already_present = xh.get_node_att(new_text_node, finals.NODE_TEXT_ATT_IF_ALREADY_PRESENT) == finals.NODE_TEXT_ATT_IF_ALREADY_PRESENT_VAL_CANCEL

    # replace place holders
    for key, value in place_holder_map.items():
        if key in original_text:
            original_text = original_text.replace(key, value)
        if new_text and key in new_text:
            new_text = new_text.replace(key, value)

    if action == finals.NODE_TEXT_ATT_ACTION_VAL_DELETE_LINE:
        fsh.delete_line_in_file(src_file_path, dst_file_path, original_text)
    elif action == finals.NODE_TEXT_ATT_ACTION_VAL_REPLACE or action == finals.NODE_TEXT_ATT_ACTION_VAL_REPLACE_LINE:
        fsh.replace_text_in_file(src_file_path, dst_file_path, original_text, new_text if new_text else '', action == finals.NODE_TEXT_ATT_ACTION_VAL_REPLACE_LINE, cancel_if_already_present)
    elif action == finals.NODE_TEXT_ATT_ACTION_VAL_ABOVE:
        fsh.append_text_above_line_in_file(src_file_path, dst_file_path, original_text, new_text, cancel_if_already_present)
    elif action == finals.NODE_TEXT_ATT_ACTION_VAL_BELOW:
        fsh.append_text_below_line_in_file(src_file_path, dst_file_path, original_text, new_text, cancel_if_already_present)
