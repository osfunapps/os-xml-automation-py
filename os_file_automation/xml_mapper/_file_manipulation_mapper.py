import os
import os_file_handler.file_handler as fh
import os_xml_handler.xml_handler as xh
from os_file_automation.xml_mapper import _shared_res as tools


def manipulate(xml_path, xml, place_holder_map):
    nodes = xh.get_all_direct_child_nodes(xh.get_root_node(xml))
    for node in nodes:
        path_src = str(xh.get_node_att(node, 'src'))
        path_dst = str(xh.get_node_att(node, 'dst'))

        for key, value in place_holder_map.items():
            if key in path_src:
                path_src = path_src.replace(key, value)
            if key in path_dst:
                path_dst = path_dst.replace(key, value)

        path_src = tools.fix_path(path_src, xml_path)
        path_dst = tools.fix_path(path_dst, xml_path)

        if os.path.isfile(path_src):
            fh.copy_file(path_src, path_dst)
        elif os.path.isdir(path_src):
            fh.copy_dir(path_src, path_dst)
