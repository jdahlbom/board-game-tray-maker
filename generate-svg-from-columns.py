from svgwrite import cm, mm
import svgwrite

exec(open('generate-tray-from-specs.py').read())

STROKE = 0.1
MIN_TOOTH_WIDTH = 10

def get_drawing(result_file_name, width='400mm', height='300mm'):
    return svgwrite.Drawing(result_file_name, height=height, width=width, viewBox=(0, 0, 400, 300))

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


def generate_edges(dwg, trayspec):
    spacer_w = trayspec['spacer_width']
    edge_w = trayspec['edge_width']
    depth = trayspec['tray_depth']
    INDENT_DEPTH=10
 
    def generate_edge(slot_widths, spacer_width, content_width, corner_toothing, edge_width, v_offset):
        path = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
        if corner_toothing:
            path.push('M 0 {}'.format(v_offset))
            path.push('h {}'.format(edge_width))
        else:
            path.push('M {} {}'.format(edge_width, v_offset))

        width_left = content_width
        for idx, slot in enumerate(slot_widths):
            width_left -= slot
            path.push('h {}'.format(slot))
            if idx < len(slot_widths)-1 or width_left > spacer_width:
                width_left -= spacer_width
                path.push('v {}'.format(INDENT_DEPTH))
                path.push('h {}'.format(spacer_width))
                path.push('v -{}'.format(INDENT_DEPTH))

        if width_left > 0:
            print("[WARN] Edge width unused for slots: {} , extending by that much!".format(width_left))
            path.push('h {}'.format(width_left))

        if corner_toothing:
            path.push('h {}'.format(edge_width))
            #Right edge
            generate_toothing(1, path, False, depth, edge_width)
        else:
            generate_toothing(1, path, True, depth, edge_width)
        path.push('v {}'.format(edge_width))
        #Bottom edge
        
        if corner_toothing:
            path.push('h -{}'.format(edge_w))
        generate_toothing(2, path, False, content_width, edge_width)

        if corner_toothing:
            path.push('h -{}'.format(edge_w))
        #Left edge
        path.push('v -{}'.format(edge_w))

        if corner_toothing:
            generate_toothing(3, path, False, depth, edge_width)
        else:
            generate_toothing(3, path, True, depth, edge_width)
        path.push('z')
        return path


    content_width = trayspec['tray_width']-edge_w*2
    content_height = trayspec['tray_height']-edge_w*2
    #Top edge
    horiz_slot_widths = list(map(lambda column: column['width'], trayspec['columns']))
    paths = []
    paths.append( generate_edge(
        horiz_slot_widths, 
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

        return list(map(get_height, column_slots))

    slot_widths = slots_from_column(trayspec['columns'][-1]['slots'])
    paths.append( generate_edge(
        slot_widths, 
        spacer_w, 
        content_height, 
        False, 
        edge_w, 
        (depth + 5)*1) )
    
    #Bottom edge
    if sum(horiz_slot_widths) + spacer_w * (len(horiz_slot_widths)-1) < content_width:
        print("Too little column content, appending empty")
        horiz_slot_widths.append(content_width - sum(horiz_slot_widths) - spacer_w*len(horiz_slot_widths))

    paths.append (generate_edge(
        horiz_slot_widths[::-1],
        spacer_w,
        content_width,
        True,
        edge_w,
        (depth + 5)*2) )

    #Left edge
    slot_widths = slots_from_column(trayspec['columns'][0]['slots'])
    if sum(slot_widths) + spacer_w*(len(slot_widths)-1) < content_height:
        print("Too little column content, appending empty")
        slot_widths.append(content_height - sum(slot_widths) - spacer_w*(len(slot_widths)))
    
    paths.append(generate_edge(
        slot_widths[::-1],
        spacer_w,
        content_height,
        False,
        edge_w,
        (depth + 5)*3) )

    return paths


def draw(dwg, trayspec):
    paths = generate_edges(dwg, trayspec)

    for path in paths:
        dwg.add(path)


def finish(dwg):
    dwg.save()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Pass the specs file as the parameter")
        sys.exit(1)

    tray_defs = generate_columns_from_spec(spacer_width=2, edge_width=3.5, specsfile=sys.argv[1])

    dwg = get_drawing('test-drawing.svg')
    draw(dwg, tray_defs)
    finish(dwg)


