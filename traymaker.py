#! /usr/bin/env python
'''
Generates Inkscape SVG file containing box components needed to 
laser cut a tabbed construction box taking kerf and clearance into account

Copyright (C) 2011 elliot white   elliot@twot.eu
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
__version__ = "0.91" ### please report bugs, suggestions etc to bugs@twot.eu ###

## unittouu method changed to InkScape 0.91 style ##
## this version will NOT work in InkScape 0.48    ##

import inkex, simplestyle, gettext
from traymaker_logic import TrayLaserCut
import gloomhaven

_ = gettext.gettext

CUT_COLOR='#000000'
ENGRAVE_COLOR='#FF0000'

class TrayMaker(inkex.Effect):

    def __init__(self):
        # Call the base class constructor.
        inkex.Effect.__init__(self)
        # Define options
        self.OptionParser.add_option('--tray_name', action='store', type='string',
                                     dest='tray_name', default='effects', help='Tray name')
        self.OptionParser.add_option('--simplify', action='store', type='string',
                                     dest='simplify', default=False, help='Simplify design for printing')
        self.OptionParser.add_option('--unit', action='store', type='string',
                                     dest='unit', default='mm', help='Measure Units')
        self.OptionParser.add_option('--cutarea', action='store', type='int',
                                     dest='cutarea', default='420', help='Width of Cut Area')
        self.OptionParser.add_option('--tab', action='store', type='float',
                                     dest='tab', default=25, help='Nominal Tab Width')
        self.OptionParser.add_option('--equal', action='store', type='int',
                                     dest='equal', default=0, help='Equal/Prop Tabs')
        self.OptionParser.add_option('--kerf', action='store', type='float',
                                     dest='kerf', default=0.5, help='Kerf (width) of cut')
        self.OptionParser.add_option('--clearance', action='store', type='float',
                                     dest='clearance', default=0.01, help='Clearance of joints')
        self.OptionParser.add_option('--spacing', action='store', type='float',
                                     dest='spacing', default=25, help='Part Spacing')
        self.OptionParser.add_option('--cut_length', action='store', type='float',
                                     dest='cut_length', default=0, help='length of the cuts for the hinge.')
        self.OptionParser.add_option('--gap_length', action='store', type='float',
                                     dest='gap_length', default=0, help='separation distance between successive hinge cuts.')
        self.OptionParser.add_option('--sep_distance', action='store', type='float',
                                     dest='sep_distance', default=0, help='distance between successive lines of hinge cuts.')

    def create_layer(self, parent, layer_name):
        # Create a new layer.
        layer = inkex.etree.SubElement(parent, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), layer_name)
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        return layer

    def effect(self):
        global nomTab, equalTabs, thickness, correction, error

        THICKNESS_THICK_MM = 3.5
        THICKNESS_SLIM_MM = 2

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()

        # Get the attibutes:
        widthDoc  = self.unittouu(svg.get('width'))
        heightDoc = self.unittouu(svg.get('height'))

        # Get script's option values.
        unit = self.options.unit
        uconv = self.unittouu("1 {}".format(unit))
        cutarea = self.options.cutarea
        nomTab = self.options.tab
        equalTabs = self.options.equal
        kerf = self.options.kerf
        clearance = self.options.clearance
        spacing = self.options.spacing

        cut_length = self.options.cut_length
        gap_length = self.options.gap_length
        sep_distance = self.options.sep_distance

        simplify = (self.options.simplify == "true")

        correction = kerf - clearance

        # check input values mainly to avoid python errors
        # TODO restrict values to *correct* solutions
        error = 0

        if spacing < kerf:
            inkex.errormsg(_('Error: Spacing too small'))
            error = 1
        if error:
            exit()

        options = {
            "unit": unit,
            "uconv": uconv,
            "nomTab": nomTab,
            "equalTabs": equalTabs,
            "kerf": kerf,
            "clearance": clearance,
            "spacing": spacing,
            "cut_length": cut_length,
            "gap_length": gap_length,
            "sep_distance": sep_distance,
            "simplify": simplify
        }

        tray_cut = TrayLaserCut(options, inkex.errormsg)

        def draw_tray(trayname, tray_num=None):
            pieces = gloomhaven.tray_setup(trayname, (THICKNESS_THICK_MM, THICKNESS_SLIM_MM), inkex.errormsg)
            for thick in set(map(lambda piece: str(piece["thickness"]), pieces)):
                command_dict = tray_cut.draw(pieces, thick, sort_pieces=True, tray_number=tray_num, max_width=cutarea)
                layer = self.create_layer(svg, "{}-{}mm".format(trayname, thick))
                for cmds in command_dict:
                    grouped_piece = inkex.etree.SubElement(layer, 'g')
                    grouped_piece.set(inkex.addNS('groupmode', 'inkscape'), 'group')
                    self.drawS(grouped_piece, " ".join(cmds["cut"]), CUT_COLOR)
                    self.drawS(grouped_piece, " ".join(cmds["engrave"]), ENGRAVE_COLOR)

        if self.options.tray_name == 'all':
            tray_number = 0
            for tray_name in gloomhaven.tray_names():
                tray_number += 1
                draw_tray(tray_name, tray_number)
        else:
            draw_tray(self.options.tray_name)

    def drawS(self, parent, XYstring, strokeColor=CUT_COLOR):         # Draw lines from a list
        name = 'part'
        style = {'stroke': strokeColor, 'fill': 'none'}
        drw = {'style': simplestyle.formatStyle(style), inkex.addNS('label', 'inkscape'): name, 'd': XYstring}
        inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), drw)


if __name__ == "__main__":
    # Create effect instance and apply it.
    effect = TrayMaker()
    effect.affect()
