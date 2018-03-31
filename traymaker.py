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

from math import pi as PI
import sys,inkex,simplestyle,gettext
from traymaker_logic import TrayLaserCut
import gloomhaven
from llist import dllist

_ = gettext.gettext

TOP = 0
MALE = 1
FEMALE = 2
NO_EDGE = 3
HINGE_FEMALE = 4
CURVE = 5


class TrayMaker(inkex.Effect):

    def __init__(self):
        # Call the base class constructor.
        inkex.Effect.__init__(self)
        # Define options
        self.OptionParser.add_option('--tray_name',action='store',type='string',
                                     dest='tray_name',default='effects',help='Tray name')
        self.OptionParser.add_option('--unit',action='store',type='string',
                                     dest='unit',default='mm',help='Measure Units')
        self.OptionParser.add_option('--tab',action='store',type='float',
                                     dest='tab',default=25,help='Nominal Tab Width')
        self.OptionParser.add_option('--equal',action='store',type='int',
                                     dest='equal',default=0,help='Equal/Prop Tabs')
        self.OptionParser.add_option('--kerf',action='store',type='float',
                                     dest='kerf',default=0.5,help='Kerf (width) of cut')
        self.OptionParser.add_option('--clearance',action='store',type='float',
                                     dest='clearance',default=0.01,help='Clearance of joints')
        self.OptionParser.add_option('--spacing',action='store',type='float',
                                     dest='spacing',default=25,help='Part Spacing')
        self.OptionParser.add_option('--cut_length',action='store',type='float',
                                     dest='cut_length',default=0,help='length of the cuts for the hinge.')
        self.OptionParser.add_option('--gap_length',action='store',type='float',
                                     dest='gap_length',default=0,help='separation distance between successive hinge cuts.')
        self.OptionParser.add_option('--sep_distance',action='store',type='float',
                                     dest='sep_distance',default=0,help='distance between successive lines of hinge cuts.')


    def effect(self):
        global parent,nomTab,equalTabs,thickness,correction,error

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()

        # Get the attibutes:
        widthDoc  = self.unittouu(svg.get('width'))
        heightDoc = self.unittouu(svg.get('height'))

        # Create a new layer.
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'newlayer')
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        parent=self.current_layer

        # Get script's option values.
        unit=self.options.unit
        uconv = self.unittouu( "1 {}".format(unit))
        nomTab = self.options.tab
        equalTabs=self.options.equal
        kerf = self.options.kerf
        clearance = self.options.clearance
        spacing = self.options.spacing

        cut_length = self.options.cut_length
        gap_length = self.options.gap_length
        sep_distance = self.options.sep_distance

        correction=kerf-clearance

        # check input values mainly to avoid python errors
        # TODO restrict values to *correct* solutions
        error=0

        if spacing<kerf:
            inkex.errormsg(_('Error: Spacing too small'))
            error=1
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
            "sep_distance": sep_distance
        }

        tray_cut = TrayLaserCut(options, inkex.errormsg)
        pieces = gloomhaven.tray_setup(self.options.tray_name, inkex.errormsg)
        command_str = tray_cut.draw(pieces)
        for cmd in command_str:
            self.drawS(cmd)


    def drawS(self, XYstring):         # Draw lines from a list
        name='part'
        style = { 'stroke': '#000000', 'fill': 'none' }
        drw = {'style':simplestyle.formatStyle(style),inkex.addNS('label','inkscape'):name,'d':XYstring}
        inkex.etree.SubElement(parent, inkex.addNS('path','svg'), drw )




if __name__ == "__main__":
    # Create effect instance and apply it.
    effect = TrayMaker()
    effect.affect()

