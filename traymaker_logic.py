
from llist import dllist
from math import pi as PI

class TrayLaserCut():
    global FEMALE, MALE, HINGE_FEMALE, TOP, NO_EDGE

    FEMALE = "FEMALE"
    MALE = "MALE"
    HINGE_FEMALE = "HINGE_FEMALE"
    TOP = "TOP"
    NO_EDGE = "NO_EDGE"

    def __init__(self, options, unittouu, errorFn):
        self.options = options
        self.unittouu = unittouu # Function reference to inkex-dependent conversion function.
        self.errorFn = errorFn

        self.thickness = self.options["thickness"]
        self.nom_tab = self.options["nomTab"]
        self.spacing = self.options["spacing"]
        self.kerf = self.options["kerf"]
        self.indentradius = self.options["indentradius"]
        self.clearance = self.options["clearance"]
        self.cut_length = self.options["cut_length"]
        self.gap_length = self.options["gap_length"]
        self.sep_distance = self.options["sep_distance"]
        self.correction = self.kerf - self.clearance

    def draw(self, pieces):
        # layout format:(rootx),(rooty),Xlength,Ylength,tabInfo
        # root= (spacing,X,Y,Z) * values in tuple
        # tabInfo= <abcd> 0=holes 1=tabs
        hinge_radius=self.unittouu("6mm")
        empty_space=self.unittouu("10mm")
        error = ""

        all_directives = []
        pieceDirectives = []

        for piece in pieces:
            piece["edges"] = dllist(piece["edges"])
            for edge in piece["edges"]:
                edge["parts"] = dllist(edge["parts"])


            edge_node = piece["edges"].first

            while edge_node is not None:
                edge = edge_node.value

                translation_x, translation_y = edge["translation"]
                rotation = edge["rotation"]

                part_node = edge["parts"].first
                while part_node is not None:
                    x_part_offset = 0
                    prev_part = part_node.prev
                    while prev_part is not None:
                        x_part_offset += prev_part.value["length"]
                        prev_part = prev_part.prev

                    directives = self.g_side(edge_node, part_node)
                    directives = self.transform(directives, 0, (x_part_offset, 0))
                    directives = self.transform(directives, rotation, (translation_x, translation_y))
                    pieceDirectives.extend(directives)
                    part_node = part_node.next

                edge_node = edge_node.next

            piece_x, piece_y = piece["offset"]
            for directive in pieceDirectives:
                (x, y) = directive["origin"]
                cmds = "M {} {} ".format(x+piece_x, y+piece_y)
                for elem in directive["elements"]:
                    cmds += elem["draw"](elem)
                all_directives.append(cmds)

        if error:
            self.errorFn('Warning: Box may be impractical')
            return ""
        else:
            return all_directives



    def line(self, x, y):
        def draw(line_element):
            (x,y) = line_element["coords"]
            (x,y) = self.rotateClockwise((x,y), line_element["rotations"])
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
            (end_x, end_y) = self.rotateClockwise(end_point, rotations)
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
            (x, y) = self.rotateClockwise((origin_x, origin_y), rotations)
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

    def g_side(self, edge_node, part_node):
        nomTab = self.nom_tab
        depth = edge_node.value["depth"]

        part = part_node.value
        length = part["length"]

        divs=int(length/nomTab)  # divisions
        if not divs%2: divs-=1   # make divs odd
        divs=float(divs)
        gapWidth=tabWidth=length/divs

        # kerf correction
        gapWidth -= self.correction
        tabWidth += self.correction
        first = self.correction/2

        leftTab = NO_EDGE
        rightTab = NO_EDGE
        if part_node.prev is None:
            left_edge = edge_node.prev
            if left_edge is None:
                left_edge = edge_node.next
                while left_edge.next is not None:
                    left_edge = left_edge.next
            leftTab = left_edge.value["parts"].last.value["tabs"]
        if part_node.next is None:
            right_edge = edge_node.next
            if right_edge is None:
                right_edge = edge_node.prev
                while right_edge.prev is not None:
                    right_edge = right_edge.prev
            rightTab = right_edge.value["parts"].first.value["tabs"]

        thisTab = part["tabs"]

        if thisTab is HINGE_FEMALE:
            start_y = self.thickness
            dirs = [{"origin": (0,start_y), "elements": [self.line(length, 0)]}]
            dirs.extend(self.living_hinge_cuts(length, start_y, depth-self.thickness, self.cut_length, self.gap_length, self.sep_distance))
            return dirs


        if thisTab is MALE:
            start_y = -self.thickness
            if leftTab in [FEMALE, HINGE_FEMALE]:
                start_x = 0
            else:
                start_x = -self.thickness
        else:
            start_y = 0
            start_x = 0
            if leftTab is MALE:
                start_x = -self.thickness


        draw_directives = {
            "origin": (start_x,start_y),
            "elements": []
        }

        if thisTab is TOP:
            if self.indentradius > 0:
                i_rad = self.indentradius
                len_to_indent = length / 2 - start_x - i_rad
                draw_directives["elements"].append(self.line(len_to_indent,0))
                draw_directives["elements"].append(self.halfcircle(i_rad))
                endOffset = 0 if rightTab is MALE else self.thickness
                len_to_end = length / 2 - endOffset - i_rad
                draw_directives["elements"].append(self.line(len_to_end,0))

            else:
                endTab = self.thickness if rightTab is MALE else 0
                draw_directives["elements"].append(self.line(length - start_x + endTab,0))
            return [draw_directives]

        currently_male_tab = True if thisTab is MALE else False
        for n in range(1,int(divs)):
            if not currently_male_tab:
                dx = gapWidth
                dy = -self.thickness
                currently_male_tab = True
            else:
                dx = tabWidth
                dy = self.thickness
                currently_male_tab = False

            if n is 1:
                (sx, sy) = draw_directives["origin"]
                dx = dx - sx + first

            if n is int(divs):
                dy = 0
            draw_directives["elements"].extend([self.line(dx, 0), self.line(0, dy)])

        endOffset = self.thickness if rightTab in [NO_EDGE, FEMALE, HINGE_FEMALE] else 0
        draw_directives["elements"].append( self.line( (gapWidth if not currently_male_tab else tabWidth) - endOffset, 0))

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
                draw_directives.append({'origin' : (currx, starty), 'elements': [self.line(0, cut_len)] })
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
                draw_directives.append({'origin' : (currx, starty), 'elements': [ self.line(0, cut_len)] })
                starty = endy + cut_line_vert_spacing
                endy = starty + cut_line_len
                if starty >= hinge_width:
                    doney = True
            currx = currx + cut_line_horiz_spacing * 2.0
            if currx > hinge_length:
                donex = True

        return draw_directives
