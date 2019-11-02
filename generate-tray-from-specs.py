import json
from llist import dllist
import sys


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


def validate_fit(col_items, max_height):
    height_sum = sum_of_heights(col_items)
    height_spacers = (col_items.size-1)*spacer_width
    height_edges = 2 * edge_width
    total_content = height_sum+height_spacers+height_edges

    #print("Items: {}, Spacers: {}, Edges: {}, Total: {}".format( height_sum, height_spacers, height_edges, total_content))
    if total_content > max_height:
        raise Exception("Total content height [{}] is larger than tray height [{}]".format(total_content, max_height))


def position_spacers(left_col, right_col, spacer_width):
    fit_range = 1.0 + spacer_width

    def extend_node_height(node, extension):
        node.value['height'] = extension + get_height(node.value)


    def position_nodes(lnode, rnode, lheight, rheight):
        print("left height {}, right height: {}".format(lheight, rheight))
        if (not lnode) or (not rnode):
            print("End of either node list reached.")
            return 0

        lheight += get_height(lnode.value)
        rheight += get_height(rnode.value)

        if abs(lheight-rheight) < 0.001:
            print("Matching spacers, moving on")
            return position_nodes(lnode.next, rnode.next, 0, 0)

        height_diff = abs(lheight-rheight)
        if height_diff < fit_range:
            print("Difference between spacers: {}".format(abs(lheight-rheight)))
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
                print("Extending right node by {}, previously {}".format(height_diff, get_height(rnode.value)))
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

    print("Total height: {} , Max_height: {}".format(total_height, max_height))
    unused_space = max_height - total_height
    if unused_space / total_height > 0.3:
        fraction = unused_space / total_height
        raise Exception("There is more than 30% extra space available for contents [{}]. Add more stuff?".format(fraction))

    add_height = unused_space / len(col_items)
    for item in col_items:
        item['height'] = round(item['min-height'] + add_height,2)
    return(col_items)


def process_column_contents(specs, tray_height):
    item_types = specs['item-types']

    columns = []

    for col in specs['columns']:
        col_items = dllist(map(lambda c_item: compute_minimum_dimensions(item_types, c_item), col))
        validate_fit(col_items, tray_height)
        columns.append(col_items) 

    for colidx in range(0, len(columns)-1):
        position_spacers(columns[colidx], columns[colidx+1], spacer_width)    

    return columns


if __name__ == '__main__':
    specs = {}

    spacer_width = 2
    edge_width = 3.5

    specsfile = sys.argv[1] #gloomhaven/tray_specs.json
    with open(specsfile) as specsfile:
        specs = json.load(specsfile)
        specsfile.close

    tray_width = specs['dimensions']['width']
    tray_height = specs['dimensions']['height']

    columns = process_column_contents(specs, tray_height)
    
    print(columns)

