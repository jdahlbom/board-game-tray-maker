import svg

#These NEED to be in a configuration file, not hard coded!
STROKE = 0.001
MIN_TOOTH_WIDTH = 7.0
INDENT_DEPTH = 10
KERF = 0.2
K_CORR = KERF/2.0

# When returning array of SVG draw instructions from a function, there
# should also be following information included in the top level:
# { "svg": [drawing instructions],
#   "width": number,
#   "height", number,
#   "offset_x": number,   <-- How much the starting point is from the top left corner of bounding rectangle
#   "offset_y": number,   <-- How much the starting point is from the top left corner of bounding rectangle
#   "tray_id": alphanumeric, "thickness": number }


def test_two_slot_slotted_top_edge():
    spacer_width = 2
    edge_width = 3
    content_width = 100
    depth = 40
    slots = [
        {
            'length': 48,
            'slot_properties': {
                'forbid_indent': True
            }
        },
        {
            'length': 50,
            'slot_properties': {
                'forbid_indent': True
            }
        }
    ]
    corner_toothing = True

    res = svg.generate_slotted_top_edge(slots, spacer_width, content_width, corner_toothing, edge_width, depth)

    expected = [
        f"h {edge_width}",
        f"h {slots[0]['length']}",
        f"h {K_CORR}",
        f"v {INDENT_DEPTH - K_CORR}",
        f"h {spacer_width - 2 * K_CORR}",
        f"v -{INDENT_DEPTH - K_CORR}",
        f"h {K_CORR}",
        f"h {slots[1]['length']}",
        f"h {edge_width}"
    ]
    assert(expected == res)


def test_single_column_two_slotted_edges():
    spacer_width = 2
    edge_width = 3
    content_width = 100
    depth = 30
    max_tooth_size = 10.0

    tray_spec = {
        'name': 'Test tray',
        'spacer_width': spacer_width,
        'edge_width': edge_width,
        'tray_depth': depth,
        'tray_width': content_width + 2*edge_width,  # Lets test this without the elasticity, with exactly sized content
        'tray_height': content_width + 2*edge_width,
        'columns': [
            {
                'width': content_width,
                'slots': [
                    {
                        'height': 48,
                        'forbid_indent': True
                    },
                    {
                        'height': 50,
                        'forbid_indent': True
                    }
                ]
            }
        ]
    }

    upper_left_corner = [
        f"h {K_CORR}"
    ]

    top_wall_top_edge_svg = [
        f"h {edge_width}",
        f"h {content_width}",
        f"h {edge_width}"
    ]

    upper_right_corner = [
        f"h {K_CORR} v {K_CORR}"
    ]

    tooth_depth = edge_width
    right_edge_svg = [
        f"v {max_tooth_size + K_CORR}",
        f"h {-tooth_depth}",
        f"v {max_tooth_size - 2*K_CORR}",
        f"h {tooth_depth}",
        f"v {max_tooth_size + K_CORR}"
    ]

    lower_right_corner = [
        f"v {edge_width}",
        f"v {K_CORR} h {-K_CORR}",
        f"h {-edge_width}"
    ]

    bottom_tooth_size = 100.0 / 9.0
    bottom_edge_svg = [
        f"h {-(bottom_tooth_size + K_CORR)}",
        f"v {-tooth_depth}",
        f"h {-(bottom_tooth_size - K_CORR*2)}",
        f"v {tooth_depth}",
        f"h {-(bottom_tooth_size + K_CORR*2)}",
        f"v {-tooth_depth}",
        f"h {-(bottom_tooth_size - K_CORR*2)}",
        f"v {tooth_depth}",
        f"h {-(bottom_tooth_size + K_CORR*2)}",
        f"v {-tooth_depth}",
        f"h {-(bottom_tooth_size - K_CORR*2)}",
        f"v {tooth_depth}",
        f"h {-(bottom_tooth_size + K_CORR*2)}",
        f"v {-tooth_depth}",
        f"h {-(bottom_tooth_size - K_CORR*2)}",
        f"v {tooth_depth}",
        f"h {-(bottom_tooth_size + K_CORR)}"
    ]

    lower_left_corner = [
        f"h {-edge_width}",
        f"h {-K_CORR} v {-K_CORR}",
        f"v {-edge_width}"
    ]

    left_edge_svg = [
        f"v {-(max_tooth_size + K_CORR)}",
        f"h {tooth_depth}",
        f"v {-(max_tooth_size - 2*K_CORR)}",
        f"h {-tooth_depth}",
        f"v {-(max_tooth_size + K_CORR)}"
    ]

    upper_left_corner_again = [
        f"v {-K_CORR}"
    ]

    close_path = ['z']

    whole_piece_svg = upper_left_corner +\
        top_wall_top_edge_svg +\
        upper_right_corner +\
        right_edge_svg +\
        lower_right_corner +\
        bottom_edge_svg +\
        lower_left_corner +\
        left_edge_svg +\
        upper_left_corner_again +\
        close_path

    expected = {
        'svg': whole_piece_svg,
        'width': content_width + 2 * edge_width,
        'height': depth + edge_width,
        'offset_x': 0,
        'offset_y': 0,
        'tray': 'Test tray',
        'thickness': edge_width
    }
    res = svg.generate_edges(tray_spec)
    assert(res[0] == expected)


