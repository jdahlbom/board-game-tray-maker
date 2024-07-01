import svgwrite

# Hairline stroke (Cutting) for Epilog printers is 0.001"
STROKE = 0.001
MIN_TOOTH_WIDTH = 7.0
INDENT_DEPTH = 10
KERF = 0.2
K_CORR = KERF/2.0

DPI = 96 # Assumed DPI used by CorelDraw
INCHES_PER_MM = 1.0 / 25.4
DPI_CONVERSION = INCHES_PER_MM * DPI # Conversion rate is 3.77953

ENABLE_DRAW_BOUNDING_BOX = False

# When returning array of SVG draw instructions from a function, there
# should also be following information included in the top level:
# { "svg": [drawing instructions],
#   "nested_objects": [ {
#       "svg": [ as above ],
#       "offset_x": numeric offset relative to parent object
#       "offset_y": numeric offset relative to parent object
#   }],
#   "width": number,
#   "height", number,
#   "offset_x": number, Offset of starting point relative to origin of "bounding box"
#   "offset_y": numbre, offset of starting point relative to origin of "bounding box"
#   "tray_id": alphanumeric,
#   "thickness": number }


def mm(value):
    return '{}mm'.format(value)


def get_drawing(result_file_name, width, height):
    return svgwrite.Drawing(
            filename=result_file_name, 
            size=(f"{width}mm", f"{height}mm"),
            viewBox=(0, 0, width * DPI_CONVERSION, height * DPI_CONVERSION))


def kerf_correct_corner(corner_index):
    if corner_index == 0:
        return 'h {}'.format(K_CORR)
    elif corner_index == 1:
        return 'h {} v {}'.format(K_CORR, K_CORR)
    elif corner_index == 2:
        return 'v {} h -{}'.format(K_CORR, K_CORR)
    elif corner_index == 3:
        return f"h -{K_CORR} v -{K_CORR}"
    elif corner_index == 4:
        return f"v {-K_CORR}"


def generate_toothing(direction, invert, length, tooth_depth):
    #Directions:
    #0 - right
    #1 - down
    #2 - left
    #3 - up
    # Returns a list of string svg commands

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

    if length / MIN_TOOTH_WIDTH < 3.0:
        raise Exception("Edge too short for toothing: {}".format(length))

    divisions = int(length / 10.0)
    if divisions % 2 == 0:
        divisions -= 1
    if divisions > 9:
        divisions = 9
    if divisions == 1:
        divisions = 3
    tooth_width = length / divisions

    p = []
    for idx in range(0, divisions):
        kerf_correction = 2 * K_CORR
        if idx == 0 or idx == divisions-1:
            kerf_correction = K_CORR
        if invert:
            kerf_correction = -kerf_correction
        if idx % 2 == 0:
            p.append('{} {}'.format(axis(0), dir_value(0, tooth_width+kerf_correction)))
        else:
            p.append('{} {}'.format(axis(1), dir_value(1, tooth_depth)))
            p.append('{} {}'.format(axis(0), dir_value(0, tooth_width-kerf_correction)))
            p.append('{} {}'.format(axis(3), dir_value(3, tooth_depth)))
    return p


def generate_slotted_top_edge(slots, spacer_width, content_width, corner_toothing, edge_width, depth):
    def should_create_sloped_indent(slot, margin):
        return 'slot_properties' in slot and \
               'needs_indent' in slot['slot_properties'] and \
               slot['slot_properties']['needs_indent'] and \
               slot['length'] > (30.0 + 2 * margin)

    path_parts = []
    if corner_toothing:
        path_parts.append('h {}'.format(edge_width))

    width_left = content_width
    for idx, slot in enumerate(slots):
        slot_length = slot['length']
        width_left -= slot_length
        margin = 5.0
        if should_create_sloped_indent(slot, margin):
            path_parts.append('h {}'.format(margin))
            path_parts = path_parts + cubic_sloped_indent(slot_length-2*margin, slot_length-20.0-2*margin, depth/2.0)
            path_parts.append('h {}'.format(margin))
        else:
            path_parts.append('h {}'.format(slot_length))
        if idx < len(slots)-1:
            width_left -= spacer_width
            path_parts.append('h {}'.format(K_CORR))
            path_parts.append('v {}'.format(INDENT_DEPTH - K_CORR))
            path_parts.append('h {}'.format(spacer_width - K_CORR*2))
            path_parts.append('v -{}'.format(INDENT_DEPTH - K_CORR))
            path_parts.append('h {}'.format(K_CORR))

    if width_left > 0.1:
        print("[WARN] Edge width unused for slots: {} , extending by that much!".format(width_left))
        path_parts.append('h {}'.format(width_left))

    if corner_toothing:
        path_parts.append('h {}'.format(edge_width))

    return path_parts


