
from llist import dllist
from math import pi as PI
import json

class TrayLaserCut():
    global FEMALE, MALE, HINGE_FEMALE, TOP, NO_EDGE, END_HALF_TAB, START_HALF_TAB

    FEMALE = "FEMALE"
    MALE = "MALE"
    HINGE_FEMALE = "HINGE_FEMALE"
    TOP = "TOP"
    NO_EDGE = "NO_EDGE"
    END_HALF_TAB = "END_HALF_TAB"
    START_HALF_TAB = "START_HALF_TAB"

    def __init__(self, options, errorFn):
        self.options = options
        self.errorFn = errorFn

        self.uconv = self.options["uconv"] # Conversion rate from 1 <unit> to drawing units.
        self.nom_tab = self.options["nomTab"]
        self.spacing = self.options["spacing"]
        self.kerf = self.options["kerf"]
        self.clearance = self.options["clearance"]
        self.cut_length = self.options["cut_length"]
        self.gap_length = self.options["gap_length"]
        self.sep_distance = self.options["sep_distance"]
        self.correction = self.kerf - self.clearance

        self.indentradius = 0



    def max_thickness(self, piece):
        if not list(filter(lambda edge: "opposite" in edge, piece["edges"])):
            return 0
        return max(map(lambda edge: edge["opposite"]["thickness"],
                filter(lambda edge: "opposite" in edge, piece["edges"])))


    def draw(self, pieces, thickness):
        error = ""

        all_directives = []
        cumul_y_piece_offset = 0

        filtered_pieces = list(filter(lambda piece: piece["thickness"] == thickness, pieces))
        max_width = max(map(lambda piece: piece["width"], filtered_pieces))

        current_row_max_height = 0
        cumul_x_piece_offset = 0
        for piece in filtered_pieces:
            pieceDirectives = []
            x_piece_offset = self.max_thickness(piece) + 1

            if "edges" not in piece:
                continue

            piece["edges"] = dllist(piece["edges"])
            for edge in piece["edges"]:
                edge["parts"] = dllist(edge["parts"])

            edge_node = piece["edges"].first

            if cumul_x_piece_offset + piece["width"] > max_width:
                cumul_x_piece_offset = 0
                cumul_y_piece_offset += current_row_max_height
                current_row_max_height = 0

            if cumul_x_piece_offset == 0:
                if "opposite" in edge_node.value:
                    cumul_y_piece_offset += edge_node.value["opposite"]["thickness"] + 1
                else:
                    cumul_y_piece_offset += 1

            edge_translation_x = cumul_x_piece_offset
            edge_translation_y = 0
            while edge_node is not None:
                edge = edge_node.value
                edge_directives = []

                rotation = edge["rotation"]

                part_node = edge["parts"].first
                while part_node is not None:
                    x_part_offset = 0
                    prev_part = part_node.prev
                    while prev_part is not None:
                        x_part_offset += prev_part.value["length"]
                        prev_part = prev_part.prev

                    part_directives = self.g_side(edge_node, part_node)
                    edge_directives.extend(self.transform(part_directives, 0, (x_part_offset, 0)))
                    part_node = part_node.next

                edge_directives.extend(self.face_path(piece, edge_node))
                directives = self.transform(edge_directives, rotation, (edge_translation_x, edge_translation_y))
                pieceDirectives.extend(directives)

                edge_node = edge_node.next
                if rotation % 2 == 0:
                    edge_translation_x += piece["width"] * (1-rotation)
                else:
                    edge_translation_y += piece["height"] * (2-rotation)

            commands = []
            for directive in pieceDirectives:
                (x, y) = directive["origin"]
                cmds = "M {} {} ".format(self.uconv * (x+x_piece_offset), self.uconv * (y+cumul_y_piece_offset))
                for elem in directive["elements"]:
                    cmds += elem["draw"](elem)
                commands.append(cmds)
            all_directives.append({"cut": commands})

            if current_row_max_height < piece["height"] + self.max_thickness(piece) + 1:
                current_row_max_height = piece["height"] + self.max_thickness(piece) + 1

            cumul_x_piece_offset += piece["width"] + 2*(self.max_thickness(piece) + 1)

        if error:
            self.errorFn('Warning: Box may be impractical')
            return ""
        else:
            return all_directives



    def line(self, x, y):
        def draw(line_element):
            (x,y) = line_element["coords"]
            (x,y) = self.rotateClockwise((x,y), line_element["rotations"])
            return "l {} {} ".format(x * self.uconv, y * self.uconv)

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
            return "a {},{} {} 0,0 {},{} ".format(radius * self.uconv, radius * self.uconv,
                                                x_angle, end_x * self.uconv, end_y * self.uconv)

        return {
            "type": "arc",
            "radius": radius,
            "rotations": 0,
            "draw": draw
        }

    def cubic_bezier_corner(self, end_point_rel, corner_rel):
        def draw(cubic_bezier):
            end_point = cubic_bezier["end_point_rel"]
            corner = cubic_bezier["corner_rel"]
            rotations = cubic_bezier["rotations"]
            (end_x, end_y) = self.rotateClockwise(end_point, rotations)
            (corner_x, corner_y) = self.rotateClockwise(corner, rotations)

            (end_x, end_y) = (end_x * self.uconv, end_y * self.uconv)
            (corner_x, corner_y) = (corner_x * self.uconv, corner_y * self.uconv)

            return "c {},{} {},{} {},{}".format(corner_x, corner_y, corner_x, corner_y, end_x, end_y)

        return {
            "type": "cubic_bezier",
            "rotations": 0,
            "end_point_rel": end_point_rel,
            "corner_rel": corner_rel,
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


        part = part_node.value
        length = part["length"]

        nomTab = self.nom_tab
        divs=int(length/nomTab)  # divisions

        if not divs%2: divs-=1   # make divs odd
        divs=float(divs)
        if divs > 9:
            divs = 9.0
        if divs < 3:
            divs = 3.0
        gapWidth=tabWidth=length/divs

        # kerf correction
        gapWidth -= self.correction
        tabWidth += self.correction
        first = self.correction/2.0

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

        if thisTab in [END_HALF_TAB, START_HALF_TAB]:
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
                            self.line(part_node.value["length"]/2.0-start_x, 0),
                            self.line(0, thickness),
                            self.line(part_node.value["length"]/2.0+end_tab, 0)
                        ]}
                return [dirs]
            if thisTab in END_HALF_TAB:
                dirs = {"origin": (start_x, 0),
                        "elements": [
                            self.line(part_node.value["length"]/2.0-start_x, 0),
                            self.line(0, -thickness),
                            self.line(part_node.value["length"]/2.0+end_tab, 0)
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
            if leftTab in [MALE, END_HALF_TAB]:
                start_x = -left_edge.value["opposite"]["thickness"]

        if "notch_depth" in part:
            if part["tabs"] is not MALE or leftTab is not MALE or rightTab is not MALE:
                raise BaseException("Invalid use of notches, must be MALE-MALE-MALE piece")
            draw_directives = {
                "origin": (start_x, start_y+part["notch_depth"]),
                "elements": [
                    self.line(left_edge.value["opposite"]["thickness"], 0),
                    self.line(0, -part["notch_depth"])
                ]
            }
            start_x = start_x + left_edge.value["opposite"]["thickness"]
        else:
            draw_directives = {
                "origin": (start_x, start_y),
                "elements" : []
            }

        if thisTab is TOP:
            if "indent" in part and part["indent"]["radius"] > 0:
                indent_radius = part["indent"]["radius"]
                indent_x_offset = part["indent"]["offset"]
                end_tab = nextnode(edge_node).value["opposite"]["thickness"] if rightTab in [START_HALF_TAB, MALE] else 0
                len_to_end = length - indent_radius * 2 - indent_x_offset + end_tab
                draw_directives["elements"].extend([
                    self.line(indent_x_offset-start_x, 0),
                    self.halfcircle(indent_radius),
                    self.line(len_to_end, 0)])
            else:
                end_tab = nextnode(edge_node).value["opposite"]["thickness"] if rightTab in [START_HALF_TAB, MALE] else 0
                if "pin_height" in part_node.value and part_node.value["pin_height"] > 0:

                    draw_directives["elements"].append(self.line(0, -part_node.value["pin_height"]))
                    draw_directives["elements"].append(self.line(left_edge.value["opposite"]["thickness"], 0))
                    draw_directives["elements"].append(self.line(0, part_node.value["pin_height"]))
                    draw_directives["elements"].append(self.line(length, 0))
                    if end_tab > 0:
                        draw_directives["elements"].append(self.line(0, -part_node.value["pin_height"]))
                        draw_directives["elements"].append(self.line(left_edge.value["opposite"]["thickness"], 0))
                        draw_directives["elements"].append(self.line(0, part_node.value["pin_height"]))
                else:
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
                dx = dx - start_x + first

            if n is int(divs):
                dy = 0
            draw_directives["elements"].extend([self.line(dx, 0), self.line(0, dy)])

        end_tab = right_edge.value["opposite"]["thickness"] if rightTab in [MALE, START_HALF_TAB] else 0
        part_width = (gapWidth if not currently_male_tab else tabWidth) + end_tab

        if "notch_depth" in part:
            draw_directives["elements"].extend([
                self.line(part_width - right_edge.value["opposite"]["thickness"], 0),
                self.line(0, part["notch_depth"]),
                self.line(right_edge.value["opposite"]["thickness"], 0)
            ])
        else:
            draw_directives["elements"].append(self.line(part_width, 0))

        return [draw_directives]

    def compute_male_tabs(self, length, holes=False):
        nomTab = self.nom_tab
        divs=int(length/nomTab)  # divisions
        if not divs%2: divs-=1   # make divs odd
        if divs > 9:
            divs = 9
        if divs < 3:
            divs = 3
        gapWidth=tabWidth=length/float(divs)

        if holes:
            temp = gapWidth
            gapWidth = tabWidth
            tabWidth = temp

        first = self.correction/2.0
        tabs = [{
            "offset": 0,
            "length": tabWidth + first
        }]
        for index in range(0, (divs-1)/2):
            tabs.append({
                "offset": gapWidth,
                "length": tabWidth
            })
        return tabs

    def invert_tabs(self, tabs):
        tablist = dllist(tabs)
        offset = tablist.first.value["length"]
        tab = tablist.first.next
        female_tabs = []
        while tab is not None:
            length = tab.value["offset"]
            female_tabs.append({
                "offset": offset,
                "length": length
            })
            offset = tab.value["length"]
            tab = tab.next
        return female_tabs

    def face_path(self, piece, edge_node):
        edge = edge_node.value

        depth = piece["height"]
        if edge["rotation"] % 2 == 1:
            depth = piece["width"]

        def draw_shapes(part_length, shape, x_offset, y_offset, width):
            directives = []
            if shape is START_HALF_TAB:
                directive = {"origin": (x_offset, y_offset), "elements": [
                    self.line(0, part_length/2.0),
                    self.line(width, 0),
                    self.line(0, -part_length/2.0),
                    self.line(-width, 0)
                ]}
                directives.append(directive)
            elif shape is END_HALF_TAB:
                directive = {"origin": (x_offset, part_length/2.0 + y_offset), "elements": [
                    self.line(0, part_length/2.0),
                    self.line(width, 0),
                    self.line(0, -part_length/2.0),
                    self.line(-width, 0)
                ]}
                directives.append(directive)
            elif shape is FEMALE:
                tabs = self.invert_tabs(self.compute_male_tabs(part_length, holes=True))
                total_y_offset = y_offset
                for tab in tabs:
                    total_y_offset += tab["offset"]
                    directive = {"origin": (x_offset, total_y_offset), "elements": [
                        self.line(0, tab["length"]),
                        self.line(width, 0),
                        self.line(0, -tab["length"]),
                        self.line(-width, 0)
                    ]}
                    directives.append(directive)
                    total_y_offset += tab["length"]
            elif shape is "C_BEZIER_RECT":
                directives.append({"origin": (x_offset + width/2.0, y_offset),
                             "elements": [
                                 self.cubic_bezier_corner((width/2.0, part_length/2.0), (width/2.0, 0)),
                                 self.cubic_bezier_corner((-width/2.0, part_length/2.0), (0, part_length/2.0)),
                                 self.cubic_bezier_corner((-width/2.0, -part_length/2.0), (-width/2.0, 0)),
                                 self.cubic_bezier_corner((width/2.0, -part_length/2.0), (0, -part_length/2.0)),
                             ]
                             })
            else:
                self.errorFn("Unsupported")
            return directives

        if "holes" not in edge:
            return []
        x_offset = 0
        directives = []
        for hole_part in edge["holes"]:
            x_offset += hole_part["offset"]
            width = None
            if "shape" in hole_part:
                if "width" not in hole_part:
                    width = hole_part["opposite"]["thickness"]
                else:
                    width = hole_part["width"]
                shape = hole_part["shape"]
                part_length = depth
                if "length" in hole_part:
                    part_length = hole_part["length"]
                directives.extend(draw_shapes(part_length, shape, x_offset, 0, width))

            elif "parts" in hole_part:
                y_offset = 0
                for part in hole_part["parts"]:
                    if "width" not in part:
                        width = hole_part["opposite"]["thickness"]
                    else:
                        width = part["width"]
                    shape = part["shape"]
                    part_length = part["length"]
                    if "offset" in part:
                        y_offset += part["offset"]
                    directives.extend(draw_shapes(part_length, shape, x_offset, y_offset, width))
                    y_offset += part_length

            if not width:
                self.errorFn("{}".format(hole_part))
            x_offset += width
        return directives