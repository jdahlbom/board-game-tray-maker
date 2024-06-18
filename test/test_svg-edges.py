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

    trayspec = {
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

    top_edge_svg = [
        f"h {edge_width}",
        f"h {trayspec['columns'][0]['slots'][0]['height']}",
        f"h {K_CORR}",
        f"v {INDENT_DEPTH - K_CORR}",
        f"h {spacer_width - 2 * K_CORR}",
        f"v -{INDENT_DEPTH - K_CORR}",
        f"h {K_CORR}",
        f"h {trayspec['columns'][0]['slots'][1]['height']}",
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
        f"v {K_CORR} h {-K_CORR}"
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
        f"h {-(bottom_tooth_size + K_CORR)}",
        f"v {-tooth_depth}"
    ]

    lower_left_corner = [
        f"h {-K_CORR} v{-K_CORR}"
    ]

    left_edge_svg = [
        f"v {-(max_tooth_size + K_CORR)}",
        f"h {tooth_depth}",
        f"v {-(max_tooth_size - 2*K_CORR)}",
        f"h {tooth_depth}",
        f"v {-(max_tooth_size + K_CORR)}"
    ]

    upper_left_corner_again = [
        f"v {-K_CORR}"
    ]

    whole_piece_svg = upper_left_corner +\
        top_edge_svg +\
        upper_right_corner +\
        right_edge_svg +\
        lower_right_corner +\
        bottom_edge_svg +\
        lower_left_corner +\
        left_edge_svg +\
        upper_left_corner_again

    res = svg.generate_edges(trayspec)

    # assert(res[0] == whole_piece_svg)