# Generates single edge "wall" piece
def generate_edge(slots, spacer_width, content_width, corner_toothing, edge_width, depth):
    path_parts = []
    # Top edge
    path_parts.append(kerf_correct_corner(0))
    path_parts.extend(generate_slotted_top_edge(slots, spacer_width, content_width, corner_toothing, edge_width, depth))

    # Right edge
    path_parts.append(kerf_correct_corner(1))
    path_parts.extend(generate_toothing(1, not corner_toothing, depth, edge_width))
    path_parts.append('v {}'.format(edge_width))

    # Bottom edge
    path_parts.append(kerf_correct_corner(2))
    if corner_toothing:
        path_parts.append('h -{}'.format(edge_width))

    path_parts.extend(generate_toothing(2, False, content_width, edge_width))

    if corner_toothing:
        path_parts.append('h -{}'.format(edge_width))

    path_parts.append(kerf_correct_corner(3))

    # Left edge
    path_parts.append('v -{}'.format(edge_width))
    path_parts.extend(generate_toothing(3, not corner_toothing, depth, edge_width))

    path_parts.append(kerf_correct_corner(4))
    path_parts.append('z')

    offset_x = 0
    if not corner_toothing:
        offset_x = edge_width
    return {
        'svg': path_parts,
        'width': content_width + 2 * edge_width,
        'height': depth + edge_width,
        'offset_x': offset_x,
        'offset_y': 0,
        'thickness': edge_width
    }


def generate_edges(trayspec):
    spacer_w = trayspec['spacer_width']
    edge_w = trayspec['edge_width']
    depth = trayspec['tray_depth']

    content_width = trayspec['tray_width']-edge_w*2
    content_height = trayspec['tray_height']-edge_w*2

    #Top wall
    horiz_slots_and_widths = list(map(lambda column: {'length': column['width'], 'slot_properties': column['slots'][0]}, trayspec['columns']))
    paths = []
    paths.append( generate_edge(
        horiz_slots_and_widths,
        spacer_w, 
        content_width, 
        True,
        edge_w,
        depth) )

    #Right wall
    def slots_from_column(column_slots):
        return list([{'length': slot['height'], 'slot_properties': slot} for slot in column_slots])

    slot_widths = slots_from_column(trayspec['columns'][-1]['slots'])
    paths.append( generate_edge(
        slot_widths, 
        spacer_w, 
        content_height, 
        False,
        edge_w,
        depth) )
    
    #Bottom wall
    horiz_slot_width_sum = sum([slot['length'] for slot in horiz_slots_and_widths])
    if horiz_slot_width_sum + spacer_w * (len(horiz_slots_and_widths)-1) < content_width:
        print("Too little column content, appending empty")
        empty_space = content_width - sum(horiz_slot_width_sum) - spacer_w*len(horiz_slots_and_widths)
        horiz_slots_and_widths.append({'length': empty_space, 'slot_properties': {}})

    paths.append(generate_edge(
        horiz_slots_and_widths[::-1],
        spacer_w,
        content_width,
        True,
        edge_w,
        depth))

    #Left wall
    slots = slots_from_column(trayspec['columns'][0]['slots'])

    paths.append(generate_edge(
        slots[::-1],
        spacer_w,
        content_height,
        False,
        edge_w,
        depth))

    for idx, svg_path in enumerate(paths):
        paths[idx]['tray'] = trayspec['name']
    return paths
    # svg_paths.append(old_write_svg(path_parts, v_offset, corner_toothings[idx]))


def spacer_floor_hole_positioning(height):
    hole_width = MIN_TOOTH_WIDTH
    if height/hole_width < 3:
        return [height]

    num_tooth = 1
    if height/hole_width > 5:
        num_tooth = 2

    tooth_spacing = (height - num_tooth * hole_width) / (num_tooth + 1)
    positions = list()
    for index in range(num_tooth * 2 + 1):
        if index % 2 == 0:
            positions.append(tooth_spacing)
        else:
            positions.append(hole_width)
    return positions


