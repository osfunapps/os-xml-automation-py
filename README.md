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
           

And more...


## Links
[GitHub - osapps](https://github.com/osfunapps)

## Licence
ISC