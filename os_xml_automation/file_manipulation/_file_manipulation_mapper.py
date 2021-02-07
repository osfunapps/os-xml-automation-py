import os_xml_handler.xml_handler as xh
from os_xml_automation import shared_res as shared_res
from os_xml_automation import shared_tools as shared_tools
from os_xml_automation.file_manipulation import _res as res
import os_file_handler.file_handler as fh
import os


# manipulate the files by the text mapper
def manipulate(xml_path, xml, place_holder_map):
    file_nodes = xh.get_all_direct_child_nodes(xh.get_root_node(xml))

    # run on all of the root's direct children
    for file_node in file_nodes:

        # get the action
        action = xh.get_node_att(file_node, shared_res.ACTION)

        # if copy, do copy
        if action == res.NODE_FILE_ATT_ACTION_VAL_COPY:
            src_path = get_file_or_dir_src_path(xml_path, place_holder_map, file_node)
            dst_path = get_dst_path(xml_path, place_holder_map, file_node, src_path)
            copy_file_or_dir(src_path, dst_path)

        # if delete, do delete
        elif action == res.NODE_FILE_ATT_ACTION_VAL_DELETE:
            to_delete_files = get_files_or_dirs_src_paths(xml_path, place_holder_map, file_node)
            delete_files_or_dirs(to_delete_files)


def delete_files_or_dirs(to_delete_files):
    for file in to_delete_files:
        if os.path.isfile(file):
            fh.remove_file(file)
        if os.path.isdir(file):
            fh.remove_dir(file)


def get_file_or_dir_src_path(xml_path, place_holder_map, file_node):
    if xh.get_child_nodes(file_node, shared_res.NODE_DIR_SRC):
        return shared_tools.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_DIR_SRC, file_search=False)
    else:
        return shared_tools.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_FILE_SRC, file_search=True)


def get_files_or_dirs_src_paths(xml_path, place_holder_map, file_node):
    if xh.get_child_nodes(file_node, shared_res.NODE_DIR_SRC):
        return shared_tools.find_files_node_paths(xml_path, place_holder_map, file_node, shared_res.NODE_DIR_SRC, file_search=False)
    else:
        return shared_tools.find_files_node_paths(xml_path, place_holder_map, file_node, shared_res.NODE_FILE_SRC, file_search=True)


def get_dst_path(xml_path, place_holder_map, file_node, src_path):
    # get the <file_dst> or the <dir_dst>
    if xh.get_child_nodes(file_node, shared_res.NODE_DIR_DST):
        return shared_tools.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_DIR_DST, file_search=False)
    else:
        return shared_tools.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_FILE_DST, src_path, file_search=True)


def copy_file_or_dir(src_path, dst_path):
    # start the delete process
    if os.path.isfile(src_path):
        fh.copy_file(src_path, dst_path, create_path_if_needed=True, overwrite_if_needed=True)
    elif os.path.isdir(src_path):
        fh.copy_dir(src_path, dst_path)
