import json
from llist import dllist
import sys
from random import choice
from string import ascii_lowercase


def compute_minimum_dimensions(item_types, item):
    item_type = item['item']
    if item_type not in item_types:
        raise Exception(f"Item type [ {item_type} ] not specified!")
    single_item = item_types[item['item']]
    elastic = False if 'elastic' not in item else True
    label = None if 'label' not in item else item['label']
    spacer_indent = None if 'spacer-indent' not in item else item['spacer-indent']
    return {
        'min-width': single_item['width'],
        'min-depth': single_item['height'],
        'min-height': single_item['thickness'] * item['amount'],
        'elastic': elastic,
        'extra-space': 0,
        'spacer-indent': spacer_indent,
        'needs_indent': 'needs_indent' in single_item and single_item['needs_indent'],
        'forbid_intent': 'forbid_indent' in single_item and single_item['forbid_indent'],
        'label': label
        }


def get_height(item):
    return item['min-height'] + item['extra-space']


def sum_of_heights(col_items):
    return sum(list([get_height(item) for item in col_items]))


def validate_fit(col_items, max_height, spacer_width, edge_width):
    height_sum = sum_of_heights(col_items)
    height_spacers = (col_items.size-1)*spacer_width
    height_edges = 2 * edge_width
    total_content = height_sum+height_spacers+height_edges

    extra_space = max_height - total_content

    if extra_space < 0:
        raise Exception("Total content height [{}] is larger than tray height [{}]".format(total_content, max_height))
    return extra_space


def random_string(stringLength=10):
    letters = ascii_lowercase
    return ''.join(choice(letters) for i in range(stringLength))


# For multi-column trays the colums may have spacers in exact same spots - or close enough
# to be moved to exact match. Then we can use multicolumn-spacers.
# Or there might be just enough difference between spacers that they cannot coexist and
# cannot be moved either. This should report an error.
def position_spacers(left_col, right_col, spacer_width):
    fit_range = 1.0 + spacer_width

    def extend_node_height(node, extension):
        node.value['height'] = extension + get_height(node.value)

    def position_nodes(lnode, rnode, left_height, right_height):
        if (not lnode) or (not rnode):
            return

        def set_col_span_id(lnode, rnode):
            if 'column_span_id' not in lnode():
                lnode()['column_span_id'] = random_string() 
            rnode()['column_span_id'] = lnode()['column_span_id']

        lheight = left_height + get_height(lnode.value)
        rheight = right_height + get_height(rnode.value)

        # Columns matching, link them and carry on
        if abs(lheight-rheight) < 0.001:
            set_col_span_id(lnode, rnode) 
            return position_nodes(lnode.next, rnode.next, 0, 0)

        height_diff = abs(lheight-rheight)
        # Slot endings are close to each other
        if height_diff < fit_range:
            if lheight < rheight:
                # Left node cannot be moved, because it might conflict with the next left column
                # Extend right node to avoid partially overlapping spacers.
                space_to_add = height_diff - fit_range

                rnext = rnode.next()
                if rnext['extra-space'] > space_to_add:
                    rnext['extra-space'] -= space_to_add
                    rnode()['extra-space'] += space_to_add
                return position_nodes(lnode.next, rnode, lheight + spacer_width, right_height)
            else:
                extend_node_height(rnode, height_diff)
                set_col_span_id(lnode, rnode)
                return position_nodes(lnode.next, rnode.next, 0, 0)

        if lheight < rheight:
            return position_nodes(lnode.next, rnode, lheight + spacer_width, right_height)
        else:
            return position_nodes(lnode, rnode.next, left_height, spacer_width + right_height)

    lnode = left_col.first
    rnode = right_col.first
    position_nodes(lnode, rnode, 0, 0)


def dllist_min_width(slot_dllist):
    widths = []
    for node in slot_dllist:
        widths.append(node['min-width'])
    return min(widths)


def process_column_contents(specs, item_types, tray_height, spacer_width, edge_width):
    columns = []
    print("Height: {}".format(specs['dimensions']['height']))

    for col in specs['columns']:
        col_items = dllist(list(map(lambda c_item: compute_minimum_dimensions(item_types, c_item), col['slots'])))
        extra_space = validate_fit(col_items, tray_height, spacer_width, edge_width)
        num_elastic_slots = len(list(filter(lambda item: item['elastic'], col_items)))
        if num_elastic_slots == 0:
            raise Exception("No elastic slots to allocate extra space")
        for slot in col_items:
            slot['extra-space'] = extra_space / num_elastic_slots

        columns.append({
            'slots': col_items,
            'width': dllist_min_width(col_items),
            'elastic': col['elastic']
            }) 

    for col_index, column in enumerate(columns):
        if col_index+1 is len(columns):
            break
        position_spacers(columns[col_index]['slots'], columns[col_index+1]['slots'], spacer_width)

    return columns


def generate_trays_from_spec(spacer_width, edge_width, specs, trayname=None):
    trays = specs['trays']
    item_types = specs['item-types']
    processed_trays = list([generate_columns_from_spec(spacer_width, edge_width, tray, item_types) for tray in trays
                            if (tray['name']==trayname or trayname is None)])
    if not processed_trays:
        print(f"No trays found in spec or matching given tray name {trayname}")
    return processed_trays


def generate_columns_from_spec(spacer_width, edge_width, tray_specs, item_types):
    specs = tray_specs
    print('Building tray "{}"'.format(specs['name']))

    tray_width = specs['dimensions']['width']
    tray_height = specs['dimensions']['height']

    columns = process_column_contents(specs, item_types, tray_height, spacer_width, edge_width)
    depth = max(list(map(lambda column: max(list(map(lambda slot: slot['min-depth'], column['slots']))), columns)))

    tray_spec = {
            'name': specs['name'],
            'tray_width': tray_width,
            'tray_height': tray_height,
            'tray_depth': depth,
            'columns': columns,
            'spacer_width': spacer_width,
            'edge_width': edge_width
            }

    total_used_width = 2 * edge_width + spacer_width * (len(tray_spec['columns'])-1) + sum(map(lambda c: c['width'], tray_spec['columns']))
    if total_used_width < tray_spec['tray_width'] - 0.01:
        missing_width = tray_spec['tray_width'] - total_used_width
        print("Content is {}mm less than available {}mm".format(missing_width, tray_spec['tray_width']))
        elastic_columns = list(filter(lambda col: col['elastic'], columns))
        if elastic_columns:
            print("Expanding *elastic* columns' width")

        for ecolumn in elastic_columns:
            ecolumn['width'] += missing_width / len(elastic_columns)
        return tray_spec
    elif total_used_width > tray_spec['tray_width'] + 0.01:
        print("Content is {}mm more than available {}mm".format(total_used_width-tray_spec['tray_width'], tray_spec['tray_width']))
        print("")
        print("--- How to fix it? ---")
        print("Until this tool supports multi-tray generation, you need to split the content into")
        print("several trays that fit in the outer box dmensions")
        sys.exit(1)
    else:
        return tray_spec


def get_specification(specsfile):
    specs = {}
    with open(specsfile) as spec_stream:
        specs = json.load(spec_stream)
        spec_stream.close()

    trays = specs['trays']
    for tray in trays:
        if not tray['dimensions']['width'] or not tray['dimensions']['height']:
            print('Each tray has to have "dimensions" entry with "width" and "height"')
            sys.exit(1)

    tray_names = [tray['name'] for tray in trays]
    for name in set(tray_names):
        if tray_names.count(name) > 1:
            print("Duplicate tray name: {}. Names are used as part of filenames, so no duplicates are allowed".format(name))
            sys.exit(1)

    return specs
