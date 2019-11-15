from svgwrite import cm, mm
import svgwrite

exec(open('generate-tray-from-specs.py').read())

STROKE = 0.1


def get_drawing(result_file_name, width='400mm', height='300mm'):
    return svgwrite.Drawing(result_file_name, height=height, width=width, viewBox=(0, 0, 400, 300))

def generate_toothing(direction, path, invert, length, edge_w):
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

        if rot_dir<2 and invert:
            return (0-abs_value)
        elif rot_dir>1 and not invert:
            return (0-abs_value)
        return abs_value


    if length < 30:
        raise Exception("Edge too short for toothing: {}".format(length))

    divisions = int(length / 10)
    if divisions % 2 == 0:
        divisions -= 1
    if divisions > 9:
        divisions = 9
        
    for idx in range(0, divisions):
        if idx % 2 == 0:
            path.push('{} {}'.format(axis(0), dir_value(0, length/divisions)))
        else:
            path.push('{} {}'.format(axis(1), dir_value(1, edge_w)))
            path.push('{} {}'.format(axis(0), dir_value(0, length/divisions)))
            path.push('{} {}'.format(axis(3), dir_value(3, edge_w)))


def generate_edges(dwg, trayspec):
    spacer_w = trayspec['spacer_width']
    edge_w = trayspec['edge_width']
    depth = trayspec['tray_depth']
    #top edge
    INDENT_DEPTH=10
    path = svgwrite.path.Path(stroke='black', stroke_width=STROKE, fill="none")
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

    return [path]


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


