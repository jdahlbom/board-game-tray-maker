from traymaker_logic import TrayLaserCut
import re

def mocked_unitfunc(unitstr):
    exp = re.compile(r'^([0-9]*)[^0-9]*$')
    matches = exp.match(unitstr)
    return 1


options = {
    "X": 10,
    "Y": 20,
    "Z": 30,
    "unit": "mm",
    "thickness": 3,
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

def mock_square(side):
    X = side
    Y = side
    return [{
        "width": X,
        "length": Y,
        "offset": (0,0),
        "edges": [
            {
                "parts": [
                    {"tabs": "TOP", "length": X}
                ],
                "translation": (0, 0),
                "rotation": 0,
                "depth": Y
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": Y}
                ],
                "translation": (X, 0),
                "rotation": 1,
                "depth": X
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": X}
                ],
                "translation": (X, Y),
                "rotation": 2,
                "depth": Y
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": Y}
                ],
                "translation": (0, Y),
                "rotation": 3,
                "depth": X
            }
        ]
    }]


def mock_female_edge(x=20, y=12):
    single_edge_piece = [{
        "width": x,
        "length": y,
        "offset": (0,0),
        "edges": [
            {
                "parts": [
                    {"tabs": "FEMALE", "length": x}
                ],
                "translation": (0, 0),
                "rotation": 0,
                "depth": y
            },
            {
                "parts": [
                    {"tabs": "FEMALE", "length": y}
                ],
                "translation": (x, 0),
                "rotation": 1,
                "depth": x
            }
        ]
    }]
    return single_edge_piece


def mock_female_male_edge(x, y):
    single_edge_piece = [{
        "width": x,
        "length": y,
        "offset": (0, 0),
        "edges": [
            {
                "parts": [
                    {"tabs": "FEMALE", "length": x}
                ],
                "translation": (0, 0),
                "rotation": 0,
                "depth": y
            },
            {
                "parts": [
                    {"tabs": "MALE", "length": y}
                ],
                "translation": (x, 0),
                "rotation": 1,
                "depth": x
            }
        ]
    }]
    return single_edge_piece


def mock_male_male_edge(x, y):
    single_edge_piece = [{
        "width": x,
        "length": y,
        "offset": (0, 0),
        "edges": [
            {
                "parts": [
                    {"tabs": "MALE", "length": x}
                ],
                "translation": (0, 0),
                "rotation": 0,
                "depth": y
            },
            {
                "parts": [
                    {"tabs": "MALE", "length": y}
                ],
                "translation": (x, 0),
                "rotation": 1,
                "depth": x
            }
        ]
    }]
    return single_edge_piece


def mock_top_male_edge(x, y):
    single_edge_piece = [{
        "width": x,
        "length": y,
        "offset": (0, 0),
        "edges": [
            {
                "parts": [
                    {"tabs": "TOP", "length": x}
                ],
                "translation": (0, 0),
                "rotation": 0,
                "depth": y
            },
            {
                "parts": [
                    {"tabs": "MALE", "length": y}
                ],
                "translation": (x, 0),
                "rotation": 1,
                "depth": x
            }
        ]
    }]
    return single_edge_piece


def mock_top_female_edge(x, y):
    single_edge_piece = [{
        "width": x,
        "length": y,
        "offset": (0, 0),
        "edges": [
            {
                "parts": [
                    {"tabs": "TOP", "length": x}
                ],
                "translation": (0, 0),
                "rotation": 0,
                "depth": y
            },
            {
                "parts": [
                    {"tabs": "FEMALE", "length": y}
                ],
                "translation": (x, 0),
                "rotation": 1,
                "depth": x
            }
        ]
    }]
    return single_edge_piece


def error_print(msg):
    print(msg)


def test_square_piece():
    traycut = TrayLaserCut(options, mocked_unitfunc, error_print)
    square_element = mock_square(10)
    cmds = traycut.draw(square_element)
    assert(cmds[0] == 'M 0 0 l 10 0 ')
    assert(cmds[1] == 'M 10 0 l 0 10 ')
    assert(cmds[2] == 'M 10 10 l -10 0 ')
    assert(cmds[3] == 'M 0 10 l 0 -10 ')

