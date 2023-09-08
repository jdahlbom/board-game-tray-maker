import svgwrite
import sys

exec(open('generate-tray-from-specs.py').read())

STROKE = 0.1
MIN_TOOTH_WIDTH = 10
INDENT_DEPTH = 10
KERF = 0.2
K_CORR = KERF/2.0


def mm(value):
    return '{}mm'.format(value)


def get_drawing(result_file_name, width, height):
    return svgwrite.Drawing(
            filename=result_file_name, 
            size=('{}mm'.format(width), '{}mm'.format(height)),
            viewBox=(0, 0, width, height))


def kerf_correct_corner(path, corner_index):
    if corner_index == 0:
        path.push('h {}'.format(K_CORR))
    elif corner_index == 1:
        path.push('h {} v {}'.format(K_CORR, K_CORR))
    elif corner_index == 2:
        path.push('v {} h -{}'.format(K_CORR, K_CORR))
    elif corner_index == 3:
        path.push('h -{} v -{}'.format(K_CORR, K_CORR))
    elif corner_index == 4:
        path.push('v {}'.format(K_CORR))


def generate_toothing(direction, path, invert, length, tooth_depth):
    #Directions:
    #0 - right
    #1 - down
    #2 - left
    #3 - up

    def axis(clockwise_rot):
        move_dir = (clockwise_rot + direction) % 4
        if move_dir % 2 == 1:
            return 'v'
        else:
            return 'h'

    def dir_value(clockwise_rot, abs_value):
        rot_dir = (clockwise_rot + direction) % 4
        if rot_dir == 0 or rot_dir == 1:
            value = abs_value
        else:
            value = 0-abs_value
        
        if invert and clockwise_rot % 2 == 1:
            value = 0-value
        return value

    if length / MIN_TOOTH_WIDTH < 3:
        raise Exception("Edge too short for toothing: {}".format(length))

    divisions = int(length / 10)
    if divisions % 2 == 0:
        divisions -= 1
    if divisions > 9:
        divisions = 9
    tooth_width = length / divisions

    for idx in range(0, divisions):
        if idx % 2 == 0:
            path.push('{} {}'.format(axis(0), dir_value(0, tooth_width)))
        else:
            path.push('{} {}'.format(axis(1), dir_value(1, tooth_depth)))
            path.push('{} {}'.format(axis(0), dir_value(0, tooth_width)))
            path.push('{} {}'.format(axis(3), dir_value(3, tooth_depth)))


def generate_slotted_top_edge(slots, spacer_width, content_width, corner_toothing, edge_width):
    def should_create_sloped_indent(slot, margin):
        return 'needs_indent' in slot['slot_properties'] and \
               slot['slot_properties']['needs_indent'] and \
               slot['width'] > (30.0 + 2 * margin)

    path_parts = []
    if corner_toothing:
        path_parts.append('h {}'.format(edge_width))

    width_left = content_width
    for idx, slot in enumerate(slots):
        width_left -= slot['width']
        margin = 10.0
        if should_create_sloped_indent(slot, margin):
            path_parts.append('h {}'.format(margin))
            path_parts = path_parts + cubic_sloped_indent(slot['width']-2*margin, slot['width']-20.0-2*margin, 10.0)
            path_parts.append('h {}'.format(margin))
        else:
            path_parts.append('h {}'.format(slot['width']))
        if idx < len(slots)-1 or width_left > spacer_width:
            width_left -= spacer_width
            path_parts.append('h {}'.format(K_CORR))
            path_parts.append('v {}'.format(INDENT_DEPTH - K_CORR))
            path_parts.append('h {}'.format(spacer_width - K_CORR*2))
            path_parts.append('v -{}'.format(INDENT_DEPTH - K_CORR))
            path_parts.append('h {}'.format(K_CORR))

    if width_left > 0:
        print("[WARN] Edge width unused for slots: {} , extending by that much!".format(width_left))
        path_parts.append('h {}'.format(width_left))

    if corner_toothing:
        path_parts.append('h {}'.format(edge_width))

    return path_parts


