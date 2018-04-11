from traymaker_logic import TrayLaserCut
from copy import deepcopy

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


def mock_square(side, offset=(0, 0)):
    X = side
    Y = side
    opposite_piece = {
        "thickness": 3
    }

    return [{
        "width": X,
        "height": Y,
        "offset": offset,
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "TOP", "length": X}
                ],
                "rotation": 0,
                "depth": Y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": Y}
                ],
                "rotation": 1,
                "depth": X,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": X}
                ],
                "rotation": 2,
                "depth": Y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": Y}
                ],
                "rotation": 3,
                "depth": X,
                "opposite": opposite_piece
            }
        ]
    }]


def mock_female_edge(x=20, y=12):
    opposite_piece = {
        "thickness": 3
    }

    single_edge_piece = [{
        "width": x,
        "height": y,
        "offset": (0,0),
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "FEMALE", "length": x}
                ],
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "FEMALE", "length": y}
                ],
                "rotation": 1,
                "depth": x,
                "opposite": opposite_piece
            }
        ]
    }]
    return single_edge_piece


def mock_female_male_edge(x, y):

    opposite_piece = {
        "thickness": 3
    }
    single_edge_piece = [{
        "width": x,
        "height": y,
        "offset": (0, 0),
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "FEMALE", "length": x}
                ],
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "MALE", "length": y}
                ],
                "rotation": 1,
                "depth": x,
                "opposite": opposite_piece
            }
        ]
    }]
    return single_edge_piece


def mock_male_male_edge(x, y):
    opposite_piece = {
        "thickness": 3
    }
    single_edge_piece = [{
        "width": x,
        "height": y,
        "offset": (0, 0),
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "MALE", "length": x}
                ],
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "MALE", "length": y}
                ],
                "rotation": 1,
                "depth": x,
                "opposite": opposite_piece
            }
        ]
    }]
    return single_edge_piece


def mock_top_male_edge(x, y):
    opposite_piece = {
        "thickness": 3
    }

    single_edge_piece = [{
        "width": x,
        "height": y,
        "offset": (0, 0),
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "TOP", "length": x}
                ],
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "MALE", "length": y}
                ],
                "rotation": 1,
                "depth": x,
                "opposite": opposite_piece
            }
        ]
    }]
    return single_edge_piece


def mock_top_female_edge(x, y):
    opposite_piece = {
        "thickness": 3
    }

    single_edge_piece = [{
        "width": x,
        "height": y,
        "offset": (0, 0),
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "TOP", "length": x}
                ],
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "FEMALE", "length": y}
                ],
                "rotation": 1,
                "depth": x,
                "opposite": opposite_piece
            }
        ]
    }]
    return single_edge_piece

def mock_half_tabs(side):
    X = side
    Y = side
    opposite_piece = {
        "thickness": 3
    }

    return [{
        "width": X,
        "height": Y,
        "offset": (0,0),
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "MALE", "length": X}
                ],
                "rotation": 0,
                "depth": Y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "START_HALF_TAB", "length": Y}
                ],
                "rotation": 1,
                "depth": X,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "FEMALE", "length": X}
                ],
                "rotation": 2,
                "depth": Y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "END_HALF_TAB", "length": Y}
                ],
                "rotation": 3,
                "depth": X,
                "opposite": opposite_piece
            }
        ]
    }]

def mock_top_half_tabs(side):
    X = side
    Y = side
    opposite_piece = {
        "thickness": 3
    }

    return [{
        "width": X,
        "height": Y,
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "END_HALF_TAB", "length": X}
                ],
                "rotation": 0,
                "depth": Y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": Y}
                ],
                "rotation": 1,
                "depth": X,
                "opposite": opposite_piece
            }
        ]
    }]

def mock_multipart_top():
    opposite_piece = {
        "thickness": 3
    }

    return [{
        "width": 12,
        "height": 12,
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "TOP", "length": 6},
                    {"tabs": "TOP", "length": 6}
                ],
                "rotation": 0,
                "depth": 12,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "START_HALF_TAB", "length": 12}
                ],
                "rotation": 1,
                "depth": 12,
                "opposite": opposite_piece
            }
        ]
    }]

def mock_multipart_top_with_indent():
    opposite_piece = {
        "thickness": 3
    }

    return [{
        "width": 80.26,
        "height": 12,
        "thickness": 3,
        "edges": [
            {
                "parts": [
                    {"tabs": "TOP", "length": 40.13, "indent": {"offset": 13.07, "radius": 7}},
                    {"tabs": "TOP", "length": 40.13, "indent": {"offset": 13.07, "radius": 7}},
                ],
                "rotation": 0,
                "depth": 12,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "START_HALF_TAB", "length": 12}
                ],
                "rotation": 1,
                "depth": 12,
                "opposite": opposite_piece
            }
        ]
    }]

