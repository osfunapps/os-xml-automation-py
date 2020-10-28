import os_xml_handler.xml_handler as xh
from os_file_automation.xml_mapper import _shared_res as shared_res
import os_file_handler.file_handler as fh
from os_tools import tools as tools
from os_file_stream_handler import file_stream_handler as fsh
from os_file_automation.xml_mapper.text_manipulation import _text_manipulation_bank as finals


# manipulate the files by the text mapper
def manipulate(xml_path, xml, place_holder_map):
    file_nodes = xh.get_all_direct_child_nodes(xh.get_root_node(xml))

    # run on all of the root's direction children
    for file_node in file_nodes:

        # get the <file_src> and <file_dst> nodes paths
        src_file_path = get_file_node_path(place_holder_map, file_node, shared_res.NODE_FILE_SRC)
        dst_file_path = get_file_node_path(place_holder_map, file_node, shared_res.NODE_FILE_DST, src_file_path)

        texts_node = xh.get_child_nodes(file_node, finals.NODE_TEXTS)[0]
        text_nodes = xh.get_child_nodes(texts_node, finals.NODE_TEXT)

        for text_node in text_nodes:
            init_text_node_cycle(text_node, place_holder_map, src_file_path, dst_file_path, xml_path)


# will do a specific text node
def init_text_node_cycle(text_node, place_holder_map, src_file_path, dst_file_path, xml_path):
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

    # fix paths if required
    src_file_path = shared_res.fix_path(src_file_path, xml_path)
    dst_file_path = shared_res.fix_path(dst_file_path, xml_path)

    if action == finals.NODE_TEXT_ATT_ACTION_VAL_DELETE_LINE:
        fsh.delete_line_in_file(src_file_path, dst_file_path, original_text)
    elif action == finals.NODE_TEXT_ATT_ACTION_VAL_REPLACE or action == finals.NODE_TEXT_ATT_ACTION_VAL_REPLACE_LINE:
        fsh.replace_text_in_file(src_file_path, dst_file_path, original_text, new_text if new_text else '', action == finals.NODE_TEXT_ATT_ACTION_VAL_REPLACE_LINE, cancel_if_already_present)
    elif action == finals.NODE_TEXT_ATT_ACTION_VAL_ABOVE:
        fsh.append_text_above_line_in_file(src_file_path, dst_file_path, original_text, new_text, cancel_if_already_present)
    elif action == finals.NODE_TEXT_ATT_ACTION_VAL_BELOW:
        fsh.append_text_below_line_in_file(src_file_path, dst_file_path, original_text, new_text, cancel_if_already_present)


# will return the path to a given file node (src or dst)
def get_file_node_path(place_holder_map, text_node, node_name, previous_found_path=None):
    file_node = xh.get_child_nodes(text_node, node_name)[0]
    file_type = xh.get_node_att(file_node, shared_res.PATH_TYPE)

    if file_type == shared_res.PATH_TYPE_AS_SRC:
        return previous_found_path
    elif file_type == shared_res.PATH_TYPE_SEARCH:
        return find_search_path(place_holder_map, file_node)
    return find_normal_path(place_holder_map, file_node)


# will return the normal of a file, after modified with the dictionary's place holders
def find_normal_path(place_holder_map, file_node):
    file_path = xh.get_text_from_child_node(file_node, shared_res.NODE_PATH)
    for key, value in place_holder_map.items():
        file_path = file_path.replace(key, value)

    return file_path


# will find the path of the file based on the user search params (full name, prefix, suffix and extension)
def find_search_path(place_holder_map, file_node):
    file_search_path = xh.get_text_from_child_node(file_node, shared_res.NODE_SEARCH_PATH)
    for key, value in place_holder_map.items():
        file_search_path = file_search_path.replace(key, value)

    file_full_name = xh.get_text_from_child_node(file_node, shared_res.NODE_FULL_NAME)
    file_prefix = xh.get_text_from_child_node(file_node, shared_res.NODE_PREFIX)
    file_suffix = xh.get_text_from_child_node(file_node, shared_res.NODE_SUFFIX)
    file_extension = xh.get_text_from_child_node(file_node, shared_res.NODE_EXTENSION)

    if file_full_name:
        for key, value in place_holder_map.items():
            file_full_name = file_full_name.replace(key, value)
    if file_prefix:
        for key, value in place_holder_map.items():
            file_prefix = file_prefix.replace(key, value)
    if file_suffix:
        for key, value in place_holder_map.items():
            file_suffix = file_suffix.replace(key, value)

    if file_full_name:
        full_name_has_extension = fh.get_extension_from_file(file_full_name)
        if not full_name_has_extension and not file_extension:
            raise IOError(f"ERROR:'{file_full_name}' doesn't have an extension! add the extension in the same line ({file_full_name}.extension) or via the <extension> tag")

    files_found = fh.search_files(file_search_path,
                                  full_name=file_full_name,
                                  prefix=file_prefix,
                                  suffix=file_suffix,
                                  by_extension=file_extension)
    file_idx = 0
    if not files_found:
        raise IOError(f"ERROR: couldn't find the file with these props:\nFull Name: '{file_full_name}'\nPrefix: '{file_prefix}'\nSuffix: '{file_suffix}'\nextension: '{file_extension}'")
    if len(files_found) > 1:
        print()
        print(f"WARNING: there are {len(files_found)} files which corresponds to the search path '{file_search_path}' with these props:\nFull Name: '{file_full_name}'\nPrefix: '{file_prefix}'\nSuffix: '{file_suffix}'\nextension: '{file_extension}'")
        print(f"**********************************************************************")
        counter = 1
        for file_found in files_found:
            print(f'{counter}) {file_found}')
            counter += 1
        print(f"**********************************************************************")
        print('Please type the number of file to use')
        file_idx = int(tools.ask_for_input(''))

    file_path = files_found[file_idx - 1]
    return file_path
