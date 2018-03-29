from traymaker_logic import TrayLaserCut
import gloomhaven

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


def mocked_unitfunc(unitstr):
    exp = re.compile(r'^([0-9]*)[^0-9]*$')
    matches = exp.match(unitstr)
    return 1


def error_print(msg):
    print(msg)


def xtest_effects_tray_syntax_works():
    pieces = gloomhaven.tray_setup("effects")
    lasercut = TrayLaserCut(options, mocked_unitfunc, error_print)
    cmds = lasercut.draw(pieces)
    print(cmds)
