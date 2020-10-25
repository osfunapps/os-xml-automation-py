import os_xml_handler.xml_handler as xh
from os_file_automation.xml_map import _shared_res as tools
import os_file_stream_handler.file_stream_handler as fsh


def manipulate(xml_path, xml, place_holder_map):
    nodes = xh.get_all_direct_child_nodes(xh.get_root_node(xml))
    for node in nodes:
        path_src = str(xh.get_node_att(node, 'src'))
        path_dst = str(xh.get_node_att(node, 'dst'))

        children_nodes = xh.get_all_direct_child_nodes(node)
        for child_node in children_nodes:
            if child_node.tag == 'original':
                old_text = str(xh.get_text_from_node(child_node))
            else:
                new_text = str(xh.get_text_from_node(child_node))
        # target_line = xh.get_node_att(node, 'line')
        action = xh.get_node_att(node, 'action')

        for key, value in place_holder_map.items():
            if key in path_src:
                path_src = path_src.replace(key, value)
            if key in path_dst:
                path_dst = path_dst.replace(key, value)

            if key in old_text:
                old_text = old_text.replace(key, value)

        path_src = tools.fix_path(path_src, xml_path)
        path_dst = tools.fix_path(path_dst, xml_path)

        if action == 'replace':
            fsh.replace_text_in_file(path_src, path_dst, old_text, new_text)
        elif action == 'above':
            fsh.append_text_above_line_in_file(path_src, path_dst, old_text, new_text)
        elif action == 'below':
            fsh.append_text_below_line_in_file(path_src, path_dst, old_text, new_text)
