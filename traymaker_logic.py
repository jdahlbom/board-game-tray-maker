
from llist import dllist
from math import pi as PI

class TrayLaserCut():
    global FEMALE, MALE, HINGE_FEMALE, TOP

    FEMALE = "FEMALE"
    MALE = "MALE"
    HINGE_FEMALE = "HINGE_FEMALE"
    TOP = "TOP"


    def __init__(self, options, unittouu):
        self.options = options
        self.unittouu = unittouu # Function reference to inkex-dependent conversion function.

        self.X = self.options["X"]
        self.Y = self.options["Y"]
        self.Z = self.options["Z"]
        self.thickness = self.options["thickness"]
        self.nom_tab = self.options["nom_tab"]
        self.spacing = self.options["spacing"]
        self.kerf = self.options["kerf"]
        self.empty_space = self.options["empty_space"]
        self.indentradius = self.options["indentradius"]
        self.clearance = self.options["clearance"]
        self.cut_length = self.options["cut_length"]
        self.gap_length = self.options["gap_length"]
        self.sep_distance = self.options["sep_distance"]


    def draw(self):
        # layout format:(rootx),(rooty),Xlength,Ylength,tabInfo
        # root= (spacing,X,Y,Z) * values in tuple
        # tabInfo= <abcd> 0=holes 1=tabs
        hinge_radius=self.unittouu("6mm")
        empty_space=self.unittouu("10mm")
        pieces = [
            {
                "width": self.X,
                "length": self.Y,
                "edges": dllist([
                    {
                        "parts": dllist([
                            {"tabs": FEMALE, "length": self.X-hinge_radius*PI/2-empty_space},
                            {"tabs": HINGE_FEMALE, "length": hinge_radius*PI/2},
                            {"tabs": FEMALE, "length": empty_space}]),
                        "translation": (0, 0),
                        "rotation": 0,
                        "depth": self.Y
                    },
                    {
                        "parts": dllist([{"tabs": TOP, "length": self.Y}]),
                        "translation": (self.X, 0),
                        "rotation": 1,
                        "depth": self.X
                    },
                    {
                        "parts": dllist([
                            {"tabs": FEMALE, "length": empty_space},
                            {"tabs": TOP, "length": hinge_radius*PI/2},
                            {"tabs": FEMALE, "length": self.X-empty_space-hinge_radius*PI/2}]),
                        "translation": (self.X, self.Y),
                        "rotation": 2,
                        "depth": self.Y
                    },
                    {
                        "parts": dllist([{"tabs": FEMALE, "length": self.Y}]),
                        "translation": (0, self.Y),
                        "rotation": 3,
                        "depth": self.X
                    }
                ]),
                "offset": ( self.Z+self.spacing*2, self.Z+self.spacing*2 )
            }]

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


        for piece in pieces: # generate and draw each piece of the box
            pieceDirectives = []

            for edge_node in piece["edges"]:
                edge = edge_node.value

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


    def line(self, x, y):
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


    def halfcircle(self, radius):
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


    def rotateClockwise(self, (x,y), rotations):
        coords = (x,y)
        for n in range(0, rotations):
            oldx, oldy = coords
            coords = (-oldy, oldx)
        return coords


    def transform(self, directives, rotations, (translation_x, translation_y)):
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




    # Each side is processed as starting from left and progressing to right, transformation to faces is done outside this fn
    #       root startOffset endOffset tabVec length  direction  isTab
    # tabInfo is a dict { self: [ TOP, MALE, FEMALE ], left: [same], right: [same] }
    # PLAIN means this is a top edge, and should not be tabbed (except in corners when that edge is FEMALE)
    # MALE means this edge should have tabs at corners, (unless neighboring edge of the face is FEMALE)
    # FEMALE means this edge should have holes at corners.

    def g_side(self, edge_node, part_node, nomTab, indentradius, (depth, cut_length, gap_length, sep_distance)):
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


    def living_hinge_cuts(self, hinge_length, start_y, hinge_width, cut_line_len, cut_line_vert_spacing, cut_line_horiz_spacing):
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
