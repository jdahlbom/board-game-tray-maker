from traymaker_logic import TrayLaserCut
import re

def mocked_unitfunc(unitstr):
    exp = re.compile(r'^([0-9]*)[^0-9]*$')
    matches = exp.match(unitstr)
    print(matches)
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
        ],
        "offset": (0,0)
    }]


def mock_tray():
    other_pieces = [
        {
            "width": self.Z,
            "length": self.Y,
            "edges": [FEMALE, MALE, FEMALE, TOP],
            "offset": ( self.spacing, self.Z+self.spacing*2 )
        },
        {
            "width": self.X,
            "length": self.Z,
            "edges": [TOP, MALE, MALE, MALE],
            "offset": ( self.X+self.spacing*2, self.spacing ),
            "indentradius": self.indentradius
        },
        {
            "width": self.Z,
            "length": self.Y,
            "edges": [FEMALE, TOP, FEMALE, MALE],
            "offset": ( self.Z+self.X+self.spacing * 3, self.Z + self.spacing*2 )
        },
        {
            "width": self.X,
            "length": self.Z,
            "edges": [MALE, MALE, TOP, MALE],
            "offset": ( self.Z+self.spacing*2, self.Z+self.Y+self.spacing*3 ),
            "indentradius": self.indentradius
        }]



def error_print(msg):
    print(msg)


def test_foo():
    traycut = TrayLaserCut(options, mocked_unitfunc, error_print)
    square_element = mock_square(10)
    cmds = traycut.draw(square_element)
    assert(cmds[0] == 'M 0 0 l 10 0 ')
    assert(cmds[1] == 'M 10 0 l 0 10 ')
    assert(cmds[2] == 'M 10 10 l -10 0 ')
    assert(cmds[3] == 'M 0 10 l 0 -10 ')