def generate_edges(dwg, trayspec):
    spacer_w = trayspec['spacer_width']
    edge_w = trayspec['edge_width']
    depth = trayspec['tray_depth']
 
    def generate_edge(slots, spacer_width, content_width, corner_toothing, edge_width, v_offset):
        path = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
        if corner_toothing:
            path.push('M 0 {}'.format(v_offset))
        else:
            path.push('M {} {}'.format(edge_width, v_offset))

        kerf_correct_corner(path, 0)
        path_parts = generate_slotted_top_edge(slots, spacer_width, content_width, corner_toothing, edge_width)
        for part in path_parts:
            path.push(part)
        #Right edge
        kerf_correct_corner(path, 1)
        generate_toothing(1, path, not corner_toothing, depth, edge_width)
        path.push('v {}'.format(edge_width))
        #Bottom edge
       
        kerf_correct_corner(path, 2)
        if corner_toothing:
            path.push('h -{}'.format(edge_w))

        generate_toothing(2, path, False, content_width, edge_width)

        if corner_toothing:
            path.push('h -{}'.format(edge_w))

        kerf_correct_corner(path, 3)
        #Left edge
        path.push('v -{}'.format(edge_w))
        generate_toothing(3, path, not corner_toothing, depth, edge_width)
        kerf_correct_corner(path, 4)
        path.push('z')
        return path


    content_width = trayspec['tray_width']-edge_w*2
    content_height = trayspec['tray_height']-edge_w*2
    #Top edge
    horiz_slots_and_widths = list(map(lambda column: {'width': column['width'], 'slot_properties': column['slots'][0]}, trayspec['columns']))
    paths = []
    paths.append( generate_edge(
        horiz_slots_and_widths,
        spacer_w, 
        content_width, 
        True, 
        edge_w, 
        0) )

    #Right edge
    def slots_from_column(column_slots):
        def get_height(slot):
            if 'height' in slot:
                return slot['height']
            return slot['min-height']

        return list(map(lambda slot: {'width': get_height(slot), 'slot_properties': slot}, column_slots))

    slot_widths = slots_from_column(trayspec['columns'][-1]['slots'])
    paths.append( generate_edge(
        slot_widths, 
        spacer_w, 
        content_height, 
        False, 
        edge_w, 
        (depth + 5)*1) )
    
    #Bottom edge
    horiz_slot_width_sum = sum([slot['width'] for slot in horiz_slots_and_widths])
    if horiz_slot_width_sum + spacer_w * (len(horiz_slots_and_widths)-1) < content_width:
        print("Too little column content, appending empty")
        empty_space = content_width - sum(horiz_slot_width_sum) - spacer_w*len(horiz_slots_and_widths)
        horiz_slots_and_widths.append({'width': empty_space, 'slot_properties': {}})

    paths.append(generate_edge(
        horiz_slots_and_widths[::-1],
        spacer_w,
        content_width,
        True,
        edge_w,
        (depth + 5)*2))

    #Left edge
    slots = slots_from_column(trayspec['columns'][0]['slots'])
    slot_width_sum = sum([slot['width'] for slot in slots])
    if slot_width_sum + spacer_w*(len(slots)-1) < content_height:
        print("Too little column content in column 0, appending empty")
        empty_space = content_height - slot_width_sum - spacer_w*(len(slots))
        slots.append( {'width': empty_space, 'slot_properties': {}})
    
    paths.append(generate_edge(
        slots[::-1],
        spacer_w,
        content_height,
        False,
        edge_w,
        (depth + 5)*3) )

    return paths


