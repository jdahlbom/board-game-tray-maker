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
from testable_traymaker import test_me
from llist import dllist

_ = gettext.gettext

TOP = 0
MALE = 1
FEMALE = 2
NO_EDGE = 3
HINGE_FEMALE = 4
CURVE = 5

test_me()

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
        inside=self.options.inside
        X = self.unittouu( str(self.options.length)  + unit )
        Y = self.unittouu( str(self.options.width) + unit )
        Z = self.unittouu( str(self.options.height)  + unit )
        indentradius = self.unittouu( str(self.options.indentradius) + unit)
        thickness = self.unittouu( str(self.options.thickness)  + unit )
        nomTab = self.unittouu( str(self.options.tab) + unit )
        equalTabs=self.options.equal
        kerf = self.unittouu( str(self.options.kerf)  + unit )
        clearance = self.unittouu( str(self.options.clearance)  + unit )
        layout=self.options.style
        spacing = self.unittouu( str(self.options.spacing)  + unit )

        cut_length = self.unittouu( str(self.options.cut_length)  + unit )
        gap_length = self.unittouu( str(self.options.gap_length)  + unit )
        sep_distance = self.unittouu( str(self.options.sep_distance)  + unit )


        if inside: # if inside dimension selected correct values to outside dimension
            X+=thickness*2
            Y+=thickness*2
            Z+=thickness*2

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
        self.draw()


    def draw(self):
        # layout format:(rootx),(rooty),Xlength,Ylength,tabInfo
        # root= (spacing,X,Y,Z) * values in tuple
        # tabInfo= <abcd> 0=holes 1=tabs
        hinge_radius=self.unittouu("6mm")
        empty_space=self.unittouu("10mm")
        pieces = [
            {
                "width": X,
                "length": Y,
                "edges": dllist([
                    {
                        "parts": dllist([
                            {"tabs": FEMALE, "length": X-hinge_radius*PI/2-empty_space},
                            {"tabs": HINGE_FEMALE, "length": hinge_radius*PI/2},
                            {"tabs": FEMALE, "length": empty_space}]),
                        "translation": (0, 0),
                        "rotation": 0,
                        "depth": Y
                    },
                    {
                        "parts": dllist([{"tabs": TOP, "length": Y}]),
                        "translation": (X, 0),
                        "rotation": 1,
                        "depth": X
                    },
                    {
                        "parts": dllist([
                            {"tabs": FEMALE, "length": empty_space},
                            {"tabs": TOP, "length": hinge_radius*PI/2},
                            {"tabs": FEMALE, "length": X-empty_space-hinge_radius*PI/2}]),
                        "translation": (X, Y),
                        "rotation": 2,
                        "depth": Y
                    },
                    {
                        "parts": dllist([{"tabs": FEMALE, "length": Y}]),
                        "translation": (0, Y),
                        "rotation": 3,
                        "depth": X
                    }
                ]),
                "offset": ( Z+spacing*2, Z+spacing*2 )
            }]

        other_pieces = [
            {
                "width": Z,
                "length": Y,
                "edges": [FEMALE, MALE, FEMALE, TOP],
                "offset": ( spacing, Z+spacing*2 )
            },
            {
                "width": X,
                "length": Z,
                "edges": [TOP, MALE, MALE, MALE],
                "offset": ( X+spacing*2, spacing ),
                "indentradius": indentradius
            },
            {
                "width": Z,
                "length": Y,
                "edges": [FEMALE, TOP, FEMALE, MALE],
                "offset": ( Z+X+spacing * 3, Z + spacing*2 )
            },
            {
                "width": X,
                "length": Z,
                "edges": [MALE, MALE, TOP, MALE],
                "offset": ( Z+spacing*2, Z+Y+spacing*3 ),
                "indentradius": indentradius
            }]


        for piece in pieces: # generate and draw each piece of the box
            pieceDirectives = []

            for edge_node in piece["edges"]:
                edge = edge_node.value
                left_edge = edge.prev.value
                right_edge = edge.next.value

                part_node = edge.value["parts"].first
                for part_node in edge.value["parts"]:

                    translation_x, translation_y = edge["translation"]
                    rotation = edge["rotation"]

                    depth = edge["depth"]

                    indentradius = 0
                    if "indentradius" in piece:
                        indentradius = piece["indentradius"]

                    x_part_offset = 0
                    prev_part = part_node.prev
                    while prev_part is not None:
                        x_part_offset += prev_part.value["length"]
                        prev_part = prev_part.prev

                    directives = g_side(edge_node, part_node, nomTab, indentradius, (depth, cut_length, gap_length, sep_distance))
                    directives = transform(directives, 0, (x_part_offset, 0))
                    directives = transform(directives, rotation, (translation_x, translation_y))
                    pieceDirectives.extend(directives)

            piece_x, piece_y = piece["offset"]
            for directive in pieceDirectives:
                (x, y) = directive["origin"]
                cmds = "M {} {} ".format(x+piece_x, y+piece_y)
                for elem in directive["elements"]:
                    cmds += elem["draw"](elem)
                drawS(cmds)

        if error:
            inkex.errormsg(_('Warning: Box may be impractical'))


