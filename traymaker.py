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
from llist import dllist

_ = gettext.gettext

TOP = 0
MALE = 1
FEMALE = 2
NO_EDGE = 3
HINGE_FEMALE = 4
CURVE = 5


class BoxMaker(inkex.Effect):

    def __init__(self):
        # Call the base class constructor.
        inkex.Effect.__init__(self)
        # Define options
        self.OptionParser.add_option('--unit',action='store',type='string',
                                     dest='unit',default='mm',help='Measure Units')
        self.OptionParser.add_option('--inside',action='store',type='int',
                                     dest='inside',default=0,help='Int/Ext Dimension')
        self.OptionParser.add_option('--length',action='store',type='float',
                                     dest='length',default=100,help='Length of Box')
        self.OptionParser.add_option('--width',action='store',type='float',
                                     dest='width',default=100,help='Width of Box')
        self.OptionParser.add_option('--depth',action='store',type='float',
                                     dest='height',default=100,help='Height of Box')
        self.OptionParser.add_option('--indentradius',action='store',type='float',
                                     dest='indentradius',default=50,help='End of tray indent circle radius')
        self.OptionParser.add_option('--tab',action='store',type='float',
                                     dest='tab',default=25,help='Nominal Tab Width')
        self.OptionParser.add_option('--equal',action='store',type='int',
                                     dest='equal',default=0,help='Equal/Prop Tabs')
        self.OptionParser.add_option('--thickness',action='store',type='float',
                                     dest='thickness',default=10,help='Thickness of Material')
        self.OptionParser.add_option('--kerf',action='store',type='float',
                                     dest='kerf',default=0.5,help='Kerf (width) of cut')
        self.OptionParser.add_option('--clearance',action='store',type='float',
                                     dest='clearance',default=0.01,help='Clearance of joints')
        self.OptionParser.add_option('--style',action='store',type='int',
                                     dest='style',default=25,help='Layout/Style')
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
        X = self.unittouu( str(self.options.length)  + unit )
        Y = self.unittouu( str(self.options.width) + unit )
        Z = self.unittouu( str(self.options.height)  + unit )
        indentradius = self.unittouu( str(self.options.indentradius) + unit)
        thickness = self.unittouu( str(self.options.thickness)  + unit )
        nomTab = self.unittouu( str(self.options.tab) + unit )
        equalTabs=self.options.equal
        kerf = self.unittouu( str(self.options.kerf)  + unit )
        clearance = self.unittouu( str(self.options.clearance)  + unit )
        spacing = self.unittouu( str(self.options.spacing)  + unit )

        cut_length = self.unittouu( str(self.options.cut_length)  + unit )
        gap_length = self.unittouu( str(self.options.gap_length)  + unit )
        sep_distance = self.unittouu( str(self.options.sep_distance)  + unit )

        correction=kerf-clearance

        # check input values mainly to avoid python errors
        # TODO restrict values to *correct* solutions
        error=0

        if min(X,Y,Z)==0:
            inkex.errormsg(_('Error: Dimensions must be non zero'))
            error=1
        if max(X,Y,Z)>max(widthDoc,heightDoc)*10: # crude test
            inkex.errormsg(_('Error: Dimensions Too Large'))
            error=1
        if min(X,Y,Z)<3*nomTab:
            inkex.errormsg(_('Error: Tab size too large'))
            error=1
        if nomTab<thickness:
            inkex.errormsg(_('Error: Tab size too small'))
            error=1
        if thickness==0:
            inkex.errormsg(_('Error: Thickness is zero'))
            error=1
        if thickness>min(X,Y,Z)/3: # crude test
            inkex.errormsg(_('Error: Material too thick'))
            error=1
        if correction>min(X,Y,Z)/3: # crude test
            inkex.errormsg(_('Error: Kerf/Clearence too large'))
            error=1
        if spacing>max(X,Y,Z)*10: # crude test
            inkex.errormsg(_('Error: Spacing too large'))
            error=1
        if spacing<kerf:
            inkex.errormsg(_('Error: Spacing too small'))
            error=1
        if indentradius<0:
            inkex.errormsg(_('Error: Indent Radius cannot be negative'))
            error=1
        if thickness >= nomTab:
            inkex.errormsg(_('Error: Material thickness should be less than nominal tab size'))
            error=1
        if error:
            exit()

        options = {
            "unit": unit,
            "X": X,
            "Y": Y,
            "Z": Z,
            "indentradius": indentradius,
            "thickness": thickness,
            "nomTab": nomTab,
            "equalTabs": equalTabs,
            "kerf": kerf,
            "clearance": clearance,
            "spacing": spacing,
            "cut_length": cut_length,
            "gap_length": gap_length,
            "sep_distance": sep_distance
        }

        tray_cut = TrayLaserCut(options, self.unittouu, inkex.errormsg)
        command_str = tray_cut.draw()
        for cmd in command_str:
            self.drawS(cmd)


    def drawS(self, XYstring):         # Draw lines from a list
        name='part'
        style = { 'stroke': '#000000', 'fill': 'none' }
        drw = {'style':simplestyle.formatStyle(style),inkex.addNS('label','inkscape'):name,'d':XYstring}
        inkex.etree.SubElement(parent, inkex.addNS('path','svg'), drw )




if __name__ == "__main__":
    # Create effect instance and apply it.
    effect = BoxMaker()
    effect.affect()