def generate_floor(dwg, trayspec, v_offset):
    edge_w = trayspec['edge_width']
    spacer_w = trayspec['spacer_width']
    width = trayspec['tray_width'] - edge_w*2
    height = trayspec['tray_height'] - edge_w*2

    path = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
    path.push('M {} {}'.format(edge_w, v_offset + edge_w))
    kerf_correct_corner(path, 0)
    generate_toothing(0, path, True, width, edge_w)
    kerf_correct_corner(path, 1)
    generate_toothing(1, path, True, height, edge_w)
    kerf_correct_corner(path, 2)
    generate_toothing(2, path, True, width, edge_w)
    kerf_correct_corner(path, 3)
    generate_toothing(3, path, True, height, edge_w)

    def generate_internal_holes(path, origin_h_offset, origin_v_offset):
        col_widths = list(map(lambda col: col['width'], trayspec['columns']))
        hole_width = MIN_TOOTH_WIDTH
        if height/hole_width < 3:
            return

        num_tooth = 1
        if height/hole_width > 5:
            num_tooth = 2

        tooth_spacing = (height - num_tooth * hole_width) / (num_tooth + 1)

        for idx, col_w in enumerate(col_widths[0:-1]):
            h_offset = sum(col_widths[0:idx+1]) + idx * spacer_w + origin_h_offset
            for tooth_idx in range(0, num_tooth):
                v_offset = (tooth_idx + 1) * tooth_spacing + tooth_idx * hole_width + origin_v_offset
                path.push('M {} {}'.format(h_offset, v_offset))
                path.push('m {} {}'.format(K_CORR, K_CORR))
                path.push('h {}'.format(spacer_w - K_CORR*2))
                path.push('v {}'.format(hole_width - K_CORR*2))
                path.push('h -{}'.format(spacer_w - K_CORR*2))
                path.push('v -{}'.format(hole_width - K_CORR*2))

    generate_internal_holes(path, edge_w, v_offset+edge_w)

    return path


def generate_vert_spacer(indent_spaces, content_width, depth, edge_width, spacer_width):
    path_parts = []
    kerf_correct_corner(path_parts, 0)
    generate_slotted_top_edge(path_parts, indent_spaces, spacer_width, content_width, True, edge_width)
    kerf_correct_corner(path_parts, 1)

    path_parts.append('v {}'.format(INDENT_DEPTH))
    kerf_correct_corner(path_parts, 2)
    path_parts.append('h -{}'.format(edge_width))
    path_parts.append('v {}'.format(depth - INDENT_DEPTH))

    def generate_floor_teeth(width):
        path_elems = []
        hole_width = MIN_TOOTH_WIDTH
        if width/hole_width < 3:
            return

        num_tooth = 1
        if width/hole_width > 5:
            num_tooth = 2

        tooth_spacing = (width - num_tooth * hole_width) / (num_tooth + 1)

        for tooth_idx in range(0, num_tooth):
            if tooth_idx == 0:
                path_elems.push('h -{}'.format(tooth_spacing - K_CORR))
            else:
                path_elems.push('h -{}'.format(tooth_spacing - 2*K_CORR))
            path_elems.push('v {}'.format(edge_width + K_CORR))
            path_elems.push('h -{}'.format(hole_width + K_CORR*2))
            path_elems.push('v -{}'.format(edge_width + K_CORR))
        path_elems.push('h -{}'.format(tooth_spacing - K_CORR))
        return path_elems

    path_parts = path_parts + generate_floor_teeth(content_width)
    kerf_correct_corner(path_parts, 3)
    path_parts.append('v -{}'.format(depth - INDENT_DEPTH))
    path_parts.append('h -{}'.format(edge_width))
    path_parts.append('v -{}'.format(INDENT_DEPTH + K_CORR))
    kerf_correct_corner(path_parts, 4)
    path_parts.append('z')
    return path_parts


# Generates SVG string path parts to draw a single horizontal spacer.
# Horizontal spacer may span multiple columns.
# This function is not aware of the column specifications, merely the drawing element inputs
# Returns: Array of SVG path strings.
def generate_horiz_spacer(bottom_indents, spacer_indents, content_width, spacer_width, l_edge_width, r_edge_width, depth):
    path_parts = []
    path_parts.append('h {}'.format(l_edge_width + K_CORR))
    if len(list(filter(lambda spacer: spacer, spacer_indents))) > 0:
        for idx, slot_width in enumerate(bottom_indents):
            if spacer_indents[idx] > 0:
                path_parts.append('h {}'.format(bottom_indents[idx]/4))
                path_parts = path_parts + cubic_sloped_indent(bottom_indents[idx]/2, bottom_indents[idx]/4.0, spacer_indents[idx]*depth)
                path_parts.append('h {}'.format(bottom_indents[idx]/4))
            else:
                path_parts.append('h {}'.format(bottom_indents[idx]))
            if idx < len(bottom_indents)-1:
                path_parts.append('h {}'.format(spacer_width))
    else:
        path_parts.append('h {}'.format(content_width))
    path_parts.append('h {}'.format(r_edge_width + K_CORR))

    path_parts.append('v {}'.format(INDENT_DEPTH + K_CORR*2))
    path_parts.append('h -{}'.format(r_edge_width))
    path_parts.append('v {}'.format(depth - INDENT_DEPTH))

    #Bottom with indent slots
    for idx, slot in enumerate(bottom_indents[::-1]):
        path_parts.append('h -{}'.format(slot + K_CORR*2))
        if idx != len(bottom_indents)-1:
            path_parts.append('v -{}'.format(depth-INDENT_DEPTH - K_CORR))
            path_parts.append('h -{}'.format(spacer_width - K_CORR*2))
            path_parts.append('v {}'.format(depth-INDENT_DEPTH - K_CORR))

    path_parts.append('v -{}'.format(depth-INDENT_DEPTH))
    path_parts.append('h -{}'.format(l_edge_width))
    path_parts.append('v -{}'.format(INDENT_DEPTH + K_CORR*2))
    path_parts.append('z')
    return path_parts


