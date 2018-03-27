
from llist import dllist
from math import pi as PI

class TrayLaserCut():
    global FEMALE, MALE, HINGE_FEMALE, TOP, NO_EDGE, END_HALF_TAB, START_HALF_TAB

    FEMALE = "FEMALE"
    MALE = "MALE"
    HINGE_FEMALE = "HINGE_FEMALE"
    TOP = "TOP"
    NO_EDGE = "NO_EDGE"
    END_HALF_TAB = "END_HALF_TAB"
    START_HALF_TAB = "START_HALF_TAB"

    def __init__(self, options, unittouu, errorFn):
        self.options = options
        self.unittouu = unittouu # Function reference to inkex-dependent conversion function.
        self.errorFn = errorFn

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
        error = ""

        all_directives = []
        pieceDirectives = []

        for piece in pieces:
            if "edges" not in piece:
                continue

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

                pieceDirectives.extend(self.face_path(edge_node))
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
        def prevnode(node):
            if node.prev is not None:
                return node.prev
            while node.next is not None:
                node = node.next
            return node

        def nextnode(node):
            if node.next is not None:
                return node.next
            while node.prev is not None:
                node = node.prev
            return node

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
        left_edge = prevnode(edge_node)
        right_edge = nextnode(edge_node)
        if part_node.prev is None:
            leftTab = left_edge.value["parts"].last.value["tabs"]
        if part_node.next is None:
            rightTab = right_edge.value["parts"].first.value["tabs"]

        thisTab = part["tabs"]

        start_x = 0
        start_y = 0
        if thisTab is HINGE_FEMALE:
            start_y = 0
            dirs = [{"origin": (0,start_y), "elements": [self.line(length, 0)]}]
         #   dirs.extend(self.living_hinge_cuts(length, start_y, depth-self.thickness, self.cut_length, self.gap_length, self.sep_distance))
            return dirs

        elif thisTab in [END_HALF_TAB, START_HALF_TAB]:
            start_x = 0
            end_tab = 0
            if leftTab in [MALE, END_HALF_TAB]:
                start_x = -left_edge.value["opposite"]["thickness"]
            if rightTab in [MALE, START_HALF_TAB]:
                end_tab = right_edge.value["opposite"]["thickness"]
            thickness = edge_node.value["opposite"]["thickness"]
            if thisTab in START_HALF_TAB:
                dirs = {"origin": (start_x, -thickness),
                        "elements": [
                            self.line(part_node.value["length"]/2-start_x, 0),
                            self.line(0, thickness),
                            self.line(part_node.value["length"]/2+end_tab, 0)
                        ]}
                return [dirs]
            if thisTab in END_HALF_TAB:
                dirs = {"origin": (start_x, 0),
                        "elements": [
                            self.line(part_node.value["length"]/2-start_x, 0),
                            self.line(0, -thickness),
                            self.line(part_node.value["length"]/2+end_tab, 0)
                        ]}
                return [dirs]
        elif thisTab is MALE:
            start_y = -edge_node.value["opposite"]["thickness"]
            if leftTab in [FEMALE, HINGE_FEMALE, TOP, NO_EDGE, START_HALF_TAB]:
                start_x = 0
            else:
                start_x = -left_edge.value["opposite"]["thickness"]
        elif thisTab in [FEMALE, TOP]:
            start_y = 0
            start_x = 0
            if leftTab is MALE:
                start_x = -left_edge.value["opposite"]["thickness"]


        draw_directives = {
            "origin": (start_x,start_y),
            "elements": []
        }

        if thisTab is TOP:
            if self.indentradius > 0:
                i_rad = self.indentradius
                len_to_indent = length / 2 - start_x - i_rad
                draw_directives["elements"].append(self.line(len_to_indent, 0))
                draw_directives["elements"].append(self.halfcircle(i_rad))
                end_tab = nextnode(edge_node).value["opposite"]["thickness"] if rightTab is [START_HALF_TAB, MALE] else 0
                len_to_end = length / 2 + end_tab - i_rad
                draw_directives["elements"].append(self.line(len_to_end, 0))

            else:
                end_tab = nextnode(edge_node).value["opposite"]["thickness"] if rightTab in [START_HALF_TAB, MALE] else 0
                draw_directives["elements"].append(self.line(length - start_x + end_tab, 0))
            return [draw_directives]

        currently_male_tab = True if thisTab is MALE else False
        for n in range(1,int(divs)):
            if not currently_male_tab:
                dx = gapWidth
                dy = -edge_node.value["opposite"]["thickness"]
                currently_male_tab = True
            else:
                dx = tabWidth
                dy = edge_node.value["opposite"]["thickness"]
                currently_male_tab = False

            if n is 1:
                (sx, sy) = draw_directives["origin"]
                dx = dx - sx + first

            if n is int(divs):
                dy = 0
            draw_directives["elements"].extend([self.line(dx, 0), self.line(0, dy)])

        end_tab = right_edge.value["opposite"]["thickness"] if rightTab in [MALE, START_HALF_TAB] else 0
        part_width = (gapWidth if not currently_male_tab else tabWidth) + end_tab

        draw_directives["elements"].append( self.line(part_width, 0))

        return [draw_directives]


    def face_path(self, edge_node):
        edge = edge_node.value
        depth = edge["depth"]
        if "holes" not in edge:
            return []
        x_offset = 0
        directives = []
        for hole_part in edge["holes"]:
            x_offset += hole_part["offset"]
            width = hole_part["width"]
            shape = hole_part["shape"]
            if shape is START_HALF_TAB:
                directive = {"origin": (x_offset, 0), "elements": []}
            elif shape is END_HALF_TAB:
                directive = {"origin": (x_offset, depth/2), "elements": []}
            directive["elements"].append(self.line(0, depth/2))
            directive["elements"].append(self.line(width, 0))
            directive["elements"].append(self.line(0, -depth/2))
            directive["elements"].append(self.line(-width, 0))
            directives.append(directive)
            x_offset += width
        return directives


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
