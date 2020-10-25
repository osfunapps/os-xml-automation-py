import os
import os_file_handler.file_handler as fh
import os_xml_handler.xml_handler as xh


def copy(xml_path, xml, place_holder_map):
    dirs_to_copy = xh.get_all_direct_child_nodes(xh.get_root_node(xml))
    for dir_node in dirs_to_copy:
        path_src = str(xh.get_node_att(dir_node, 'src'))
        path_dst = str(xh.get_node_att(dir_node, 'dst'))

        for key, value in place_holder_map.items():
            if key in path_src:
                path_src = path_src.replace(key, value)
            if key in path_dst:
                path_dst = path_dst.replace(key, value)

        path_src = fix_path(path_src, xml_path)
        path_dst = fix_path(path_dst, xml_path)

        if os.path.isfile(path_src):
            fh.copy_file(path_src, path_dst)
        elif os.path.isdir(path_src):
            fh.copy_dir(path_src, path_dst)


def fix_path(path_str, xml_path):
    # if that's a relative source
    if path_str.startswith('./'):
        return fix_path(os.path.join(fh.get_parent_path(xml_path), path_str[2:]), xml_path)

    else:
        parent_num = path_str.count('../')
        if parent_num > 0:
            parent_dir = fh.get_parent_path(xml_path)
            for i in range(0, parent_num):
                parent_dir = fh.get_parent_path(parent_dir)
            rest_of_path_idx = path_str.rindex('../') + 3
            rest_of_path = path_str[rest_of_path_idx:]
            return os.path.join(parent_dir, rest_of_path)
        else:
            return path_str