def cubic_sloped_indent(top_width, bottom_width, depth):
    def cubic_bezier_curve(corner1, corner2, end_point):
        return "c {},{} {},{} {},{} ".format(
                corner1[0], corner1[1], 
                corner2[0], corner2[1],
                end_point[0], end_point[1])

    path_parts = []

    # relative arc
    slope_width = (top_width - bottom_width) / 2.0
    slope_corner_offsetx = slope_width / 2.0
    corner1 = ( slope_corner_offsetx, 0 )
    corner2 = ( slope_width - slope_corner_offsetx, depth )
    end_point = ( slope_width, depth )
    down_slope_cmd = cubic_bezier_curve(corner1, corner2, end_point)
    path_parts.append(down_slope_cmd)
    base_cmd = "h {} ".format(bottom_width)
    path_parts.append(base_cmd)
    corner1 = ( slope_corner_offsetx, 0 )
    corner2 = ( slope_width - slope_corner_offsetx, -depth )
    end_point = ( slope_width, -depth )
    up_slope_cmd = cubic_bezier_curve(corner1, corner2, end_point)
    path_parts.append(up_slope_cmd)
    return path_parts


def draw_spacers(dwg, trayspec):
    columns = trayspec['columns']
    spacer_w = trayspec['spacer_width']
    edge_w = trayspec['edge_width']
    depth = trayspec['tray_depth']
    content_width = trayspec['tray_height'] - 2 * edge_w

    paths = []

    # Generate spacer indent slots for vertical dividing spacers: Need to observe both columns
    for idx, column in enumerate(columns[0:-1]):
        indent_gaps = []
        lslot = column['slots'].first
        rcolumn = columns[idx+1]
        rslot = rcolumn['slots'].first
        ldist = 0
        rdist = 0
        while lslot is not column['slots'].last or rslot is not rcolumn['slots'].last:
            lheight = lslot()['height']
            rheight = rslot()['height']

            if ('col_span_id' in lslot() and 
                'col_span_id' in rslot() and 
                lslot()['col_span_id']==rslot()['col_span_id']):
                ldist = 0
                rdist = 0
                indent_gaps.append(lheight)
                lslot = lslot.next
                rslot = rslot.next
            else:
                if ldist + lheight < rdist + rheight:
                    next_gap = lheight
                    if ldist < rdist:
                        next_gap = ldist + lheight - rdist
                    indent_gaps.append(next_gap)
                    ldist += lheight + spacer_w
                    lslot = lslot.next
                else:
                    next_gap = rheight
                    if rdist < ldist:
                        next_gap = rdist + rheight - ldist
                    indent_gaps.append(next_gap)
                    rdist += rheight + spacer_w
                    rslot = rslot.next

        paths.append(generate_vert_spacer(path, indent_gaps, content_width, depth, edge_w, spacer_w))

    # Horizontal spacer generation, they may span multiple columns.
    # Spans should be identified by slots having 'column_span_id' field.
    # Inputs:
    # columns : Tray spec of columns with added information about column spanning slot spacers
    # edge_w : Edge material width, where edge refers to tray edges
    # spacer_w : Spacer material width, where spacer is any component within the tray but not on its edges.
    #
    # Alters:
    # columns[index]['slots'][slot_index]['skip_this'] values in case of column spanning horiz spacers.
    #
    # Returns:
    # spacer_paths : Array of paths to draw
    def generate_horizontal_spacers(columns, edge_width, spacer_width, depth):
        def determine_if_should_indent(slot_index, slots):
            if len(slots)-1 <= slot_index:
                print("Should not run determine_if_should_indent for the last slot in column")
                return False

            slot_above = slots[slot_index]
            slot_below = slots[slot_index+1]

            needs_indent_a = 'needs_indent' in slot_above and slot_above['needs_indent']
            needs_indent_b = 'needs_indent' in slot_below and slot_below['needs_indent']
            forbid_indent_a = 'forbid_indent' in slot_above and slot_above['forbid_indent']
            forbid_indent_b = 'forbid_indent' in slot_below and slot_below['forbid_indent']

            return (needs_indent_a or needs_indent_b) and not (forbid_indent_a or forbid_indent_b)


        spacer_paths = []
        for idx, column in enumerate(columns):
            slots = column['slots']

            l_edge_width = edge_width
            if idx > 0:
                l_edge_width = spacer_width
            r_edge_width = spacer_width

            if len(slots) == 1:
                continue

            for slot_index, slot in enumerate(slots):
                if 'skip_this' in slot:
                    continue
                col_slots = [column['width']]
                spacer_indents = [determine_if_should_indent(slot_index, slots)]
                if 'column_span_id' in slot:
                    csid = slot['column_span_id']
                    for rcolumn in columns[idx+1:-1]:
                        right_slots = list(filter(lambda rslot: 'column_span_id' in rslot
                            and rslot['column_span_id'] == csid, rcolumn['slots']))
                        if len(right_slots) > 0:
                            r_slot = right_slots[0]
                            rslot_index = rcolumn['slots'].index(r_slot)
                            col_slots.append(rcolumn['width'])
                            spacer_indents.append(determine_if_should_indent(rslot_index, rcolumn['slots']))

                            r_slot['skip_this'] = True
                            if rcolumn == columns[-1]:
                                r_edge_width = edge_w  #H-spacer ends up connecting to tray edge.

                spacer_paths.append(generate_horiz_spacer(
                    col_slots,
                    spacer_indents,
                    sum(col_slots) + spacer_w * (len(col_slots)-1),
                    spacer_w,
                    l_edge_width,
                    r_edge_width,
                    depth))
        return spacer_paths

    horiz_paths = generate_horizontal_spacers(columns, edge_w, spacer_w, depth)

    # Loops through an array of arrays of string type svg path parts, composes SVG paths out of them
    # This enables late absolute positioning of elements.
    for path_index, path_parts in enumerate(paths + horiz_paths):
        parts = ['M 0 {}'.format( (depth+5) * path_index)] + path_parts
        element_path = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
        for part in parts:
            element_path.push(part)
        dwg.add(element_path)


