from svgwrite import cm, mm
import svgwrite

exec(open('generate-tray-from-specs.py').read())


def get_drawing(result_file_name, width='400mm', height='300mm'):
    return svgwrite.Drawing(result_file_name, height=height, width=width, viewBox=(0, 0, 400, 300))


def draw(dwg, columns):
    path = svgwrite.path.Path(stroke='black', stroke_width=0.01, fill="none")
    path.push('M 1 3')
    path.push('h 3')
    path.push('v 2')
    path.push('h 3')
    path.push('v -2')
    path.push('h 3')
    path.push('v 3')
    path.push('z')
    dwg.add(path)


def finish(dwg):
    dwg.save()


if __name__ == '__main__':
    tray_defs = generate_columns_from_spec(spacer_width=2, edge_width=3.5, specsfile=sys.argv[1])
    print(tray_defs)

    dwg = get_drawing('test-drawing.svg')
    draw(dwg, columns)
    finish(dwg)