def mock_half_tabs_odd_edge_length():
    opposite_piece = {
        "thickness": 3
    }

    return [
    {
        "name": "1 small h-divider",
        "width": 62,
        "height": 13,
        "thickness": 2,
        "edges": [
            {
                "rotation": 0,
                "depth": 13,
                "opposite": opposite_piece,
                "parts": [
                    {
                        "tabs": "TOP",
                        "length": 62
                    }
                ]
            },
            {
                "rotation": 1,
                "opposite": opposite_piece,
                "parts": [
                    {
                        "tabs": "START_HALF_TAB",
                        "length": 13
                    }
                ]
            },
            {
                "rotation": 2,
                "opposite": opposite_piece,
                "parts": [
                    {
                        "tabs": "TOP",
                        "length": 62
                    }
                ]
            },
            {
                "rotation": 3,
                "opposite": opposite_piece,
                "parts": [
                    {
                        "tabs": "END_HALF_TAB",
                        "length": 13
                    }
                ]
            }
        ],

    }]


def error_print(msg):
    print(msg)


def test_square_piece():
    traycut = TrayLaserCut(deepcopy(options), error_print)
    square_element = mock_square(10)
    cmds = traycut.draw(square_element,3)
    cmds = cmds[0]["cut"]
    offset = 4
    assert(cmds[0] == 'M {} {} l 10 0 '.format(offset, offset))
    assert(cmds[1] == 'M {} {} l 0 10 '.format(offset+10, offset))
    assert(cmds[2] == 'M {} {} l -10 0 '.format(offset+10,offset+10))
    assert(cmds[3] == 'M {} {} l 0 -10 '.format(offset, offset+10))

def test_female_female_tabbed_side():
    xlen = 20
    ylen = 24
    ytab = 24/5.0
    pieces = mock_female_edge(xlen, ylen)
    tab_size = 4.0
    opts = deepcopy(options)
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]
    thickness = pieces[0]["edges"][0]["opposite"]["thickness"]
    offset = 4
    expected = 'M {} {} '.format(offset, offset) + \
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
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
    expected = 'M {} {} '.format(xlen+offset, offset) +\
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
    pieces = mock_female_male_edge(xlen, ylen)
    tab_size = 4.0
    opts = deepcopy(options)
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]
    offset = 4
    thickness = pieces[0]["edges"][0]["opposite"]["thickness"]
    expected = 'M {} {} '.format(-thickness+offset, offset) + \
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
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
    expected = 'M {} {} '.format(xlen + thickness + offset, offset) + \
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
    pieces = mock_male_male_edge(xlen, ylen)
    tab_size = 4.0
    opts = deepcopy(options)
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]
    thickness = pieces[0]["edges"][0]["opposite"]["thickness"]
    offset = 4
    expected = 'M {} {} '.format(-thickness + offset, -thickness + offset) + \
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
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
    expected = 'M {} {} '.format(xlen + thickness + offset, -thickness + offset) + \
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
    pieces = mock_top_male_edge(xlen, ylen)
    tab_size = 4.0
    opts = deepcopy(options)
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]
    thickness = pieces[0]["edges"][0]["opposite"]["thickness"]
    offset = 4
    expected = 'M {} {} '.format(-thickness + offset, offset) + \
               'l {} {} '.format(xlen+thickness*2, 0)
    assert(cmds[0] == expected)
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
    expected = 'M {} {} '.format(xlen + thickness + offset, offset) + \
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
    pieces = mock_top_female_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]

    offset = 4
    expected = 'M {} {} '.format(offset, offset) + \
               'l {} {} '.format(xlen, 0)
    assert(cmds[0] == expected)
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
    expected = 'M {} {} '.format(xlen + offset, offset) + \
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

def test_square_with_holes():
    pieces = mock_square(10)
    pieces[0]["edges"][0]["holes"] = [{
        "opposite": {"thickness": 2},
        "offset": 4,
        "shape": "START_HALF_TAB"
    }]
    traycut = TrayLaserCut(deepcopy(options), error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]

    offset = 4
    assert(cmds[0] == 'M {} {} l 10 0 '.format(offset, offset))
    assert(cmds[1] == 'M {} {} l 0 5.0 l 2 0 l 0 -5.0 l -2 0 '.format(offset+4, offset))
    assert(cmds[2] == 'M {} {} l 0 10 '.format(offset+10, offset))
    assert(cmds[3] == 'M {} {} l -10 0 '.format(offset+10, offset+10))
    assert(cmds[4] == 'M {} {} l 0 -10 '.format(offset, offset+10))


