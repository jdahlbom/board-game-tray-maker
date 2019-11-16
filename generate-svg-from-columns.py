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

    #Top piece
    path = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
    
   #top edge
    INDENT_DEPTH=10
    path.push('M 0 0')
    width_left = trayspec['tray_width']
    path.push('h {}'.format(edge_w))
    width_left -= edge_w
    for idx, column in enumerate(trayspec['columns']):
        width_left -= column['width']
        path.push('h {}'.format(column['width']))
        if idx < len(trayspec['columns'])-1:
            width_left -= spacer_w
            path.push('v {}'.format(INDENT_DEPTH))
            path.push('h {}'.format(spacer_w))
            path.push('v -{}'.format(INDENT_DEPTH))
    path.push('h {}'.format(edge_w))
    #Right edge
    generate_toothing(1, path, False, depth, edge_w)
    path.push('v {}'.format(edge_w))
    #Bottom edge
    content_width = trayspec['tray_width'] - edge_w*2
    path.push('h -{}'.format(edge_w))
    generate_toothing(2, path, False, content_width, edge_w)
    path.push('h -{}'.format(edge_w))
    #Left edge
    path.push('v -{}'.format(edge_w))
    generate_toothing(3, path, False, depth, edge_w)
    path.push('z')

    #Right piece
    path_r = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
    
   #top edge
    INDENT_DEPTH=10
    path_r.push('M {} {}'.format(edge_w, trayspec['tray_depth']+10))
    content_width = trayspec['tray_height'] - 2*edge_w
    slots = trayspec['columns'][len(trayspec['columns'])-1]['slots']
    print(slots)

    width_left = content_width
    for idx, slot in enumerate(slots):
        height = slot['min-height']
        if 'height' in slot:
            height = slot['height']
        print(slot)
        path_r.push('h {}'.format(height))
        width_left -= height
        if idx < len(slots)-1 or width_left > spacer_w:
            path_r.push('v {}'.format(INDENT_DEPTH))
            path_r.push('h {}'.format(spacer_w))
            path_r.push('v -{}'.format(INDENT_DEPTH))
            width_left -= spacer_w
    if width_left != 0:
        print("Not enough slots content to match whole column")
        path_r.push('h {}'.format(width_left))

    #Right edge
    generate_toothing(1, path_r, True, depth, edge_w)
    path_r.push('v {}'.format(edge_w))
    #Bottom edge
    generate_toothing(2, path_r, False, content_width, edge_w)
    #Left edge
    path_r.push('v -{}'.format(edge_w))
    generate_toothing(3, path_r, True, depth, edge_w)
    path_r.push('z')



    return [path, path_r]


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


