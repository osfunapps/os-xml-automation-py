import os_xml_handler.xml_handler as xh

from os_file_automation import bp

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
    bp.copy(xml_path, xml, place_holder_map)
