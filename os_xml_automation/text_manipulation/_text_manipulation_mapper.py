import os_xml_handler.xml_handler as xh

from os_xml_automation import shared_res as shared_res
from os_xml_automation import shared_tools as shared_tools
from os_xml_automation.text_manipulation import _res as res


# manipulate the files by the text mapper
def manipulate(xml_path, xml, place_holder_map):
    file_nodes = xh.get_all_direct_child_nodes(xh.get_root_node(xml))

    # run on all of the root's direction children
    for file_node in file_nodes:

        # get the <file_src> and <file_dst> nodes paths
        src_file_path = shared_tools.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_FILE_SRC)
        dst_file_path = shared_tools.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_FILE_DST, src_file_path)

        texts_node = xh.get_child_nodes(file_node, res.NODE_TEXTS)[0]
        text_nodes = xh.get_child_nodes(texts_node, res.NODE_TEXT)

        for text_node in text_nodes:
            init_text_node_cycle(text_node, place_holder_map, src_file_path, dst_file_path)


# will do a specific text node
def init_text_node_cycle(text_node, place_holder_map, src_file_path, dst_file_path):

    # get the current action and text
    action = str(xh.get_node_att(text_node, shared_res.ACTION))
    original_text = xh.get_text_from_child_node(text_node, shared_res.NODE_ORIGINAL_TEXT)
    cancel_if_already_present = False
    new_text = ''

    # delete range and set in range are special. They will need a special way to be dealt with
    if action == res.NODE_TEXT_ATT_ACTION_VAL_DELETE_RANGE or action == res.NODE_TEXT_ATT_ACTION_VAL_REPLACE_IN_RANGE:
        handle_delete_range(text_node, place_holder_map, src_file_path, dst_file_path)
        if action == res.NODE_TEXT_ATT_ACTION_VAL_DELETE_RANGE:
            return
        else:
            # set in range will change the action to above line and set the required text above the bottom boundary
            action = res.NODE_TEXT_ATT_ACTION_VAL_ABOVE
            original_text = xh.get_text_from_child_node(text_node, res.NODE_TO_TEXT)
            original_text = shared_tools.fill_place_holders(original_text, place_holder_map)

    if action != res.NODE_TEXT_ATT_ACTION_VAL_DELETE_LINE:
        new_text_node = xh.get_child_nodes(text_node, shared_res.NODE_NEW_TEXT)[0]
        new_text = xh.get_text_from_node(new_text_node)
        cancel_if_already_present = xh.get_node_att(new_text_node, res.NODE_TEXT_ATT_IF_ALREADY_PRESENT) == res.NODE_TEXT_ATT_IF_ALREADY_PRESENT_VAL_CANCEL

    # replace place holders
    for key, value in place_holder_map.items():
        if key in original_text:
            original_text = original_text.replace(key, value)
        if new_text and key in new_text:
            new_text = new_text.replace(key, value)

    from os_file_stream_handler import file_stream_handler as fsh
    if action == res.NODE_TEXT_ATT_ACTION_VAL_DELETE_LINE:
        fsh.delete_line_in_file(src_file_path, dst_file_path, original_text)
    elif action == res.NODE_TEXT_ATT_ACTION_VAL_REPLACE or action == res.NODE_TEXT_ATT_ACTION_VAL_REPLACE_LINE:
        fsh.replace_text_in_file(src_file_path, dst_file_path, original_text, new_text if new_text else '', action == res.NODE_TEXT_ATT_ACTION_VAL_REPLACE_LINE, cancel_if_already_present)
    elif action == res.NODE_TEXT_ATT_ACTION_VAL_ABOVE:
        fsh.append_text_above_line_in_file(src_file_path, dst_file_path, original_text, new_text, cancel_if_already_present)
    elif action == res.NODE_TEXT_ATT_ACTION_VAL_BELOW:
        fsh.append_text_below_line_in_file(src_file_path, dst_file_path, original_text, new_text, cancel_if_already_present)


# will delete a text in range
def handle_delete_range(text_node, place_holder_map, src_file_path, dst_file_path):
    from_text = xh.get_text_from_child_node(text_node, res.NODE_FROM_TEXT)
    to_text = xh.get_text_from_child_node(text_node, res.NODE_TO_TEXT)
    from_text = shared_tools.fill_place_holders(from_text, place_holder_map)
    to_text = shared_tools.fill_place_holders(to_text, place_holder_map)
    include_boundaries = xh.get_node_att(text_node, res.NODE_TEXT_ATT_INCLUDE_BOUNDARIES)
    include_boundaries = not include_boundaries or include_boundaries == 'false'
    from os_file_stream_handler import file_stream_handler as fsh
    fsh.delete_text_range_in_file(src_file_path, dst_file_path, from_text, to_text, include_bundaries=include_boundaries)
