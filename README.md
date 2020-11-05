Introduction
------------

this module contains automation tools for file handling

## Installation
Install via pip:

    pip install os-file-automation


## File automation:
   
Will copy directory/file by an absolute/relative/dynamic path defined by an xml file.

The xml could be defined like so:

```xml
<root>
    
     <!--example 1 -->
     <!--the tag name of the files/dirs can be whatever you want -->
    <dir_copy_1>
    
        <dir_src>
            <path >./same_dir_file.txt</path>
        </dir_src>
    
        <dir_dst>
            <path>../copied_file.txt</path>
        </dir_dst>
    
    </dir_copy_1>
    
    
    <!-- example 2 -->
    <!-- the tag name of the files/dirs can be whatever you want -->
    <dir_copy_2>
    
        <!-- set path_type as "search" to look for the dir in a given path -->
        <dir_src path_type="search">
            <search_path>/a/path/to/search/for/the/dir</search_path>
            <full_name>my_dir_name</full_name>
        </dir_src>
    
        <dir_dst>
            <path>../my_dir_name_copy</path>
        </dir_dst>
    </dir_copy_2>
    
    
    <!-- example 3 -->
    <!-- the tag name of the files/dirs can be whatever you want -->
    <file_copy_1>
    
        <!-- set path_type as "search" to look for the file in a given path -->
        <file_src path_type="search">
    
    
            <!-- here we will use a place holder defined when you'll call the function-->
            <search_path>$a_path_defined_in_code</search_path>
            <name_prefix>myf</name_prefix>
            <!--<name_suffix>ile</name_suffix>-->
            <extension>.txt</extension>
        </file_src>
    
        <file_dst>
            <path>../copied_file.txt</path>
        </file_dst>
    </file_copy_1>
    
    <!-- example 4 -->
    <!-- the tag name of the files/dirs can be whatever you want -->
    <file_copy_2>
    
        <!-- set path_type as "search" to look for the file in a given path -->
        <file_src>
            <path>path/to/my/file.txt</path>
        </file_src>
    
        <file_dst>
            <path>path/to/my/file_2.txt</path>
        </file_dst>
    </file_copy_2>
    
</root>
```

After your created the xml file, call it from code:
    
    import os_file_automation.xml_mapper.xml_mapper as xm
 
    xm.copy_files_by_xml(xml_path='path/to/xml', place_holder_map= {'$project_path': 'the/path/to/my/project/path'})
        

## Text automation

Will copy/append/replace/delete text defined by an xml map file.
     
An example of an xml file could be:
     
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