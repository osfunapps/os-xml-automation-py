Introduction
------------

This module contains automation tools for files and text handling

## Installation
Install via pip:

    pip install os-xml-automation

## File handling automation:
   
Just create a xml file with all the actions you want to do (copy/delete a directory/file by an absolute/relative/dynamic path)

- [xml example](/examples/file_mapper/example.xml):

```xml
<root>

     <!--example 1 -->
     <!--the tag name of the files/dirs can be whatever you want -->
    <dir_copy_1 action="copy">

        <dir_src>
            <path >./same_dir_file.txt</path>
        </dir_src>

        <dir_dst>
            <path>../copied_file.txt</path>
        </dir_dst>

    </dir_copy_1>


    <!-- example 2 -->
    <!-- the tag name of the files/dirs can be whatever you want -->
    <dir_copy_2 action="copy">

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
    <file_copy_1 action="copy">

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
    <file_copy_2 action="copy">

        <!-- set path_type as "search" to look for the file in a given path -->
        <file_src>
            <path>path/to/my/file.txt</path>
        </file_src>

        <file_dst>
            <path>path/to/my/file_2.txt</path>
        </file_dst>
    </file_copy_2>


    <!-- delete file example -->    
    <file_delete_1 action="delete">

        <!-- set path_type as "search" to look for the file in a given path -->
        <file_src path_type="search">
            <!-- here we will use a place holder defined when you'll call the function-->
            <search_path>/Users/home/Desktop/bv/temp</search_path>
            <prefix>toc</prefix>
        </file_src>
    </file_delete_1>


</root>
```
After your created the xml file, call it from code:
    
    from os_xml_automation import xml_automation as xm
    xm.manipulate_files_by_xml(xml_path='path/to/xml', place_holder_map= {'$project_path': 'the/path/to/my/project/path'})

## Text automation

Will copy/append/replace/delete text defined by a xml map file.

- [xml example](/examples/text_mapper/example.xml):
```xml
<root>


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
                <new_text>this line will be instead of the spooky face</new_text>
            </text>
            <text action="above_line">
                <original_text>this is a funny face: 👾</original_text>
                <new_text>this line will be above the funny face</new_text>
            </text>

            <!-- delete_range will remove text between boundaries -->
            <text action="delete_range" include_boundaries="true">
                <original_text>range delete start</original_text>
                <new_text>range delete end</new_text>
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
                <original_text>$first_person_name</original_text>
                <new_text>Johnny the tool 😼</new_text>
            </text>
            <text action="below_line">
                <original_text>craig the $craig_last_name</original_text>
                <new_text>Osama bin gladden 👳 is below craig $craig_last_name</new_text>
            </text>
        </texts>
    </people_file>

</root>
```
NOTICE: It doesn't matter what the tag names of the file nodes (the direct children of the root). 
    
To use:
    
    from os_xml_automation import xml_automation as xm
 
    xm.set_texts_by_xml(xml_path='path/to/xml',
                        place_holder_map= {'$project_path': 'the/path/to/my/project/path',
                                                                      $first_person_name': 'Johnny boy',
                                                                     '$second_person_name': 'Craig and Josh'})

And more...


## Links
[GitHub - osapps](https://github.com/osfunapps)

## Licence
ISC