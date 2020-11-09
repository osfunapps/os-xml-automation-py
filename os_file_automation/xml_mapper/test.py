from os_file_automation.xml_mapper import xml_mapper as xm

xm.set_xcode_project_by_xml('/Users/home/Google Drive/Remotes/iOS/apps/lg/automation/xcode_mapper.xml',
                            place_holder_map={'$app_path': '/Users/home/Google Drive/Remotes/iOS/apps/lg',
                                              '$shared_mapper_path': '/Users/home/Programming/Python/projects/PrepeareGeneralRemoteiOS/res/shared_xcode_mapper.xml'})