def line(x, y):
    def draw(line_element):
        (x,y) = line_element["coords"]
        (x,y) = rotateClockwise((x,y), line_element["rotations"])
        return "l {} {} ".format(x, y)

    return {
        "type": "line",
        "coords": (x,y),
        "rotations": 0,
        "draw": draw
    }


def halfcircle(radius):
    # relative arc
    def draw(arc_element):
        radius = arc_element["radius"]
        rotations = arc_element["rotations"]
        x_angle = (rotations % 4) * 90
        end_point = ( 2 * radius, 0 )
        (end_x, end_y) = rotateClockwise(end_point, rotations)
        return "a{},{} {} 0,0 {},{}".format(radius, radius, x_angle, end_x, end_y)

    return {
        "type": "arc",
        "radius": radius,
        "rotations": 0,
        "draw": draw
    }


def rotateClockwise((x,y), rotations):
    coords = (x,y)
    for n in range(0, rotations):
        oldx, oldy = coords
        coords = (-oldy, oldx)
    return coords


def transform(directives, rotations, (translation_x, translation_y)):
    def single_directive(directive):
        (origin_x, origin_y) = directive["origin"]
        (x, y) = rotateClockwise((origin_x, origin_y), rotations)
        origin = (x + translation_x, y + translation_y)
        for elem in directive["elements"]:
            elem["rotations"] += rotations

        return {
            "origin": origin,
            "elements": directive["elements"]
        }

    return list(map(single_directive, directives))


def drawS(XYstring):         # Draw lines from a list
    name='part'
    style = { 'stroke': '#000000', 'fill': 'none' }
    drw = {'style':simplestyle.formatStyle(style),inkex.addNS('label','inkscape'):name,'d':XYstring}
    inkex.etree.SubElement(parent, inkex.addNS('path','svg'), drw )
    return


# Each side is processed as starting from left and progressing to right, transformation to faces is done outside this fn
#       root startOffset endOffset tabVec length  direction  isTab
# tabInfo is a dict { self: [ TOP, MALE, FEMALE ], left: [same], right: [same] }
# PLAIN means this is a top edge, and should not be tabbed (except in corners when that edge is FEMALE)
# MALE means this edge should have tabs at corners, (unless neighboring edge of the face is FEMALE)
# FEMALE means this edge should have holes at corners.

def g_side(edge_node, part_node, nomTab, indentradius, (depth, cut_length, gap_length, sep_distance)):
    part = part_node.value
    length = part["length"]

    divs=int(length/nomTab)  # divisions
    if not divs%2: divs-=1   # make divs odd
    divs=float(divs)
    gapWidth=tabWidth=length/divs

    # kerf correction
    gapWidth-=correction
    tabWidth+=correction
    first=correction/2

    leftTab = NO_EDGE
    rightTab = NO_EDGE
    if part.prev is None:
        left_edge = edge_node.prev
        if left_edge is None:
            left_edge = edge_node.next
            while left_edge.next is not None:
                left_edge = left_edge.next
        leftTab = edge_node.last.value["tabs"]
    if part.next is None:
        right_edge = edge_node.next
        if right_edge is None:
            right_edge = edge_node.prev
            while right_edge.prev is not None:
                right_edge = right_edge.prev
        rightTab = right_edge.first.value["tabs"]

    thisTab = part_node.value["tabs"]

    if thisTab is HINGE_FEMALE:
        start_y = thickness
        dirs = [{"origin": (0,start_y), "elements": [line(length, 0)]}]
        dirs.extend(living_hinge_cuts(length, start_y, depth-thickness, cut_length, gap_length, sep_distance))
        return dirs


    if thisTab is MALE:
        start_y = 0
        if leftTab in [FEMALE, HINGE_FEMALE]:
            start_x = thickness
        else:
            start_x = 0
    else:
        start_y = thickness
        start_x = thickness
        if leftTab is MALE:
            start_x = 0


    draw_directives = {
        "origin": (start_x,start_y),
        "elements": []
    }

    if thisTab is TOP:
        if indentradius > 0:
            len_to_indent = length / 2 - start_x - indentradius
            draw_directives["elements"].append(line(len_to_indent,0))
            draw_directives["elements"].append(halfcircle(indentradius))
            endOffset = 0 if rightTab is MALE else thickness
            len_to_end = length / 2 - endOffset - indentradius
            draw_directives["elements"].append(line(len_to_end,0))

        else:
            endOffset = 0 if rightTab is MALE else thickness
            draw_directives["elements"].append(line(length - start_x - endOffset,0))
        return [draw_directives]

    currently_male_tab = True if thisTab is MALE else False
    for n in range(1,int(divs)):
        if not currently_male_tab:
            dx = gapWidth
            dy = -thickness
            currently_male_tab = True
        else:
            dx = tabWidth
            dy = thickness
            currently_male_tab = False

        if n is 1:
            (sx, sy) = draw_directives["origin"]
            dx = dx - sx + first

        if n is int(divs):
            dy = 0
        draw_directives["elements"].extend([line(dx, 0), line(0, dy)])

    endOffset = thickness if tabInfo["right"] in [NO_EDGE, FEMALE, HINGE_FEMALE] else 0
    draw_directives["elements"].append( line( (gapWidth if not currentlyTab else tabWidth) - endOffset, 0))

    return [draw_directives]


