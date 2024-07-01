from rectpack import newPacker, float2dec


object_margin = 0.5


def get_packer_id(svg_object):
    return f"{svg_object['tray']}___{svg_object['thickness']}___{svg_object['id_in_tray']}"


#  Given a list of svg objects it sorts them by thickness, and then lays them out within
#  a rectangle boundary that may span several "bins", corresponding to separate cuttable boards.
def pack_objects(svg_objects, material_width_mm: 600, material_height_mm: 600):
    objects_by_id = {}
    for idx in range(len(svg_objects)):
        svg_objects[idx]['id_in_tray'] = idx
        svg_objects[idx]['packer_id'] = get_packer_id(svg_objects[idx])
        objects_by_id[svg_objects[idx]['packer_id']] = svg_objects[idx]

    unique_thicknesses = set([obj['thickness'] for obj in svg_objects])

    bins_by_thickness = {}
    for thickness in unique_thicknesses:
        packer = newPacker(rotation=False)
        matching_objects = list([obj for obj in svg_objects if obj['thickness'] == thickness])
        packer.add_bin(material_width_mm, material_height_mm, 4)
        for obj in matching_objects:
            packer.add_rect(float2dec(obj['width'] + object_margin * 2, 5),
                            float2dec(obj['height'] + object_margin * 2, 5),
                            obj['packer_id'])
        packer.pack()

        rect_list = packer.rect_list()
        bins = {}
        for rect in rect_list:
            bin_id, offset_x, offset_y, width_x, width_y, object_id = rect
            obj = objects_by_id[object_id]
            obj['packer_offset_x'] = float(offset_x) + object_margin
            obj['packer_offset_y'] = float(offset_y) + object_margin
            if bin_id not in bins:
                bins[bin_id] = list()
            bins[bin_id].append(obj)

        bins_by_thickness[f"{thickness}mm"] = bins
    return bins_by_thickness
