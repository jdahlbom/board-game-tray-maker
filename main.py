import sys

import svg
import tray as gtray
import layout
import yaml


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
    with open('config.yaml') as stream:
        config = yaml.safe_load(stream)

    cfg = dict()
    cfg['edge_width'] = config['edge_material']['thickness']
    cfg['spacer_width'] = config['spacer_material']['thickness']

    def get_material_kerfs(config):
        materials = config['material_kerf']
        edge_material = config['edge_material']['material']
        edge_thickness = config['edge_material']['thickness']
        spacer_material = config['spacer_material']['material']
        spacer_thickness = config['spacer_material']['thickness']

        def get_closest(material_kerfs, thickness):
            material_keys = material_kerfs.keys()
            mkeys = [float(key) for key in material_keys]
            closest_thickness = min(mkeys, key=lambda x: abs(x - thickness))
            return material_kerfs[int(closest_thickness)]

        edge_kerf = get_closest(materials[edge_material], edge_thickness)
        spacer_kerf = get_closest(materials[spacer_material], spacer_thickness)
        return edge_kerf, spacer_kerf

    kerfs = get_material_kerfs(config)
    cfg['edge_kerf'] = kerfs[0]
    cfg['spacer_kerf'] = kerfs[1]

    specs = gtray.get_specification(sys.argv[1])

    trays = gtray.generate_trays_from_spec(cfg['spacer_width'], cfg['edge_width'], specs, trayname_arg)

    all_objects = list()
    for tray in trays:
        svg_tray = convert_tray_format(tray)
        edge_width = svg_tray['edge_width']
        spacer_width = svg_tray['spacer_width']
        tray_name = svg_tray['name']

        Svg = svg.Svg(cfg['edge_kerf'], cfg['spacer_kerf'])

        all_objects.extend(Svg.generate_edges(svg_tray))
        all_objects.append(Svg.generate_floor(svg_tray))
        all_objects.extend(Svg.generate_spacers(svg_tray))

    panel_width = config['edge_material']['default_sizes']['width'] - 2 * svg.OUTLINE_MARGIN
    panel_height = config['edge_material']['default_sizes']['height'] - 2 * svg.OUTLINE_MARGIN

    bins = layout.pack_objects(all_objects, panel_width, panel_height)
    game_name = 'game-name'

    for thickness in bins.keys():
        svg.draw_objects(bins[thickness], thickness, game_name, panel_width, panel_height)