def generate_floor(trayspec):
    edge_w = trayspec['edge_width']
    spacer_w = trayspec['spacer_width']
    width = trayspec['tray_width'] - edge_w*2
    height = trayspec['tray_height'] - edge_w*2

    p = []
    p.append(kerf_correct_corner(0))
    p.extend(generate_toothing(0, True, width, edge_w))
    p.append(kerf_correct_corner(1))
    p.extend(generate_toothing(1, True, height, edge_w))
    p.append(kerf_correct_corner(2))
    p.extend(generate_toothing(2, True, width, edge_w))
    p.append(kerf_correct_corner(3))
    p.extend(generate_toothing(3, True, height, edge_w))
    p.append(kerf_correct_corner(4))
    p.append('z')

    def generate_internal_holes():
        col_widths = list(map(lambda col: col['width'], trayspec['columns']))
        positions = spacer_floor_hole_positioning(height)
        hole_svgs = []

        if len(positions) == 1:
            return hole_svgs

        for idx, col_w in enumerate(col_widths[0:-1]):
            h_offset = sum(col_widths[0:idx+1]) + idx * spacer_w
            for index, position_length in enumerate(positions):
                if index % 2 == 0:
                    continue
                parts = list()
                v_offset = sum(positions[0:index])
                parts.append('m {} {}'.format(K_CORR, K_CORR))
                parts.append('h {}'.format(spacer_w - K_CORR*2))
                parts.append('v {}'.format(position_length - K_CORR*2))
                parts.append('h -{}'.format(spacer_w - K_CORR*2))
                parts.append('v -{}'.format(position_length - K_CORR*2))
                parts.append('z')
                hole_svgs.append({
                    'svg': parts,
                    'offset_x': h_offset,
                    'offset_y': v_offset
                })
        return hole_svgs

    nested_objects = generate_internal_holes()
    return {
        'svg': p,
        'nested_objects': nested_objects,
        'width': width + 2 * edge_w,
        'height': height + 2 * edge_w,
        'offset_x': edge_w,
        'offset_y': edge_w,
        'thickness': edge_w,
        'tray': trayspec['name']
    }


def generate_vert_spacer(indent_spaces, content_width, depth, edge_width, spacer_width):
    path_parts = [ kerf_correct_corner(0)]
    path_parts.extend(generate_slotted_top_edge(indent_spaces, spacer_width, content_width, True, edge_width, depth))
    path_parts.append(kerf_correct_corner(1))

    path_parts.append('v {}'.format(INDENT_DEPTH))
    path_parts.append(kerf_correct_corner(2))
    path_parts.append('h -{}'.format(edge_width))
    path_parts.append('v {}'.format(depth - INDENT_DEPTH))

    def generate_floor_teeth(width, edge_w):
        p = []
        positions = spacer_floor_hole_positioning(width)
        if len(positions) == 1:
            return [f"h -{positions[0]}"]

        for index, position_length in enumerate(positions):
            kerf_correction = K_CORR
            if index == 3 and len(positions) == 5:
                kerf_correction = 2 * K_CORR

            if index % 2 == 0:
                p.append(f"h -{position_length - kerf_correction}")
            else:
                p.append('v {}'.format(edge_w + K_CORR))
                p.append('h -{}'.format(position_length + K_CORR*2))
                p.append('v -{}'.format(edge_w + K_CORR))
        return p

    path_parts = path_parts + generate_floor_teeth(content_width, edge_width)
    path_parts.append('v -{}'.format(depth - INDENT_DEPTH))
    path_parts.append('h -{}'.format(edge_width))
    path_parts.append(kerf_correct_corner(3))
    path_parts.append('v -{}'.format(INDENT_DEPTH))
    path_parts.append(kerf_correct_corner(4))
    path_parts.append('z')

    positions_for_height = spacer_floor_hole_positioning(content_width)
    height_from_teeth = edge_width + K_CORR
    if len(positions_for_height) == 1:
        height_from_teeth = 0
    spacer_object = {
        'svg': path_parts,
        'width': content_width + 2 * edge_width + 2 * K_CORR,
        'height': depth + 2 * K_CORR + height_from_teeth,
        'offset_x': 0,
        'offset_y': 0,
        'thickness': spacer_width
    }
    return spacer_object