def test_generate_floor_with_two_simple_columns():
    spacer_width = 2
    edge_width = 3
    content_width = 30

    tray_spec = {
        'name': 'Test tray',
        'spacer_width': spacer_width,
        'edge_width': edge_width,
        'tray_depth': 111,
        'tray_width': content_width + 2*edge_width,  # Lets test this without the elasticity, with exactly sized content
        'tray_height': content_width + 2*edge_width,
        'columns': [
            {
                'width': content_width,
                'slots': [
                    {
                        'height': content_width,
                        'forbid_indent': True
                    }
                ]
            },
            {
                'width': content_width,
                'slots': [
                    {
                        'height': 50,
                        'forbid_indent': True
                    }
                ]
            }
        ]
    }

    tooth_w = content_width / 3.0
    tooth_depth = edge_width

    initial_corner = [
        f"h {K_CORR}"
    ]
    top_edge = [
        f"h {tooth_w - K_CORR}",
        f"v -{tooth_depth}",
        f"h {tooth_w + K_CORR*2}",
        f"v {tooth_depth}",
        f"h {tooth_w - K_CORR}"
    ]
    top_right_corner = [
        f"h {K_CORR} v {K_CORR}",
    ]
    right_edge = [
        f"v {tooth_w - K_CORR}",
        f"h {tooth_depth}",
        f"v {tooth_w + K_CORR*2}",
        f"h -{tooth_depth}",
        f"v {tooth_w - K_CORR}"
    ]
    lower_right_corner = [
        f"v {K_CORR} h -{K_CORR}"
    ]
    bottom_edge = [
        f"h -{tooth_w - K_CORR}",
        f"v {tooth_depth}",
        f"h -{tooth_w + K_CORR*2}",
        f"v -{tooth_depth}",
        f"h -{tooth_w - K_CORR}"
    ]
    lower_left_corner = [
        f"h -{K_CORR} v -{K_CORR}"
    ]
    left_edge = [
        f"v -{tooth_w - K_CORR}",
        f"h -{tooth_depth}",
        f"v -{tooth_w + K_CORR*2}",
        f"h {tooth_depth}",
        f"v -{tooth_w - K_CORR}"
    ]
    last_corner = [
        f"v -{K_CORR}"
    ]
    close_path = [
        'z'
    ]
    expected_svg = initial_corner +\
        top_edge +\
        top_right_corner +\
        right_edge +\
        lower_right_corner +\
        bottom_edge +\
        lower_left_corner +\
        left_edge +\
        last_corner +\
        close_path

    res = svg.generate_floor(tray_spec)
    assert(res['svg'] == expected_svg)