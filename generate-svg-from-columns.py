from svgwrite import cm, mm
import svgwrite

exec(open('generate-tray-from-specs.py').read())

STROKE = 0.1


def get_drawing(result_file_name, width='400mm', height='300mm'):
    return svgwrite.Drawing(result_file_name, height=height, width=width, viewBox=(0, 0, 400, 300))


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
    path.push('v {}'.format(depth/3))
    path.push('h -{}'.format(edge_w))
    path.push('v {}'.format(depth/3))
    path.push('h {}'.format(edge_w))
    path.push('v {}'.format(depth/3))
    path.push('v {}'.format(edge_w))
    #Bottom edge
    path.push('h -{}'.format(trayspec['tray_width']))
    #Left edge
    path.push('v -{}'.format(edge_w))
    path.push('v -{}'.format(depth/3))
    path.push('h {}'.format(edge_w))
    path.push('v -{}'.format(depth/3))
    path.push('h -{}'.format(edge_w))
    path.push('v -{}'.format(depth/3))
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
    print(tray_defs)

    dwg = get_drawing('test-drawing.svg')
    draw(dwg, tray_defs)
    finish(dwg)