# Generates SVG string path parts to draw a single horizontal spacer.
# Horizontal spacer may span multiple columns.
# This function is not aware of the column specifications, merely the drawing element inputs

# Returns: Array of SVG path strings.
def generate_horiz_spacer(col_widths, spacer_indents, content_width, spacer_width, l_edge_width, r_edge_width, depth):
    path_parts = []
    path_parts.append('h {}'.format(l_edge_width + K_CORR))
    if len(list(filter(lambda spacer: spacer, spacer_indents))) > 0:
        margin = 5.0
        for idx, slot_width in enumerate(col_widths):
            if spacer_indents[idx]:
                # TODO: Duplicate code, should refactor to single function call
                path_parts.append('h {}'.format(margin))
                path_parts = path_parts + cubic_sloped_indent(slot_width-2*margin, slot_width-20.0-2*margin, depth/2.0)
                path_parts.append('h {}'.format(margin))
            else:
                path_parts.append('h {}'.format(col_widths[idx]))
            if idx < len(col_widths)-1:
                path_parts.append('h {}'.format(spacer_width))
    else:
        path_parts.append('h {}'.format(content_width))
    path_parts.append('h {}'.format(r_edge_width + K_CORR))

    path_parts.append('v {}'.format(INDENT_DEPTH + K_CORR*2))
    path_parts.append('h -{}'.format(r_edge_width))
    path_parts.append('v {}'.format(depth - INDENT_DEPTH))

    #Bottom with indent slots
    for idx, slot_width in enumerate(col_widths[::-1]):
        path_parts.append('h -{}'.format(slot_width + K_CORR*2))
        if idx != len(col_widths)-1:
            path_parts.append('v -{}'.format(depth-INDENT_DEPTH - K_CORR))
            path_parts.append('h -{}'.format(spacer_width - K_CORR*2))
            path_parts.append('v {}'.format(depth-INDENT_DEPTH - K_CORR))

    path_parts.append('v -{}'.format(depth-INDENT_DEPTH))
    path_parts.append('h -{}'.format(l_edge_width))
    path_parts.append('v -{}'.format(INDENT_DEPTH + K_CORR*2))
    path_parts.append('z')
    spacer_object = {
        'svg': path_parts,
        'width': l_edge_width + sum(col_widths) + spacer_width * (len(col_widths) -1) + r_edge_width + 2 * K_CORR,
        'height': depth + 2 * K_CORR,
        'offset_x': 0,
        'offset_y': 0,
        'thickness': spacer_width
    }
    return spacer_object


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


def create_vertical_spacer_combined_slot_list(columns, spacer_w):
    spacer_indent_lists = []

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
                    lslot()['col_span_id'] == rslot()['col_span_id']):
                ldist = 0
                rdist = 0
                indent_gaps.append({'length': lheight})
                lslot = lslot.next
                rslot = rslot.next
            else:
                if ldist + lheight < rdist + rheight:
                    if ldist < rdist:
                        next_gap = ldist + lheight - rdist
                        indent_gaps.append({'length': next_gap})
                    else:
                        indent_gaps.append({'length': lheight})
                    ldist += lheight + spacer_w
                    lslot = lslot.next
                else:
                    if rdist < ldist:
                        next_gap = rdist + rheight - ldist
                        indent_gaps.append({'length': next_gap})
                    else:
                        indent_gaps.append({'length': rheight})
                    rdist += rheight + spacer_w
                    rslot = rslot.next
        # For last slots, use the smaller slot
        lheight = lslot()['height']
        rheight = rslot()['height']
        if lheight <= rheight:
            indent_gaps.append({'length': lheight})
        else:
            indent_gaps.append({'length': rheight})

        spacer_indent_lists.append(indent_gaps)
    return spacer_indent_lists


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

    spacer_objects = []
    for idx, column in enumerate(columns):
        slots = column['slots']

        l_edge_width = edge_width
        r_edge_width = edge_width
        if idx > 0:
            l_edge_width = spacer_width
        if idx < len(columns)-1:
            r_edge_width = spacer_width

        if len(slots) == 1:
            continue

        for slot_index, slot in enumerate(slots):
            # Don't generate end spacer for the last slot of column.
            if slot_index == len(slots)-1:
                continue
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
                            r_edge_width = edge_width  #H-spacer ends up connecting to tray edge.

            spacer_objects.append(generate_horiz_spacer(
                col_slots,
                spacer_indents,
                sum(col_slots) + spacer_width * (len(col_slots)-1),
                spacer_width,
                l_edge_width,
                r_edge_width,
                depth))
    return spacer_objects


