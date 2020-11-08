import os_xml_handler.xml_handler as xh
from os_file_automation.xml_mapper import _shared_res as shared_res
import os_file_handler.file_handler as fh
import os


# manipulate the files by the text mapper
def manipulate(xml_path, xml, place_holder_map):
    file_nodes = xh.get_all_direct_child_nodes(xh.get_root_node(xml))

    # run on all of the root's direct children
    for file_node in file_nodes:

        # get the <file_src> or the <dir_src>
        if xh.get_child_nodes(file_node, shared_res.NODE_DIR_SRC):
            src_path = shared_res.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_DIR_SRC, file_search=False)
        else:
            src_path = shared_res.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_FILE_SRC, file_search=True)

        # get the <file_dst> or the <dir_dst>
        if xh.get_child_nodes(file_node, shared_res.NODE_DIR_DST):
            dst_path = shared_res.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_DIR_DST, file_search=False)
        else:
            dst_path = shared_res.get_file_node_path(xml_path, place_holder_map, file_node, shared_res.NODE_FILE_DST, src_path, file_search=True)

        # start the copy process
        if os.path.isfile(src_path):
            fh.copy_file(src_path, dst_path, create_path_if_needed=True, overwrite_if_needed=True)

        elif os.path.isdir(src_path):
            fh.copy_dir(src_path, dst_path, overwrite_content_if_exists=True)
