import os_file_automation.xml_mapper.xml_mapper as xm
from os_file_handler import file_handler as fh

# xm.set_texts_by_xml('/Users/home/Programming/Python/projects/PrepeareGeneralRemoteiOS/src/ads/normalize/normal_ads_props.xml',
#                     {'$project_path': '/Users/home/Programming/iOS/Remotes/Projects/GeneralRemote/GeneralRemoteiOS'})

# ans = fh.search_file('/Users/home/Programming/Python/modules/general/os_tools', full_name='MANIFEST')

xm.copy_files_by_xml('/Users/home/Programming/Python/modules/general/tests/file_mapper_xml_example.xml', {'$project_path': '/Users/home/Programming/Python/modules/general/tests'})
# fh.copy_dir('/Users/home/Programming/Python/modules/general/dir1', '/Users/home/Programming/Python/modules/general/dir2/dir1', overwrite_content_if_exists=True)
