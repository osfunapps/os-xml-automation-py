import os_xml_handler.xml_handler as xh
from os_file_automation.xml_mapper import _shared_res as shared_res
import os_file_handler.file_handler as fh
import os
from os_tools import tools as tools

XML_TRUE = 'true'

NODE_STEP = 'step'
NODE_UNLINK = 'unlink'
NODE_UNLINK_ATT_DELETE = 'delete'
NODE_LINK = 'link'
NODE_PODS = 'pods'
NODE_POD = 'pod_line'
NODE_UNLINK_ATT_TYPE = 'type'
NODE_UNLINK_ATT_TYPE_VAL_DIR = 'dir'
NODE_UNLINK_ATT_TYPE_VAL_FILE = 'file'
NODE_FRAMEWORKS = 'frameworks'
NODE_ROOT_ATT_EXTENSION_MAPPER_PATH = 'extension_mapper_path'


# manipulate an xcode project by an xml properties file
def manipulate(xml_path, xml, place_holder_map):
    from os_xcode_tools import xcode_project_manipulator as xpm
    root_node = xh.get_root_node(xml)
    add_extension_nodes(place_holder_map, root_node, xml)

    project_properties_node = xh.get_child_nodes(root_node, 'project_properties')[0]

    # fetch the project properties
    project_root = xh.get_text_from_child_node(project_properties_node, 'project_root')
    xcodeproj_file_name = xh.get_text_from_child_node(project_properties_node, 'xcodeproj_file_name')
    root_dir_name = xh.get_text_from_child_node(project_properties_node, 'root_dir_name')
    bundle_identifier = xh.get_text_from_child_node(project_properties_node, 'bundle_identifier')
    product_name = xh.get_text_from_child_node(project_properties_node, 'product_name')
    plist_path = xh.get_text_from_child_node(project_properties_node, 'plist_path')
    logo_path = xh.get_text_from_child_node(project_properties_node, 'app_icon.appiconset')

    # set the general properties in the xcode project
    project = xpm.build_project(os.path.join(project_root, xcodeproj_file_name))
    xpm.set_bundle_identifier(project, bundle_identifier)
    xpm.set_product_name(project, product_name)

    # copy the plist file
    plist_dst = os.path.join(project_root, root_dir_name, 'Info.plist')
    plist_path = shared_res.fill_place_holders(plist_path, place_holder_map)
    fh.copy_file(plist_path, plist_dst, overwrite_if_needed=True)

    # copy the logo files
    logo_dst = os.path.join(project_root, root_dir_name, 'Assets.xcassets', 'AppIcon.appiconset')
    logo_path = shared_res.fill_place_holders(logo_path, place_holder_map)
    fh.remove_dir(logo_dst)
    fh.copy_dir(logo_path, logo_dst)

    # add file extensions
    added_files_extensions_node = xh.get_child_nodes(root_node, 'added_files_extensions')[0]
    extension_list = []
    for extension_node in xh.get_all_direct_child_nodes(added_files_extensions_node):
        extension_list.append(xh.get_text_from_node(extension_node))
    xpm.add_files_extensions_arr(extension_list)

    # start running on all of the steps
    run_next_step_cycle(project, root_node, xml_path, place_holder_map, curr_step=1)
    print_line()
    print('saving...')
    xpm.save_changes(project)


# will add all of the nodes from the extension file to the xml
def add_extension_nodes(place_holder_map, root_node, xml):
    extension_mapper_path = xh.get_node_att(root_node, NODE_ROOT_ATT_EXTENSION_MAPPER_PATH)
    if extension_mapper_path:
        extension_mapper_path = shared_res.fill_place_holders(extension_mapper_path, place_holder_map)
        extension_xml = xh.read_xml_file(extension_mapper_path)
        return xh.merge_xml1_with_xml2(extension_xml, xml)
    else:
        return xml


# operate the next step
def run_next_step_cycle(project, root_node, xml_path, place_holder_map, curr_step):
    next_step_node = xh.get_child_nodes(root_node, f'{NODE_STEP}_{str(curr_step)}')

    # if the next step exists, start running on all of the direct children
    if next_step_node:
        print_line()
        print(f'Starting step: {str(curr_step)}')
        next_step_node = next_step_node[0]
        for curr_step_child_node in xh.get_all_direct_child_nodes(next_step_node):
            curr_step_tag = curr_step_child_node.tag

            # if link
            if curr_step_tag == NODE_LINK:
                do_link_tag(project, xml_path, place_holder_map, curr_step_child_node)

            # if unlink
            elif curr_step_tag == NODE_UNLINK:
                do_unlink_tag(project, place_holder_map, curr_step_child_node)

            # if pods
            elif curr_step_tag == NODE_PODS:
                do_pods_tag(project, place_holder_map, curr_step_child_node)

            # if frameworks
            elif curr_step_tag == NODE_FRAMEWORKS:
                do_frameworks_tag(project, place_holder_map, curr_step_child_node)
        print('done!')
        run_next_step_cycle(project, root_node, xml_path, place_holder_map, curr_step + 1)


