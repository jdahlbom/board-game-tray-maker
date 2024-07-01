import sys

import svg
import tray as gtray
import layout


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

    all_objects = list()
    for tray in trays:
        svg_tray = convert_tray_format(tray)
        edge_width = svg_tray['edge_width']
        spacer_width = svg_tray['spacer_width']
        tray_name = svg_tray['name']

        all_objects.extend(svg.generate_edges(svg_tray))
#        all_objects.extend(svg.generate_floor(svg_tray))
        all_objects.extend(svg.generate_spacers(svg_tray))

    panel_width = cfg['edge_material_width']
    panel_height = cfg['edge_material_height']

    bins = layout.pack_objects(all_objects, panel_width, panel_height)
    game_name = 'should-get-game-name-somewhere'

    for thickness in bins.keys():
        svg.draw_objects(bins[thickness], thickness, game_name, panel_width, panel_height)