def test_half_tabs():
    pieces = mock_half_tabs(12)
    opts = deepcopy(options)
    opts["nomTab"] = 4
    traycut = TrayLaserCut(options, error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]

    offset = 4

    assert(cmds[0] == 'M {} {} l 7.0 0 l 0 3 l 4.0 0 l 0 -3 l 7.0 0 '.format(offset-3, offset-3))
    assert(cmds[1] == 'M {} {} l 0 9.0 l -3 0 l 0 6.0 '.format(offset+15, offset-3))
    assert(cmds[2] == 'M {} {} l -4.0 0 l 0 3 l -4.0 0 l 0 -3 l -4.0 0 '.format(offset+12, offset+12))
    assert(cmds[3] == 'M {} {} l 0 -6.0 l -3 0 l 0 -9.0 '.format(offset, offset + 12))


def test_two_squares():
    pieces = mock_square(10)
    pieces.extend(mock_square(10, (0, 20)))
    traycut = TrayLaserCut(deepcopy(options), error_print)
    thickness = 3
    piece_cmds = traycut.draw(pieces, thickness)

    offset = thickness + 1
    p_height = 10

    cmds = piece_cmds[0]["cut"]
    assert(len(cmds) == 4)
    assert(cmds[0] == 'M {} {} l 10 0 '.format(offset, offset))
    assert(cmds[1] == 'M {} {} l 0 10 '.format(offset+10, offset))
    assert(cmds[2] == 'M {} {} l -10 0 '.format(offset+10, offset+10))
    assert(cmds[3] == 'M {} {} l 0 -10 '.format(offset, offset+10))
    cmds = piece_cmds[1]["cut"]
    assert(len(cmds) == 4)
    assert(cmds[0] == 'M {} {} l 10 0 '.format(offset, offset + 2*(thickness+1) + p_height))
    assert(cmds[1] == 'M {} {} l 0 10 '.format(offset+10, offset + 2*(thickness+1) + p_height))
    assert(cmds[2] == 'M {} {} l -10 0 '.format(offset+10, offset + 2*(thickness+1) + 2*p_height))
    assert(cmds[3] == 'M {} {} l 0 -10 '.format(offset, offset + 2*(thickness+1) + 2*p_height))


def test_top_and_half():
    side_len = 10
    pieces = mock_top_half_tabs(side_len)
    thickness = 3
    offset = thickness + 1
    traycut = TrayLaserCut(deepcopy(options), error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]
    assert(len(cmds) == 2)
    assert(cmds[0] == 'M {} {} l 5.0 0 l 0 {} l 5.0 0 '.format(offset, offset, -thickness))
    assert(cmds[1] == 'M {} {} l 0 {} '.format(side_len+offset, offset-thickness, side_len+thickness))


def test_conversion_with_top_and_half():
    side_len = 10
    pieces = mock_top_half_tabs(side_len)
    opts = deepcopy(options)
    opts["uconv"] = 2.0
    thickness = 3*opts["uconv"]
    offset = thickness + 1*opts["uconv"]
    traycut = TrayLaserCut(opts, error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]
    assert(len(cmds) == 2)
    assert(cmds[0] == 'M {} {} l 10.0 0.0 l 0.0 {} l 10.0 0.0 '.format(offset, offset, -thickness))
    assert(cmds[1] == 'M {} {} l 0.0 {} '.format(side_len*opts["uconv"]+offset, offset-thickness, side_len*opts["uconv"]+thickness))


def test_multipart_top():
    pieces = mock_multipart_top()
    traycut = TrayLaserCut(deepcopy(options), error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]
    assert(len(cmds) == 3)
    assert(cmds[0] == 'M 4 4 l 6 0 ')
    assert(cmds[1] == 'M 10 4 l 9 0 ')
    assert(cmds[2] == 'M 19 4 l 0 6.0 l -3 0 l 0 6.0 ')

def test_multipart_top_indent():
    pieces = mock_multipart_top_with_indent()
    traycut = TrayLaserCut(deepcopy(options), error_print)
    cmds = traycut.draw(pieces,3)
    cmds = cmds[0]["cut"]
    assert(len(cmds) == 3)
    assert(cmds[0] == 'M 4 4 l 13.07 0 a 7,7 0 0,0 14,0 l 13.06 0 ')
    assert(cmds[1] == 'M 44.13 4 l 13.07 0 a 7,7 0 0,0 14,0 l 16.06 0 ')
    assert(cmds[2] == 'M 87.26 4 l 0 6.0 l -3 0 l 0 6.0 ')

def test_half_tabs_with_odd_length():
    opts = deepcopy(options)
    opts["nomTab"] = 15
    pieces = mock_half_tabs_odd_edge_length()
    traycut = TrayLaserCut(opts, error_print)
    cmds = traycut.draw(pieces,2)
    cmds = cmds[0]["cut"]
    assert(len(cmds) == 4)
    assert(cmds[0] == 'M 1 4 l 68 0 ')
    assert(cmds[1] == 'M 69 4 l 0 6.5 l -3 0 l 0 6.5 ')
    assert(cmds[2] == 'M 66 17 l -62 0 ')
    assert(cmds[3] == 'M 4 17 l 0 -6.5 l -3 0 l 0 -6.5 ')