def living_hinge_cuts(hinge_length, start_y, hinge_width, cut_line_len, cut_line_vert_spacing, cut_line_horiz_spacing):
    """
    Return a list of cut lines as dicts. Each dict contains the end points for one cut line.
    [{x1, y1, x2, y2}, ... ]

    Parameters
    x, y: the coordinates of the lower left corner of the bounding rect
    dx, dy: width and height of the bounding rect
    l: the nominal length of a cut line
    d: the separation between cut lines in the y-direction
    dd: the nominal separation between cut lines in the x-direction

    l will be adjusted so that there is an integral number of cuts in the y-direction.
    dd will be adjusted so that there is an integral number of cuts in the x-direction.
    """
    draw_directives = []

    # use l as a starting guess. Adjust it so that we get an integer number of cuts in the y-direction
    # First compute the number of cuts in the y-direction using l. This will not in general be an integer.
    p = (hinge_width - cut_line_vert_spacing) / (cut_line_vert_spacing + cut_line_len)

    #round p to the nearest integer
    p = round(p)
    #compute the new l that will result in p cuts in the y-direction.
    cut_line_len = (hinge_width - cut_line_vert_spacing) / p - cut_line_vert_spacing

    # use dd as a starting guess. Adjust it so that we get an even integer number of cut lines in the x-direction.
    p = hinge_length / cut_line_horiz_spacing
    p = round(p)
    if p % 2 == 1:
        p = p + 1
    cut_line_horiz_spacing = hinge_length / p

    #
    # Column A cuts
    #
    currx = 0
    donex = False
    while not donex:
        doney = False
        starty = start_y
        endy = (cut_line_len + cut_line_vert_spacing) / 2.0
        while not doney:
            cut_len = min(cut_line_len, endy)
            if endy >= hinge_width:
                cut_len -= (endy - hinge_width)
            # Add the end points of the line
            draw_directives.append({'origin' : (currx, starty), 'elements': [line(0, cut_len)] })
            starty = endy + cut_line_vert_spacing
            endy = starty + cut_line_len
            if starty >= hinge_width:
                doney = True
        currx = currx + cut_line_horiz_spacing * 2.0
        if currx - hinge_length > cut_line_horiz_spacing:
            donex = True
    #
    #Column B cuts
    #
    currx = cut_line_horiz_spacing
    donex = False
    while not donex:
        cut_len = cut_line_len
        doney = False
        starty = start_y + cut_line_vert_spacing
        endy = starty + cut_line_len
        while not doney:
            if endy >= hinge_width:
                cut_len -= (endy-hinge_width)
            # create a line
            draw_directives.append({'origin' : (currx, starty), 'elements': [line(0, cut_len)] })
            starty = endy + cut_line_vert_spacing
            endy = starty + cut_line_len
            if starty >= hinge_width:
                doney = True
        currx = currx + cut_line_horiz_spacing * 2.0
        if currx > hinge_length:
            donex = True

    return draw_directives


if __name__ == "__main__":
    # Create effect instance and apply it.
    effect = BoxMaker()
    effect.affect()

