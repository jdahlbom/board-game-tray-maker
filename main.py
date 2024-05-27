import sys

import svg
import tray as gtray


def convert_tray_format(tray):
    for column in tray['columns']:
        for slot_index, slot in enumerate(column['slots']):
            column['slots'][slot_index] = {
                'height': slot['min-height'] + slot['extra-space'],
                'needs_indent': 'needs_indent' in slot and slot['needs_indent'],
                'forbid_intent': 'forbid-intent' in slot and slot['forbid_indent'],
                'label': slot['label']
            }
    return tray


def finish(dwg):
    dwg.save()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: main.py <specsfile.json> [ 'Single tray name']")
        sys.exit(1)

    trayname_arg = None
    if len(sys.argv) == 3:
        trayname_arg = sys.argv[2]

    # TODO: Bring the material specifications from some external source at some point.
    cfg = {
        'spacer_width': 1,
        'edge_width': 3,
    # Board sizes for materials
        'spacer_material_width': 400,
        'spacer_material_height': 300,
        'edge_material_width': 400,
        'edge_material_height': 300
    }

    specs = gtray.get_specification(sys.argv[1])

    trays = gtray.generate_trays_from_spec(cfg['spacer_width'], cfg['edge_width'], specs, trayname_arg)

    for tray in trays:
        svg_tray = convert_tray_format(tray)
        edge_width = svg_tray['edge_width']
        spacer_width = svg_tray['spacer_width']
        tray_name = svg_tray['name']
        dwg = svg.get_drawing('output/{}-{}-edges.svg'.format(tray_name, edge_width), cfg['edge_material_width'], cfg['edge_material_height'])
        svg.draw_edges(dwg, svg_tray)
        finish(dwg)

        dwg = svg.get_drawing('output/{}-{}-spacers.svg'.format(tray_name, spacer_width), cfg['spacer_material_width'], cfg['spacer_material_height'])
        svg.draw_spacers(dwg, svg_tray)
        finish(dwg)