def draw_edges(dwg, trayspec):
    paths = generate_edges(dwg, trayspec)
    paths.append(generate_floor(dwg, trayspec, (trayspec['tray_depth']+5)*4))

    for path in paths:
        dwg.add(path)


def finish(dwg):
    dwg.save()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Pass the specs file as the parameter")
        sys.exit(1)

    # TODO: Bring the material specifications from some external source at some point.
    cfg = {
        'spacer_width': 2.5,
        'edge_width': 3.5,
        'spacer_material_width': 400,
        'spacer_material_height': 300,
        'edge_material_width': 400,
        'edge_material_height': 300
    }

    specs = get_specification(sys.argv[1])

    trays = generate_trays_from_spec(cfg['spacer_width'], cfg['edge_width'], specs)

    for tray in trays:
        for column in tray['columns']:
            for slot in column['slots']:
                if 'height' not in slot:
                    slot['height'] = slot['min-height']

        edge_width = tray['edge_width']
        spacer_width = tray['spacer_width']
        tray_name = tray['name']
        dwg = get_drawing('{}-{}.svg'.format(tray_name, edge_width), cfg['edge_material_width'], cfg['edge_material_height'])
        draw_edges(dwg, tray)
        finish(dwg)

        dwg = get_drawing('{}-{}.svg'.format(tray_name, spacer_width), cfg['spacer_material_width'], cfg['spacer_material_height'])
        draw_spacers(dwg, tray)
        finish(dwg)


