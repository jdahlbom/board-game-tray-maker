from traymaker_logic import TrayLaserCut

def mocked_unitfunc(unitstr):
    return 1


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
                "translation": (0, 0),
                "rotation": 0,
                "depth": Y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": Y}
                ],
                "translation": (X, 0),
                "rotation": 1,
                "depth": X,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": X}
                ],
                "translation": (X, Y),
                "rotation": 2,
                "depth": Y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "TOP", "length": Y}
                ],
                "translation": (0, Y),
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
                "translation": (0, 0),
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "FEMALE", "length": y}
                ],
                "translation": (x, 0),
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
                "translation": (0, 0),
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "MALE", "length": y}
                ],
                "translation": (x, 0),
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
                "translation": (0, 0),
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "MALE", "length": y}
                ],
                "translation": (x, 0),
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
                "translation": (0, 0),
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "MALE", "length": y}
                ],
                "translation": (x, 0),
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
                "translation": (0, 0),
                "rotation": 0,
                "depth": y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "FEMALE", "length": y}
                ],
                "translation": (x, 0),
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
                "translation": (0, 0),
                "rotation": 0,
                "depth": Y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "START_HALF_TAB", "length": Y}
                ],
                "translation": (X, 0),
                "rotation": 1,
                "depth": X,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "FEMALE", "length": X}
                ],
                "translation": (X, Y),
                "rotation": 2,
                "depth": Y,
                "opposite": opposite_piece
            },
            {
                "parts": [
                    {"tabs": "END_HALF_TAB", "length": Y}
                ],
                "translation": (0, Y),
                "rotation": 3,
                "depth": X,
                "opposite": opposite_piece
            }
        ]
    }]



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
    pieces = mock_female_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(pieces)
    thickness = pieces[0]["edges"][0]["opposite"]["thickness"]
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
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
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
    pieces = mock_female_male_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(pieces)
    thickness = pieces[0]["edges"][0]["opposite"]["thickness"]
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
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
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
    pieces = mock_male_male_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(pieces)
    thickness = pieces[0]["edges"][0]["opposite"]["thickness"]
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
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
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
    pieces = mock_top_male_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(pieces)
    thickness = pieces[0]["edges"][0]["opposite"]["thickness"]
    expected = 'M {} {} '.format(-thickness, 0) + \
               'l {} {} '.format(xlen+thickness*2, 0)
    assert(cmds[0] == expected)
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
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
    pieces = mock_top_female_edge(xlen, ylen)
    tab_size = 4.0
    opts = options
    opts["nomTab"] = tab_size
    traycut = TrayLaserCut(opts, mocked_unitfunc, error_print)
    cmds = traycut.draw(pieces)
    expected = 'M {} {} '.format(0, 0) + \
               'l {} {} '.format(xlen, 0)
    assert(cmds[0] == expected)
    thickness = pieces[0]["edges"][1]["opposite"]["thickness"]
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

def test_square_with_holes():
    pieces = mock_square(10)
    pieces[0]["edges"][0]["holes"] = [{
        "opposite": {"thickness": 2},
        "offset": 4,
        "shape": "START_HALF_TAB"
    }]
    traycut = TrayLaserCut(options, mocked_unitfunc, error_print)
    cmds = traycut.draw(pieces)
    assert(cmds[0] == 'M 0 0 l 10 0 ')
    assert(cmds[1] == 'M 4 0 l 0 5 l 2 0 l 0 -5 l -2 0 ')
    assert(cmds[2] == 'M 10 0 l 0 10 ')
    assert(cmds[3] == 'M 10 10 l -10 0 ')
    assert(cmds[4] == 'M 0 10 l 0 -10 ')

def test_half_tabs():
    pieces = mock_half_tabs(12)
    opts = options
    opts["nomTab"] = 4
    traycut = TrayLaserCut(options, mocked_unitfunc, error_print)
    cmds = traycut.draw(pieces)

    assert(cmds[0] == 'M -3 -3 l 7.0 0 l 0 3 l 4.0 0 l 0 -3 l 7.0 0 ')
    assert(cmds[1] == 'M 15 -3 l 0 9 l -3 0 l 0 6 ')
    assert(cmds[2] == 'M 12 12 l -4.0 0 l 0 3 l -4.0 0 l 0 -3 l -4.0 0 ')
    assert(cmds[3] == 'M 0 12 l 0 -6 l -3 0 l 0 -9 ')


def test_two_squares():
    pieces = mock_square(10)
    pieces.extend(mock_square(10, (0, 20)))
    traycut = TrayLaserCut(options, mocked_unitfunc, error_print)
    cmds = traycut.draw(pieces)

    assert(len(cmds) == 8)
    assert(cmds[0] == 'M 0 0 l 10 0 ')
    assert(cmds[1] == 'M 10 0 l 0 10 ')
    assert(cmds[2] == 'M 10 10 l -10 0 ')
    assert(cmds[3] == 'M 0 10 l 0 -10 ')
    assert(cmds[4] == 'M 0 20 l 10 0 ')
    assert(cmds[5] == 'M 10 20 l 0 10 ')
    assert(cmds[6] == 'M 10 30 l -10 0 ')
    assert(cmds[7] == 'M 0 30 l 0 -10 ')