def generate_spacers(trayspec):
    columns = trayspec['columns']
    spacer_w = trayspec['spacer_width']
    edge_w = trayspec['edge_width']
    depth = trayspec['tray_depth']
    content_width = trayspec['tray_height'] - 2 * edge_w

    spacer_indent_gaps = create_vertical_spacer_combined_slot_list(columns, spacer_w)

    paths = []  # List of lists of strings. Each list of strings contains the svg vector path for a object
    for gaps in spacer_indent_gaps:
        paths.append(generate_vert_spacer(gaps, content_width, depth, edge_w, spacer_w))

    horiz_paths = generate_horizontal_spacers(columns, edge_w, spacer_w, depth)

    spacer_objects = paths + horiz_paths
    for idx in range(len(spacer_objects)):
        spacer_objects[idx]['tray'] = trayspec['name']
    return spacer_objects


def draw_spacers(dwg, trayspec):
    spacer_objects = generate_spacers(trayspec)

    # Loops through an array of arrays of string type svg path parts, composes SVG paths out of them
    # This enables late absolute positioning of elements.
    padding = 1
    cumulative_v_offset = 0
    for spacer_obj in spacer_objects:
        parts = [f"M {padding} {cumulative_v_offset + padding}"] + spacer_obj['svg']
        cumulative_v_offset += spacer_obj['height'] + padding
        element_path = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
        for part in parts:
            element_path.push(part)
        dwg.add(element_path)


def draw_edges(dwg, trayspec):
    object_padding = 1
    # This old method of drawing objects without layout is kept here for visual debugging for now.
    # Should be replaced with entirely separate layout package

    def old_write_svg(path_object, v_offset, padding):
        path = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
        path.push(f"M {path_object['offset_x'] + padding} {path_object['offset_y'] + padding + v_offset}")
        for part in path_object['svg']:
            path.push(part)
        return path

    svg_objects = generate_edges(trayspec)

    paths = []
    cumulative_v_offset = 0
    for svg_part in svg_objects:
        paths.append(old_write_svg(svg_part, cumulative_v_offset, object_padding))
        cumulative_v_offset += svg_part['height'] + 2 * object_padding

    floor_object = generate_floor(trayspec)
    paths.append(old_write_svg(floor_object, cumulative_v_offset, object_padding))
    for nested_part in floor_object['nested_objects']:
        nested_part['offset_x'] += floor_object['offset_x']
        nested_part['offset_y'] += floor_object['offset_y']
        paths.append(old_write_svg(nested_part, cumulative_v_offset, object_padding))

    for path in paths:
        dwg.add(path)


def get_bounding_box_path(svg_obj):
    path = svgwrite.path.Path(stroke='red', stroke_width=0.2, fill='none')
    offset_x = svg_obj['packer_offset_x']
    offset_y = svg_obj['packer_offset_y']
    path.push(f"M {offset_x} {offset_y}")
    path.push(f"h {svg_obj['width']}")
    path.push(f"v {svg_obj['height']}")
    path.push(f"h -{svg_obj['width']}")
    path.push(f"v -{svg_obj['height']}")
    path.push('z')
    return path


def draw_objects(objects_in_bins, thickness, identifier, panel_width, panel_height):
    for bin_id in objects_in_bins.keys():
        file_name = f"output/{identifier}-{thickness}-panel-{bin_id+1}.svg"
        dwg = get_drawing(file_name, panel_width, panel_height)

        for svg_obj in objects_in_bins[bin_id]:
            path = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
            offset_x = svg_obj['offset_x'] + svg_obj['packer_offset_x']
            offset_y = svg_obj['offset_y'] + svg_obj['packer_offset_y']
            path.push(f"M {offset_x} {offset_y}")
            for part in svg_obj['svg']:
                path.push(part)
            if 'nested_objects' in svg_obj:
                for nested in svg_obj['nested_objects']:
                    path.push(f"M {offset_x + nested['offset_x']} {offset_y + nested['offset_y']}")
                    for part in nested['svg']:
                        path.push(part)

            dwg.add(path)
            if ENABLE_DRAW_BOUNDING_BOX:
                dwg.add(get_bounding_box_path(svg_obj))
        dwg.save()
        print(f"Generated {file_name}")

