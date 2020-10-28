import os
import os_file_handler.file_handler as fh


ACTION = 'action'
PATH_TYPE = 'path_type'
PATH_TYPE_SEARCH = 'search'
PATH_TYPE_AS_SRC = 'as_src'

# root children
NODE_FILE_SRC = 'file_src'
NODE_FILE_DST = 'file_dst'
NODE_ORIGINAL_TEXT = 'original_text'
NODE_NEW_TEXT = 'new_text'

# file node children
NODE_PATH = 'path'
NODE_SEARCH_PATH = 'search_path'
NODE_FULL_NAME = 'full_name'
NODE_PREFIX = 'name_prefix'
NODE_SUFFIX = 'name_suffix'
NODE_EXTENSION = 'extension'


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
