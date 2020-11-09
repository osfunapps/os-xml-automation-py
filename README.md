Introduction
------------

this module contains automation tools for file handling

## Installation
Install via pip:

    pip install os-file-automation


## File copy automation:
   
Will copy directory/file by an absolute/relative/dynamic path defined by an xml file.

![An example of an xml file](/examples/file_mapper_xml_example.xml)

After your created the xml file, call it from code:
    
    import os_file_automation.xml_mapper.xml_mapper as xm
 
    xm.copy_files_by_xml(xml_path='path/to/xml', place_holder_map= {'$project_path': 'the/path/to/my/project/path'})
        

## Text automation

Will copy/append/replace/delete text defined by an xml map file.
     
![An example of an xml file](/examples/text_mapper_xml_example.xml)
     
NOTICE: It doesn't matter what the tag names of the file nodes (the direct children of the root). 
    
to use:
    
    import os_file_automation.xml_mapper.xml_mapper as xm
 
    xm.set_texts_by_xml(xml_path='path/to/xml',
                        place_holder_map= {'$project_path': 'the/path/to/my/project/path',
                                                                      $first_person_name': 'Johnny boy',
                                                                     '$second_person_name': 'Craig and Josh'})

## XCode project automation:
   
Will build an xcode project by a predefined xml file.

![xml example 1](/examples/xcode_mapper/xcode_mapper_xml_example.xml)

You can also extend an xml file to another one, to prevent repeating yourself:
- ![xml example 2](/examples/xcode_mapper/xcode_mapper_xml_example_2.xml)
- ![xml example 2 extension file](/examples/xcode_mapper/shared_mapper.xml)


After your created the xml file, call it from code:
    
    import os_file_automation.xml_mapper.xml_mapper as xm
 
    xm.set_xcode_project_by_xml('/path/to/your/xcode_mapper.xml',
                                place_holder_map = {'$app_path': '/path/to/a/dynamic/directory'})

        
           

And more...


## Links
[GitHub - osapps](https://github.com/osfunapps)

## Licence
ISC