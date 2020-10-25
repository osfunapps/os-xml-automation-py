Introduction
------------

this module contains automation tools for file handling 

## Installation
Install via pip:

    pip install os-file-automation


## Usage       
        
    import os_file_automation as file_automation
    

## Functions and signatures:
    
    
    '''
    Will copy files by an xml map file.
     
    an example of an xml file could be:
     
     <files>
        <!-- copy an absolute path -->
        <element src="/Users/home/Google Drive/shared_podfile" dst="/Users/home/Google Drive/new_dir/shared_podfile"/>
        
        <!-- copy to a relative parent path -->
        <element src="../../Google Drive/shared_podfile" dst="../new_dir/shared_podfile"/>
        
        <!-- copy to the same directory parent path -->
        <element src="./my_file.txt" dst="./new_dir/my_file_with_different_name.txt"/>
    </files>
    
    NOTICE: It doesn't matter what the tag names of any of the xml tree tags as long as the attribute 'src' and 'dst' is satisfied for each sub node of the root
    
    '''
    
    
    def copy_files_by_xml(xml_path, place_holder_map=None):
        if place_holder_map is None:
            place_holder_map = {}
        xml = xh.read_xml_file(xml_path)
        bp.copy(xml_path, xml, place_holder_map)


And more...


## Links
[GitHub - osapps](https://github.com/osfunapps)

## Licence
ISC