def test_female_female_tabbed_side():
    xlen = 20
    ylen = 24
    ytab = 24/5.0
    f_female_female_edges = mock_female_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    thickness = opts["thickness"]
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(f_female_female_edges)
    expected = 'M 0 0 ' + \
        'l {} {} '.format(tab_size, 0) + \
        'l {} {} '.format(0, -thickness) +\
        'l {} {} '.format(tab_size, 0) + \
        'l {} {} '.format(0, thickness) +\
        'l {} {} '.format(tab_size, 0) + \
        'l {} {} '.format(0, -thickness) + \
        'l {} {} '.format(tab_size, 0) + \
        'l {} {} '.format(0, thickness) + \
        'l {} {} '.format(tab_size, 0)
    assert(cmds[0] == expected)
    expected = 'M {} 0 '.format(xlen) +\
        'l 0 {} '.format(ytab) +\
        'l {} 0 '.format(thickness) +\
        'l 0 {} '.format(ytab) +\
        'l {} 0 '.format(-thickness) + \
        'l 0 {} '.format(ytab) + \
        'l {} 0 '.format(thickness) + \
        'l 0 {} '.format(ytab) + \
        'l {} 0 '.format(-thickness) +\
        'l 0 {} '.format(ytab)

    assert(cmds[1] == expected)


def test_female_male_tabbed_side():
    xlen = 20
    ylen = 24
    ytab = 24/5.0
    f_female_male_edges = mock_female_male_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    thickness = opts["thickness"]
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(f_female_male_edges)
    expected = 'M {} 0 '.format(-thickness) + \
               'l {} {} '.format(tab_size+thickness, 0) + \
               'l {} {} '.format(0, -thickness) + \
               'l {} {} '.format(tab_size, 0) + \
               'l {} {} '.format(0, thickness) + \
               'l {} {} '.format(tab_size, 0) + \
               'l {} {} '.format(0, -thickness) + \
               'l {} {} '.format(tab_size, 0) + \
               'l {} {} '.format(0, thickness) + \
               'l {} {} '.format(tab_size + thickness, 0)
    assert(cmds[0] == expected)
    expected = 'M {} {} '.format(xlen + thickness, 0) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(-thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(-thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(thickness) + \
               'l 0 {} '.format(ytab)
    assert(cmds[1] == expected)


def test_male_male_tabbed_side():
    xlen = 20
    ylen = 24
    ytab = 24/5.0
    f_male_male_edges = mock_male_male_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    thickness = opts["thickness"]
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(f_male_male_edges)
    expected = 'M {} {} '.format(-thickness, -thickness) + \
               'l {} {} '.format(tab_size+thickness, 0) + \
               'l {} {} '.format(0, thickness) + \
               'l {} {} '.format(tab_size, 0) + \
               'l {} {} '.format(0, -thickness) + \
               'l {} {} '.format(tab_size, 0) + \
               'l {} {} '.format(0, thickness) + \
               'l {} {} '.format(tab_size, 0) + \
               'l {} {} '.format(0, -thickness) + \
               'l {} {} '.format(tab_size + thickness, 0)
    assert(cmds[0] == expected)
    expected = 'M {} {} '.format(xlen + thickness, -thickness) + \
               'l 0 {} '.format(ytab+thickness) + \
               'l {} 0 '.format(-thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(-thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(thickness) + \
               'l 0 {} '.format(ytab+thickness)
    assert(cmds[1] == expected)


def test_top_male_tabbed_side():
    xlen = 20
    ylen = 24
    ytab = 24/5.0
    f_top_male_edges = mock_top_male_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    thickness = opts["thickness"]
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(f_top_male_edges)
    expected = 'M {} {} '.format(-thickness, 0) + \
               'l {} {} '.format(xlen+thickness*2, 0)
    assert(cmds[0] == expected)
    expected = 'M {} {} '.format(xlen + thickness, 0) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(-thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(-thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(thickness) + \
               'l 0 {} '.format(ytab)
    assert(cmds[1] == expected)


def test_top_female_tabbed_side():
    xlen = 20
    ylen = 24
    ytab = 24/5.0
    f_top_female_edges = mock_top_female_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    thickness = opts["thickness"]
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(f_top_female_edges)
    expected = 'M {} {} '.format(0, 0) + \
               'l {} {} '.format(xlen, 0)
    assert(cmds[0] == expected)
    expected = 'M {} {} '.format(xlen, 0) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(-thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(thickness) + \
               'l 0 {} '.format(ytab) + \
               'l {} 0 '.format(-thickness) + \
               'l 0 {} '.format(ytab)
    assert(cmds[1] == expected)
