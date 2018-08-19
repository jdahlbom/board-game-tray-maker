from copy import deepcopy
import math
import json


def tray_def():
    return json.loads(open("gloomhaven/trays.json", "r").read())


def tray_names():
    names = []
    for tray_name, _ in tray_def().iteritems():
        names.append(tray_name)
    return names


def tray_setup(tray_name, (thickness_thick, thickness_slim), errorFn):
    trays = tray_def()

    tray = trays[tray_name]
    dimensions = tray["dimensions"]
    dims = {
        "tray.width": dimensions["width"],
        "tray.height": dimensions["height"],
        "tray.depth": dimensions["depth"]
    }
    pieces = tray["pieces"]
    new_pieces = []

    for piece in pieces:
        if "thickness" not in piece:
            continue
        if piece["thickness"] == "material.thickness.THICK":
            piece["thickness"] = thickness_thick
        elif piece["thickness"] == "material.thickness.SLIM":
            piece["thickness"] = thickness_slim


    def generate_rectangle_edges(width, height):
        return [
            {
                "rotation": 0,
                "parts": [{
                    "length": width,
                    "tabs": "TOP"
                }]
            },
            {
                "rotation": 1,
                "parts": [{
                    "length": height,
                    "tabs": "TOP"
                }]
            },
            {
                "rotation": 2,
                "parts": [{
                    "length": width,
                    "tabs": "TOP"
                }]
            },
            {
                "rotation": 3,
                "parts": [{
                    "length": height,
                    "tabs": "TOP"
                }]
            }
        ]

    def compute_angled_base_pieces(piece):
        width = piece["width"]
        base_height = piece["slot_height"]
        angle_deg = 15
        flat_height = base_height * 0.8
        angled_height = 1.0 / math.cos(angle_deg * math.pi/360) * base_height * 0.2
        return [
            {
                "name": "{}-flat".format(piece["name"]),
                "width": width,
                "height": flat_height,
                "thickness": piece["thickness"],
                "edges": generate_rectangle_edges("piece.width", "piece.height")
            },
            {
                "name": "{}-slope".format(piece["name"]),
                "width": width,
                "height": angled_height,
                "thickness": piece["thickness"],
                "edges": generate_rectangle_edges("piece.width", "piece.height")
            }
        ]

    for piece in pieces:
        if "copy_of" in piece:
            copyable = next( fpiece for fpiece in pieces if fpiece["name"] == piece["copy_of"])
            piece_name = deepcopy(piece["name"])
            copy = deepcopy(copyable)
            copy["name"] = piece_name
            new_pieces.append(copy)
        else:
            new_pieces.append(piece)

        if "number_of_copies" in piece:
            num_copies = piece["number_of_copies"]
            for i in range(1, num_copies):
                new_piece = deepcopy(piece)
                del(new_piece["number_of_copies"])
                new_piece["name"] = "{}-copy {}".format(piece["name"], i)
                new_pieces.append(new_piece)
            del(piece["number_of_copies"])

    pieces = deepcopy(new_pieces)

    new_pieces = []

    for piece in pieces:
        if "composite_type" in piece:
            if piece["composite_type"] is "angled base":
                new_pieces.extend(compute_angled_base_pieces(piece))
        else:
            new_pieces.append(piece)

    pieces = deepcopy(new_pieces)
    new_pieces = []

    for piece in pieces:
        for dim_key in ["width", "height"]:
            if piece[dim_key] in dims.keys():
                piece[dim_key] = dims[piece[dim_key]]

        piece_width = piece["width"]
        piece_height = piece["height"]

        for edge in piece["edges"]:
            for part in edge["parts"]:
                if part["length"] == "piece.width":
                    part["length"] = piece_width
                elif part["length"] == "piece.height":
                    part["length"] = piece_height

            if "opposite" in edge:
                opposite_name = edge["opposite"]
                opposite_piece = next((piece for piece in pieces if piece["name"] == opposite_name), None)
                if not opposite_piece or "thickness" not in opposite_piece:
                    errorFn("Opposite piece [{}] missing for edge [{}] in piece [{}] in tray [{}]".format(opposite_name, edge, piece["name"], tray_name))
                    continue
                edge["opposite"] = {"thickness": opposite_piece["thickness"]}
            if "holes" in edge:
                for hole in edge["holes"]:
                    if "opposite" not in hole:
                        continue
                    opposite_name = hole["opposite"]
                    opposite_piece = next((piece for piece in pieces if piece["name"] == opposite_name), None)
                    if not opposite_piece or "thickness" not in opposite_piece:
                        errorFn("Opposite piece [{}] missing for piece [{}] in tray [{}]".format(opposite_name, piece["name"], tray_name))
                        continue
                    hole["opposite"] = {"thickness": opposite_piece["thickness"]}
        new_pieces.append(piece)

    if "copies" in tray:
        copies = tray["copies"]
        all_pieces = []
        for i in range(0, copies):
            all_pieces.extend(new_pieces)
        return all_pieces

    return new_pieces

