import yaml
import json
import sys

def read_box_layout(filename):
    box_config = dict()
    with open(filename) as stream:
        box_config = yaml.safe_load(stream)
    stream.close()
    print(box_config)
    return box_config


def read_tray_layout(filename):
    tray_config = dict()
    with open(filename) as stream:
        tray_config = json.load(stream)
    return tray_config


def validate_card_column_temp(box, trays):
    edge_width = box['edge-width']
    card_column = box['columns'][2]
    assert(card_column['width'] >= (92 + 2 * edge_width))


if __name__ == '__main__':
    box_file = sys.argv[1]
    tray_file = sys.argv[2]
    print(box_file, tray_file)
    box = read_box_layout(box_file)
    tray = read_tray_layout(tray_file)
    validate_card_column_temp(box, tray)