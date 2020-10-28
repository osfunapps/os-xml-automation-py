Introduction
------------

this module contains automation tools for file handling 

## Installation
Install via pip:

    pip install os-file-automation


## Usage       
        
    import os_file_automation as file_automation
    

## File automation:
    
    '''
    Will copy files/directories defined by an xml map file.
     
    an example of an xml file could be:
     
     <files>
     
        <!-- copy an absolute path -->
        <element src="/Users/home/Google Drive/my_text_file.txt" dst="/Users/home/Google Drive/new_dir/my_text_file.txt">
     
        <!-- copy to a patch with a place holders that their definitions is defined in code-->
        <element src="$dynamic_src/src_dir" dst="$dynamic_dst/dst_dir">
     
        <!-- copy to a relative parent path -->
        <element src="../../Google Drive/shared_podfile" dst="../new_dir/shared_podfile"/>
        
        <!-- copy to the same directory parent path -->
        <element src="./my_file.txt" dst="./new_dir/my_file_with_different_name.txt"/>
    </files>
    
    NOTICE: It doesn't matter what the tag names of any of the xml tree tags as long as the attribute 'src' and 'dst' is satisfied for each sub node of the root.
    
    param xml_path: the path to your XML file
    place_holder_map: a map holding the place holders that appear in the xml file, with their respective definitions. 
    The map could be like {'$dynamic_src': '/Users/home/my_dyn_src',
                           '$dynamic_dst': '/Users/home/my_dyn_dst'}
    }
    '''
    
    
    def copy_files_by_xml(xml_path, place_holder_map=None):
        if place_holder_map is None:
            place_holder_map = {}
        xml = xh.read_xml_file(xml_path)
        file_manipulator.manipulate(xml_path, xml, place_holder_map)
    
    
    '''
## Text automation

Will copy/append/replace/delete text defined by an xml map file.
     
an example of an xml file could be:
     
```xml
<root>

    <!-- example 1 -->
    <!-- the tag name of the files can be whatever you want -->
    <app_view_controller>

        <!-- set the source file to read -->
        <file_src>
            <path>abs/path/to/ViewController.swift</path>
            <!-- or relative path:
            <path>../../relative/path/to/ViewController.swift</path>
            -->
        </file_src>

        <!-- set the destination file to write -->
        <file_dst>
            <path>./ViewController(modified).swift</path>
        </file_dst>

        <!-- set the texts to change -->
        <texts>

            <!-- the text action can be either replace/replace_line/delete line/above_line/below_line -->
            <text action="replace_line">
                <original_text>// this is some old school code I wrote in my ViewController.swift file</original_text>
                <new_text>// the new, cooler and more sophisticated code 🤖</new_text>
            </text>


            <!-- add the if_already_present attribute and value to prevent duplications if the line already exists -->
            <text action="replace">
                <original_text>.testBannerAdId</original_text>
                <new_text if_already_present="cancel">realBannerAdId</new_text>
            </text>
        </texts>
    </app_view_controller>


    <!-- example 2 -->
    <!-- the tag name of the files can be whatever you want -->
    <faces_file>

        <!-- set path_type as "search" to look for the file in a given path -->
        <file_src path_type="search">
            <search_path>../search_path</search_path>
            <full_name>faces_file.java</full_name>
            <!-- other search tags could be:
            <name_prefix>my_fi</name_prefix>
            <name_suffix>_file</name_suffix>
            <extension>.java</extension>
            -->
        </file_src>

        <!-- set path_type as "as_src" to overwrite the source file. in this example, my_file.java -->
        <file_dst path_type="as_src" />
        <texts>
            <text action="delete_line">
                <original_text>this is a sad face: 😥</original_text>
            </text>
            <text action="replace_line">
                <original_text>this is a spooked face: 😱</original_text>
            </text>
            <text action="above_line">
                <original_text>this is a funny face: 👾</original_text>
            </text>
        </texts>
    </faces_file>


    <!-- example 3 -->
    <!-- the tag name of the files can be whatever you want -->
    <people_file>
        <file_src path_type="search">

            <!-- this example shows the use of place holders. The place holders values could be defined via code and replace the place holders in the xml, during runtime.
            in this example $project_path could be defined during runtime to be whatever path you want (even relative) -->
            <search_path>$project_path</search_path>
            <full_name>people_names.swift</full_name>
        </file_src>
        <file_dst path_type="as_src" />
        <texts>
            <text action="replace">
                <!-- place holders can be used wherever you want. Event in the text you look for! -->
                <original_text>$first_person_name the tool 😼</original_text>
                <new_text>Johnny Knoxville</new_text>
            </text>
            <text action="below_line">
                <original_text>$second_person_name</original_text>
                <new_text>Osama bin gladden 👳 is now below $second_person_name</new_text>
            </text>
        </texts>
    </people_file>

</root>
```
    
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