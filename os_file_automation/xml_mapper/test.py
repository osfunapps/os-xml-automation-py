from os_file_automation.xml_mapper import xml_mapper as xm
#
# # xm.set_xcode_project_by_xml('/Users/home/Google Drive/Remotes/iOS/apps/lg/automation/xcode_mapper.xml',
# #                             place_holder_map={'$app_path': '/Users/home/Google Drive/Remotes/iOS/apps/lg',
# #                                               '$shared_mapper_path': '/Users/home/Programming/Python/projects/PrepeareGeneralRemoteiOS/res/shared_xcode_mapper.xml'})
#
# # xm.set_xcode_project_by_xml('/Users/home/Programming/Python/modules/general/os_file_automation/examples/xcode_mapper/test/xcode_mapper.xml',
# #                             {
# #                                 '$project_path': '/Users/home/Programming/iOS/Remotes/Projects/GeneralRemote/GeneralRemoteiOS'
# #                             })
#
# xm.set_texts_by_xml('/Users/home/Google Drive/Remotes/iOS/apps/fire/automation/text_mapper.xml',
#                     {'$project_path': '/Users/home/Programming/iOS/Remotes/Projects/GeneralRemote/GeneralRemoteiOS'})

xm.manipulate_files_by_xml("/Users/home/Programming/Python/modules/general/os_file_automation/examples/file_mapper/file_mapper_xml_example_2.xml")
