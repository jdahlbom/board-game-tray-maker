import json
from llist import dllist
import sys
from functools import reduce

def compute_minimum_dimensions(item_types, item):
    single_item = item_types[item['item']]
    return {
        'min-width': single_item['width'],
        'min-depth': single_item['height'],
        'min-height': single_item['thickness'] * item['amount']
            }


def get_height(item):
    if 'height' in item:
        return item['height']
    return item['min-height']


def sum_of_heights(col_items):
    return reduce(lambda add,aggr: add+aggr, map(get_height, col_items))


def validate_fit(col_items, max_height, spacer_width, edge_width):
    height_sum = sum_of_heights(col_items)
    height_spacers = (col_items.size-1)*spacer_width
    height_edges = 2 * edge_width
    total_content = height_sum+height_spacers+height_edges

    if total_content > max_height:
        raise Exception("Total content height [{}] is larger than tray height [{}]".format(total_content, max_height))


def position_spacers(left_col, right_col, spacer_width):
    fit_range = 1.0 + spacer_width

    def extend_node_height(node, extension):
        node.value['height'] = extension + get_height(node.value)


    def position_nodes(lnode, rnode, lheight, rheight):
        if (not lnode) or (not rnode):
            return 0

        lheight += get_height(lnode.value)
        rheight += get_height(rnode.value)

        if abs(lheight-rheight) < 0.001:
            return position_nodes(lnode.next, rnode.next, 0, 0)

        height_diff = abs(lheight-rheight)
        if height_diff < fit_range:
            if lheight < rheight:
                lnext = lnode.next
                if lnext:
                    lnext_height = get_height(lnext.value) + spacer_width
                    r_diff_to_lnext = lheight + lnext_height - rheight
                    if r_diff_to_lnext < fit_range:
                        extend_node_height(rnode, r_diff_to_lnext)
                        return position_nodes(lnext.next, rnode.next, 0, 0)
                r_extension = fit_range - height_diff
                extend_node_height(rnode, r_extension)
                return position_nodes(lnode.next, rnode.next, 0, fit_range)
            else:
                extend_node_height(rnode, height_diff)
                return position_nodes(lnode.next, rnode.next, 0, 0)

        if lheight < rheight:
            return position_nodes(lnode.next, rnode, spacer_width + height_diff, 0)
        else:
            return position_nodes(lnode, rnode.next, 0, spacer_width + height_diff)

    lnode = left_col.first
    rnode = right_col.first
    position_nodes(lnode, rnode, 0, 0)


def stretch_to_fill(col_items, max_height):
    height_contents = sum_of_heights(col_items)
    height_spacers = (len(col_items)-1)*spacer_width
    height_edges = 2 * edge_width
    total_height = height_contents + height_spacers + height_edges

    unused_space = max_height - total_height
    if unused_space / total_height > 0.3:
        fraction = unused_space / total_height
        raise Exception("There is more than 30% extra space available for contents [{}]. Add more stuff?".format(fraction))

    add_height = unused_space / len(col_items)
    for item in col_items:
        item['height'] = round(item['min-height'] + add_height,2)
    return(col_items)


def dllist_min_width(slot_dllist):
    widths = []
    for node in slot_dllist:
        widths.append(node['min-width'])
    return min(widths)


def process_column_contents(specs, tray_height, spacer_width, edge_width):
    item_types = specs['item-types']

    columns = []

    for col in specs['columns']:
        col_items = dllist(list(map(lambda c_item: compute_minimum_dimensions(item_types, c_item), col)))
        validate_fit(col_items, tray_height, spacer_width, edge_width)
        columns.append({
            'slots': col_items,
            'width': dllist_min_width(col_items)
            }) 

    for colidx in range(0, len(columns)-1):
        position_spacers(columns[colidx]['slots'], columns[colidx+1]['slots'], spacer_width)    

    return columns


def generate_columns_from_spec(spacer_width, edge_width, specsfile):
    specs = {}

    with open(specsfile) as specsfile:
        specs = json.load(specsfile)
        specsfile.close

    tray_width = specs['dimensions']['width']
    tray_height = specs['dimensions']['height']

    columns = process_column_contents(specs, tray_height, spacer_width, edge_width)
    depth = max(list(map(lambda column: max(list(map(lambda slot: slot['min-depth'], column['slots']))), columns)))

    return {
            'tray_width': tray_width,
            'tray_height': tray_height,
            'tray_depth': depth,
            'columns': columns,
            'spacer_width': spacer_width,
            'edge_width': edge_width
            }


