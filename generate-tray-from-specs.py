import json


def compute_minimum_dimensions(item):
    single_item = item_types[item['item']]
    return {
        'min-width': single_item['width'],
        'min-depth': single_item['height'],
        'min-height': single_item['thickness'] * item['amount']
            }


def sum_of_heights(col_items):
    def map_heights(item):
        if 'height' in item:
            return item['height']
        return item['min-height']

    return reduce(lambda add,aggr: add+aggr, map(map_heights, col_items))


def validate_fit(col_items, max_height):
    height_sum = sum_of_heights(col_items)
    height_spacers = (len(col_items)-1)*spacer_width
    height_edges = 2 * edge_width
    total_content = height_sum+height_spacers+height_edges

    #print("Items: {}, Spacers: {}, Edges: {}, Total: {}".format( height_sum, height_spacers, height_edges, total_content))
    if total_content > max_height:
        raise Exception("Total content height [{}] is larger than tray height [{}]".format(total_content, max_height))


def stretch_to_fill(col_items, max_height):
    height_contents = sum_of_heights(col_items)
    height_spacers = (len(col_items)-1)*spacer_width
    height_edges = 2 * edge_width
    total_height = height_contents + height_spacers + height_edges

    unused_space = max_height - total_height
    if height_contents * 0.3 < unused_space:
        fraction = unused_space / height_contents
        raise Exception("There is more than 30% extra space available for contents [{}]. Add more stuff?".format(fraction))

    add_height = unused_space / len(col_items)
    for item in col_items:
        item['height'] = round(item['min-height'] + add_height,2)
    return(col_items)


def compute_spacer_placement(columns):
    placement_lists = []
    for left_col_index in range(0,len(columns)-1):
        placement_lists.append({
            "left": columns[left_col_index],
            "right": columns[left_col_index + 1]
            })
    print(placement_lists)

if __name__ == '__main__':
    specs = {}
    with open('gloomhaven/tray_specs.json') as specsfile:
        specs = json.load(specsfile)
        specsfile.close

    item_types = specs['item-types']

    tray_width = specs['dimensions']['width']
    tray_height = specs['dimensions']['height']

    spacer_width = 2
    edge_width = 3.5

    colnum = 1

    columns = []

    for col in specs['columns']:
        col_items = map(compute_minimum_dimensions, col)
        print("Column number: {}".format(colnum))
        validate_fit(col_items, tray_height)
        colnum += 1
        stretch_to_fill(col_items, tray_height)
        columns.append(col_items) 

    compute_spacer_placement(columns)

