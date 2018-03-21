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
    "nom_tab": 4,
    "spacing": 1,
    "kerf": 0.1,
    "empty_space": 1,
    "clearance": 0.1,
    "cut_length": 5,
    "gap_length": 2,
    "sep_distance": 1,
    "indentradius": 0
}


def test_foo():
    traycut = TrayLaserCut(options, mocked_unitfunc)
    traycut.draw()
