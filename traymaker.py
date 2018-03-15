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

import sys,inkex,simplestyle,gettext
_ = gettext.gettext

TOP = 0
MALE = 1
FEMALE = 2

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
   
    # layout format:(rootx),(rooty),Xlength,Ylength,tabInfo
    # root= (spacing,X,Y,Z) * values in tuple
    # tabInfo= <abcd> 0=holes 1=tabs
    pieces = [
      {
        "width": X,
        "length": Y,
        "edges": [FEMALE, FEMALE, FEMALE, FEMALE],
        "offset": ( Z+spacing*2, Z+spacing*2 )
      },
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
      for edge in range(0, 4):

        tabInfo = {
          "self": piece["edges"][edge],
          "left": piece["edges"][(edge-1+4)%4],
          "right": piece["edges"][(edge+1)%4]
        }
        length = piece["width"] if edge % 2 == 0 else piece["length"]

        translation_x, translation_y = (0,0)

        if edge in [1, 2]:
          translation_x = piece["width"]
        if edge in [2, 3]:
          translation_y = piece["length"]

        indentradius = 0
        if "indentradius" in piece:
          indentradius = piece["indentradius"]

        directives = g_side(tabInfo, length, nomTab, indentradius)
        directives = transform(directives, edge, (translation_x, translation_y))
        pieceDirectives.append(directives)

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
  (origin_x, origin_y) = directives["origin"]
  (x, y) = rotateClockwise((origin_x, origin_y), rotations)
  origin = (x + translation_x, y + translation_y)
  for elem in directives["elements"]:
    elem["rotations"] += rotations

  return {
    "origin": origin,
    "elements": directives["elements"]
  }


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

def g_side(tabInfo, length, nomTab, indentradius):
  divs=int(length/nomTab)  # divisions
  if not divs%2: divs-=1   # make divs odd
  divs=float(divs)
  gapWidth=tabWidth=length/divs

  # kerf correction
  gapWidth-=correction
  tabWidth+=correction
  first=correction/2

  currentlyTab = True
  if tabInfo["self"] in [MALE, TOP]:
    start_y = 0
    if tabInfo["left"] is FEMALE:
      start_x = thickness
    else:
      start_x = 0
  else:
    currentlyTab = False
    start_y = thickness
    start_x = thickness if tabInfo["left"] is FEMALE else 0

  draw_directives = {
      "origin": (start_x,start_y),
      "elements": []
    }

  if tabInfo["self"] is TOP:
    if not currentlyTab:
      draw_directives["elements"].append(line(0, thickness))

    if indentradius > 0:
      len_to_indent = length / 2 - start_x - indentradius
      draw_directives["elements"].append(line(len_to_indent,0))
      draw_directives["elements"].append(halfcircle(indentradius))
      endOffset = 0 if tabInfo["right"] is MALE else thickness
      len_to_end = length / 2 - endOffset - indentradius
      draw_directives["elements"].append(line(len_to_end,0))

    else:
      endOffset = 0 if tabInfo["right"] is MALE else thickness
      draw_directives["elements"].append(line(length - start_x - endOffset,0))

  else:
    for n in range(1,int(divs)):
      if not currentlyTab:
        dx = gapWidth
        dy = -thickness
        currentlyTab = True
      else:
        dx = tabWidth
        dy = thickness
        currentlyTab = False

      if n is 1:
        (sx, sy) = draw_directives["origin"]
        dx = dx - sx + first

      draw_directives["elements"].extend([line(dx, 0),line(0, dy)])

    endOffset = thickness if tabInfo["right"] is FEMALE else 0
    draw_directives["elements"].append( line( (gapWidth if not currentlyTab else tabWidth) - endOffset, 0))

  return draw_directives


# Create effect instance and apply it.
effect = BoxMaker()
effect.affect()