# will operate the <unlink> tag
def do_unlink_tag(project, place_holder_map, node):
    from os_xcode_tools import xcode_project_manipulator as xpm
    node_path = xh.get_text_from_node(node)
    node_path = shared_res.fill_place_holders(node_path, place_holder_map)
    node_type = xh.get_node_att(node, NODE_UNLINK_ATT_TYPE)
    if node_type == NODE_UNLINK_ATT_TYPE_VAL_DIR:
        node_group = xpm.get_or_create_group(project, path_to_group=node_path)
        xpm.remove_group(project, node_group)
    elif node_type == NODE_UNLINK_ATT_TYPE_VAL_FILE:
        node_group = xpm.get_or_create_group(project, path_to_group=fh.get_parent_path(node_path))
        xpm.remove_file_from_group(project, node_group, fh.get_file_name_from_path(node_path))

    if xh.get_node_att(node, NODE_UNLINK_ATT_DELETE) == XML_TRUE:
        project_grandpa_path = os.path.join(xpm.get_project_root(project), '..')
        path_to_delete = os.path.join(project_grandpa_path, node_path)
        if fh.is_dir_exists(path_to_delete):
            fh.remove_dir(path_to_delete)
        elif fh.is_file_exists(path_to_delete):
            fh.remove_file(path_to_delete)


# will operate the <link> tag
def do_link_tag(project, xml_path, place_holder_map, link_node):
    # get the src <file_src> or the <dir_src> (from the computer's path)
    from os_xcode_tools import xcode_project_manipulator as xpm
    if xh.get_child_nodes(link_node, shared_res.NODE_DIR_SRC):

        # dir copy
        src_text = shared_res.get_file_node_path(xml_path, place_holder_map, link_node, shared_res.NODE_DIR_SRC, file_search=False)
        dst_node = xh.get_child_nodes(link_node, shared_res.NODE_DIR_DST)[0]
        dst_text = xh.get_text_from_child_node(dst_node, 'path')
        dst_text = shared_res.fill_place_holders(dst_text, place_holder_map)
        xpm.add_dir(project, src_text, dst_text)

    else:

        # file copy
        src_text = shared_res.get_file_node_path(xml_path, place_holder_map, link_node, shared_res.NODE_FILE_SRC, file_search=True)
        dst_node = xh.get_child_nodes(link_node, shared_res.NODE_FILE_DST)[0]
        dst_text = xh.get_text_from_child_node(dst_node, 'path')
        dst_text = shared_res.fill_place_holders(dst_text, place_holder_map)
        file_group = xpm.get_or_create_group(project, fh.get_parent_path(dst_text))
        xpm.add_file_to_group(project, src_text, file_group)


# will operate the <pods> tag
def do_pods_tag(project, place_holder_map, pods_node):
    # find the pod file
    from os_xcode_tools import xcode_project_manipulator as xpm
    project_path = xpm.get_project_root(project)
    pods_file_path = fh.search_file(project_path, 'Podfile', recursive=True)[0]

    # copy the first part of the pods
    from os_file_stream_handler import file_stream_handler as fsh
    pod_file_lines = fsh.read_file(pods_file_path)
    pod_file_output = []
    for line in pod_file_lines:
        pod_file_output.append(line)
        if 'target ' in line:
            break

    # read the pods to lines and append them
    pod_nodes = xh.get_child_nodes(pods_node, NODE_POD)
    for pod in pod_nodes:
        pod_text = xh.get_text_from_node(pod)
        pod_text = shared_res.fill_place_holders(pod_text, place_holder_map)
        pod_file_output.append(f'{pod_text}\n')

    # add the pods
    pod_file_output.append('\nend')
    fsh.write_file(pods_file_path, pod_file_output)

    # save and run pod install
    print("Installing pods...")
    tools.run_command(f'cd {project_path} && pod install')


# will operate the <frameworks> tag
def do_frameworks_tag(project, place_holder_map, frameworks_node):
    # get all of the frameworks
    framework_dict_list = []
    for framework_node in xh.get_all_direct_child_nodes(frameworks_node):
        framework_path = xh.get_text_from_child_node(framework_node, 'path')
        framework_path = shared_res.fill_place_holders(framework_path, place_holder_map)
        framework_type = xh.get_text_from_child_node(framework_node, 'type')

        framework_dict_list.append(
            {
                'type': framework_type,
                'path': framework_path,
            }
        )

    from os_xcode_tools import xcode_project_manipulator as xpm
    xpm.set_frameworks(project, framework_dict_list)


def print_line():
    print('-----------------------------------------------------------------------')
