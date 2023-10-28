import sys

import svg
import tray as gtray


def finish(dwg):
    dwg.save()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Pass the specs file as the parameter")
        sys.exit(1)

    # TODO: Bring the material specifications from some external source at some point.
    cfg = {
        'spacer_width': 3,
        'edge_width': 3,
        'spacer_material_width': 400,
        'spacer_material_height': 300,
        'edge_material_width': 400,
        'edge_material_height': 300
    }

    specs = gtray.get_specification(sys.argv[1])

    trays = gtray.generate_trays_from_spec(cfg['spacer_width'], cfg['edge_width'], specs)

    for tray in trays:
        for column in tray['columns']:
            for slot in column['slots']:
                if 'height' not in slot:
                    slot['height'] = slot['min-height']

        edge_width = tray['edge_width']
        spacer_width = tray['spacer_width']
        tray_name = tray['name']
        dwg = svg.get_drawing('output/{}-{}-edges.svg'.format(tray_name, edge_width), cfg['edge_material_width'], cfg['edge_material_height'])
        svg.draw_edges(dwg, tray)
        finish(dwg)

        dwg = svg.get_drawing('output/{}-{}-spacers.svg'.format(tray_name, spacer_width), cfg['spacer_material_width'], cfg['spacer_material_height'])
        svg.draw_spacers(dwg, tray)
        finish(dwg)


