from traymaker_logic import TrayLaserCut
import gloomhaven
import json

options = {
    "unit": "mm",
    "uconv": 1,
    "nomTab": 4,
    "spacing": 1,
    "kerf": 0.1,
    "empty_space": 1,
    "clearance": 0.1,
    "cut_length": 5,
    "gap_length": 2,
    "sep_distance": 1,
    "indentradius": 0
}

opposite_piece = {
    "thickness": 3
}

def mock_vdivider():
    return {
        "name": "3 full v-divider",
        "width": 116,
        "height": 12,
        "thickness": 2,
        "edges": [
            {
                "rotation": 0,
                "depth": 12,
                "parts": [
                    {
                        "tabs": "TOP",
                        "length": 116
                    }
                ],
            },
            {
                "rotation": 1,
                "opposite": opposite_piece,
                "parts": [
                    {
                        "tabs": "START_HALF_TAB",
                        "length": 12
                    }
                ]
            },
            {
                "rotation": 2,
                "opposite": opposite_piece,
                "parts": [
                    {
                        "tabs": "FEMALE",
                        "length": 116
                    }
                ]
            },
            {
                "rotation": 3,
                "opposite": opposite_piece,
                "parts": [
                    {
                        "tabs": "END_HALF_TAB",
                        "length": 12
                    }
                ]
            }
        ],
    }

def error_print(msg):
    print(msg)


def test_effects_tray_syntax_works():
    for trayname in ["effects", "small_terrain", "large_terrain", "monsters", "monster_cards", "event_cards"]:
        pieces = gloomhaven.tray_setup(trayname, error_print)
        lasercut = TrayLaserCut(options, error_print)
        cmds = lasercut.draw(pieces, 3)


def test_vdivider():
    pieces = [ mock_vdivider() ]
    lasercut = TrayLaserCut(options, error_print)
    cmds = lasercut.draw(pieces, 2)
    tw = 116 / 9.0
    cmds = cmds[0]["cut"]
    assert(len(cmds) == 4)
    assert(cmds[0] == 'M 1 1 l 122 0 ')
    assert(cmds[1] == 'M 123 1 l 0 6.0 l -3 0 l 0 6.0 ')
    assert(cmds[2] == 'M 120 13 ' +
            'l {} 0 l 0 3 l {} 0 l 0 -3 '.format(-tw, -tw) +
            'l {} 0 l 0 3 l {} 0 l 0 -3 '.format(-tw, -tw) +
            'l {} 0 l 0 3 l {} 0 l 0 -3 '.format(-tw, -tw) +
            'l {} 0 l 0 3 l {} 0 l 0 -3 '.format(-tw, -tw) +
            'l {} 0 '.format(-tw))


if __name__ == "__main__":
    test_effects_tray_syntax_works()