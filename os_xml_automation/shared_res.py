import os_file_handler.file_handler as fh
from os_xml_handler import xml_handler as xh
from os_tools import tools as tools

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
NODE_PREFIX_2 = 'prefix'  # added cause users tend to do that wrong

NODE_SUFFIX = 'name_suffix'
NODE_SUFFIX_2 = 'suffix'  # added cause users tend to do that wrong

NODE_EXTENSION = 'extension'

# file node types
NODE_DIR_SRC = 'dir_src'
NODE_DIR_DST = 'dir_dst'

NODE_STEP = 'step'
NODE_ROOT_ATT_EXTENSION_MAPPER_PATH = 'extension_mapper_path'
