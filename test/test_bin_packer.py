from rectpack import newPacker, float2dec


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

