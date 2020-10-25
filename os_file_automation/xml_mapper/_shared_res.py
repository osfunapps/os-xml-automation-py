import os
import os_file_handler.file_handler as fh


# will turn a relative path to abs
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
