import os_file_handler.file_handler as fh
from os_xml_handler import xml_handler as xh
from os_tools import tools as tools

import os_xml_automation.shared_res as res


######################################################################
# This class meant to provide support for other automation libraries #
######################################################################

# will return the path to a given file node (src or dst)
def get_file_node_path(xml_path,
                       place_holder_map,
                       file_node,
                       node_name,
                       previous_found_path=None,
                       file_search=True):
    file_node = xh.get_child_nodes(file_node, node_name)[0]
    file_type = xh.get_node_att(file_node, res.PATH_TYPE)

    if file_type == res.PATH_TYPE_AS_SRC:
        output_file_path = previous_found_path

    elif file_type == res.PATH_TYPE_SEARCH:
        output_file_path = find_search_path(place_holder_map, file_node, file_search)
    else:
        output_file_path = find_normal_path(place_holder_map, file_node)

    # fix paths if required
    return tools.rel_path_to_abs(output_file_path, xml_path)


# will return all of the files/directories which corresponds to the search in the node
def find_files_node_paths(xml_path,
                          place_holder_map,
                          file_node,
                          node_name,
                          file_search=True):
    file_node = xh.get_child_nodes(file_node, node_name)[0]

    file_paths = find_search_path(place_holder_map, file_node, file_search=file_search, allow_multiple_files=True)

    # fix paths if required
    for i in range(0, len(file_paths)):
        file_paths[i] = tools.rel_path_to_abs(file_paths[i], xml_path)
    return file_paths


# will return the normal of a file, after modified with the dictionary's place holders
def find_normal_path(place_holder_map, file_node):
    file_path = xh.get_text_from_child_node(file_node, res.NODE_PATH)
    for key, value in place_holder_map.items():
        file_path = file_path.replace(key, value)

    return file_path


# will find the path of the file based on the user search params (full name, prefix, suffix and extension)
def find_search_path(place_holder_map, file_node, file_search=True, allow_multiple_files=False):
    file_search_path = xh.get_text_from_child_node(file_node, res.NODE_SEARCH_PATH)
    for key, value in place_holder_map.items():
        file_search_path = file_search_path.replace(key, value)

    file_full_name = xh.get_text_from_child_node(file_node, res.NODE_FULL_NAME)
    file_prefix = xh.get_text_from_child_node(file_node, res.NODE_PREFIX)
    if not file_prefix:
        file_prefix = xh.get_text_from_child_node(file_node, res.NODE_PREFIX_2)
    file_suffix = xh.get_text_from_child_node(file_node, res.NODE_SUFFIX)
    if not file_suffix:
        file_suffix = xh.get_text_from_child_node(file_node, res.NODE_SUFFIX_2)
    file_extension = xh.get_text_from_child_node(file_node, res.NODE_EXTENSION)

    if file_full_name:
        for key, value in place_holder_map.items():
            file_full_name = file_full_name.replace(key, value)
    if file_prefix:
        for key, value in place_holder_map.items():
            file_prefix = file_prefix.replace(key, value)
    if file_suffix:
        for key, value in place_holder_map.items():
            file_suffix = file_suffix.replace(key, value)

    if file_full_name and file_search:
        full_name_has_extension = fh.get_extension_from_file(file_full_name)
        if not full_name_has_extension and not file_extension:
            print(f"ERROR:'{file_full_name}' doesn't have an extension!\nAdd the extension in the same line (<full_name>{file_full_name}.extension</full_name>) or via the <extension> tag.\n")
            file_extension = tools.ask_for_input(f"If you want to proceed, type the extension below:")

    if file_search:
        files_found = fh.search_file(file_search_path,
                                     full_name=file_full_name,
                                     prefix=file_prefix,
                                     suffix=file_suffix,
                                     by_extension=file_extension,
                                     recursive=True)
    else:
        files_found = fh.search_dir(file_search_path,
                                    full_name=file_full_name,
                                    prefix=file_prefix,
                                    suffix=file_suffix,
                                    recursive=True)
    file_idx = 0
    if not files_found:
        raise IOError(f"ERROR: couldn't find the file/directory with these props:\nFull Name: '{file_full_name}'\nPrefix: '{file_prefix}'\nSuffix: '{file_suffix}'\nextension: '{file_extension}'")

    if allow_multiple_files:
        return files_found

    if len(files_found) > 1:
        print()
        print(f"WARNING: there are {len(files_found)} files/directories which corresponds to the search path '{file_search_path}' with these props:\nFull Name: '{file_full_name}'\nPrefix: '{file_prefix}'\nSuffix: '{file_suffix}'\nextension: '{file_extension}'")
        print(f"**********************************************************************")
        counter = 1
        for file_found in files_found:
            print(f'{counter}) {file_found}')
            counter += 1
        print(f"**********************************************************************")
        print('Please type the number of file/directory to use')
        file_idx = int(tools.ask_for_input(''))

    file_path = files_found[file_idx - 1]
    return file_path


# will fill the node's text relative to it's place holders
def fill_place_holders(text, place_holder_map):
    for key, value in place_holder_map.items():
        text = text.replace(key, value)
    return text


# will add all of the nodes from the extension file to the xml
def add_extension_nodes(xml_path, place_holder_map, root_node, xml):
    extension_mapper_path = xh.get_node_att(root_node, res.NODE_ROOT_ATT_EXTENSION_MAPPER_PATH)
    if extension_mapper_path:
        extension_mapper_path = tools.rel_path_to_abs(extension_mapper_path, xml_path)
        extension_mapper_path = fill_place_holders(extension_mapper_path, place_holder_map)
        extension_xml = xh.read_xml_file(extension_mapper_path)
        return xh.merge_xml1_with_xml2(extension_xml, xml)
    else:
        return xml
