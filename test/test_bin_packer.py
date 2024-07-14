from rectpack import newPacker, float2dec
import layout
import test.fixtures as fixtures
import math

def test_bin_packing():
    objects = [
        {
            "width": 50.0,
            "height": 30.0,
            "tray": "first",
            "thickness": 3,
            "id_in_tray": 1,
            "slots": [
                {
                    "name": "Minor Power card",
                    "y_offset": 0
                },
                {
                    "name": "Major Power card",
                    "y_offset": 30
                }
            ]
        },
        {
            "width": 30.0,
            "height": 20.0,
            "tray": "first",
            "thickness": 3,
            "id_in_tray": 2
        },
        {
            "width": 60.0,
            "height": 60.0,
            "tray": "first",
            "thickness": 3,
            "id_in_tray": 3
        },
        {
            "width": 50.0,
            "height": 50.0,
            "tray": "first",
            "thickness": 3,
            "id_in_tray": 4
        }
    ]

    def add_id(object):
        object['packer_id'] = f"{object['tray']}___{object['thickness']}___{object['id_in_tray']}"
        return object

    objects_with_id = [add_id(object) for object in objects]

    packer = newPacker()

    packer.add_bin(100, 100, 3)
    object_margin = 0.1
    for obj in objects_with_id:
        packer.add_rect(float2dec(obj['width'] + object_margin*2, 2), float2dec(obj['height'] + object_margin * 2, 2), obj['packer_id'])
    packer.pack()

    rect_list = packer.rect_list()

    # First three objects are in bin 0
    # Tuple: (bin, x_bottom_left, y_bottom_left, width, height, rectangle_id)
    assert(rect_list[0][0] == 0)
    assert(rect_list[1][0] == 0)
    assert(rect_list[2][0] == 0)
    # Fourth object should be in bin 1
    assert(rect_list[3][0] == 1)


def test_pack_objects():
    objects = fixtures.get_object_list_with_two_thicknesses_and_bins()
    result = layout.pack_objects(objects, 40 + layout.object_margin*2, 80 + 2 * layout.object_margin)
    assert(len(result["3mm"]) == 2)
    assert(len(result["1mm"]) == 1)

    object_margin = layout.object_margin
    one_mm_object = result["1mm"][0][0]
    assert(one_mm_object["packer_offset_x"] == object_margin)
    assert(one_mm_object["packer_offset_y"] == object_margin)

    three_mm_bins = result["3mm"]
    single_object_bin = three_mm_bins[0]
    assert(len(single_object_bin) == 1)
    assert(single_object_bin[0]["height"] == objects[0]["height"])

    two_object_bin = three_mm_bins[1]
    assert(len(two_object_bin) == 2)

    assert(two_object_bin[0]["packer_offset_x"] == object_margin)
    assert(two_object_bin[0]["packer_offset_y"] == object_margin)

    assert(two_object_bin[1]["packer_offset_x"] == object_margin)
    expected_y_offset = float(float2dec(2 * object_margin + two_object_bin[0]["height"], 5)) + object_margin
    assert(two_object_bin[1]["packer_offset_y"] == expected_y_offset)
    assert(two_object_bin[1]["offset_x"] == 0)


def test_four_object_layout():
    objects = fixtures.get_four_objects_to_lay_out()
    result = layout.pack_objects(objects, 400, 300)

    assert("3mm" in result)
    bins = result["3mm"]
    assert(len(bins) == 1)
    objects = bins[0]
    assert(len(objects) == 4)

    first = objects[0]
    padding = layout.object_margin
    assert(first['packer_offset_x'] == padding)
    assert(first['packer_offset_y'] == padding)
    assert(first['width'] == 98)
    assert(first['height'] == 70)

    second = objects[1]
    assert(math.isclose(second['packer_offset_x'], padding, abs_tol=0.001))
    assert(math.isclose(second['packer_offset_y'], 3 * padding + first['height'], abs_tol=0.001))
