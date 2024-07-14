import svg
import test.fixtures as fixtures

# These NEED to be in a configuration file, not hard coded!
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

    tray_spec = fixtures.get_single_column_two_slot_tray_spec(spacer_width, edge_width, depth, content_width)
    slots = tray_spec['columns'][0]['slots']
    slots[0]['length'] = slots[0]['height']
    slots[1]['length'] = slots[1]['height']

    corner_toothing = True

    svgi = svg.Svg(KERF, KERF)
    res = svgi.generate_slotted_top_edge(slots, spacer_width, content_width, corner_toothing, edge_width, depth)

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

    tray_spec = fixtures.get_single_column_two_slot_tray_spec(spacer_width, edge_width, depth, content_width)

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
    svgi = svg.Svg(KERF, KERF)
    res = svgi.generate_edges(tray_spec)
    assert(res[0] == expected)


def test_generate_floor_with_two_simple_columns():
    spacer_width = 2
    edge_width = 3
    content_width = 30
    tray_spec = fixtures.get_simple_two_column_tray_spec(spacer_width, edge_width, content_width)

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

    hole_width = svg.MIN_TOOTH_WIDTH
    nested_objects = [{
        'svg': [
            f"m {K_CORR} {K_CORR}",
            f"h {spacer_width - 2 * K_CORR}",
            f"v {hole_width - 2 * K_CORR}",
            f"h -{spacer_width - 2 * K_CORR}",
            f"v -{hole_width - 2 * K_CORR}",
            'z'
        ],
        'offset_x': (content_width - spacer_width) / 2.0,
        'offset_y': (tray_spec['columns'][0]['slots'][0]['height'] - hole_width) / 2.0
    }]

    res = svg.Svg(KERF, KERF).generate_floor(tray_spec)
    assert(res['svg'] == expected_svg)
    assert(res['nested_objects'] == nested_objects)
    expected_floor_object = {
        'svg': expected_svg,
        'nested_objects': nested_objects,
        'offset_x': edge_width,
        'offset_y': edge_width,
        'thickness': edge_width,
        'width': content_width + 2 * edge_width,
        'height': content_width + 2 * edge_width,
        'tray': tray_spec['name']
    }
    assert(res == expected_floor_object)


def test_walls_match_with_floors():
    edge_width = 3
    content_width = 30.0
    content_height = 34.0
    depth = 30.0
    depth_tooth_size = depth / 3.0
    width_tooth = content_width / 3.0
    height_tooth = content_height / 3.0
    tray_spec = fixtures.get_single_column_single_slot_tray_spec(edge_width, depth, content_width, content_height)
    svgi = svg.Svg(KERF, KERF)
    edges = svgi.generate_edges(tray_spec)
    floor = svgi.generate_floor(tray_spec)

    expected_edges_w = [
        f"h {K_CORR}",  # Top edge
        f"h {edge_width}",
        f"h {content_width}",
        f"h {edge_width}",
        f"h {K_CORR} v {K_CORR}",
        f"v {depth_tooth_size + K_CORR}",  # Right edge
        f"h {-edge_width}",
        f"v {depth_tooth_size - 2*K_CORR}",
        f"h {edge_width}",
        f"v {depth_tooth_size + K_CORR}",
        f"v {edge_width}",
        f"v {K_CORR} h -{K_CORR}",
        f"h -{edge_width}",  # Floor edge
        f"h -{width_tooth + K_CORR}",
        f"v -{edge_width}",
        f"h -{width_tooth - 2*K_CORR}",
        f"v {edge_width}",
        f"h -{width_tooth + K_CORR}",
        f"h -{edge_width}",
        f"h -{K_CORR} v -{K_CORR}",
        f"v -{edge_width}",  # Left edge
        f"v -{depth_tooth_size + K_CORR}",
        f"h {edge_width}",
        f"v -{depth_tooth_size - K_CORR*2}",
        f"h -{edge_width}",
        f"v -{depth_tooth_size + K_CORR}",
        f"v -{K_CORR}",
        'z'
    ]
    result_edge_w = edges[0]['svg']
    assert(result_edge_w == expected_edges_w)

    expected_floor_w = [
        f"h {K_CORR}",
        f"h {width_tooth -K_CORR}",
        f"v -{edge_width}",
        f"h {width_tooth + K_CORR*2}",
        f"v {edge_width}",
        f"h {width_tooth - K_CORR}",
        f"h {K_CORR} v {K_CORR}",
    ]
    floor_w = floor['svg'][:len(expected_floor_w)]
    assert(floor_w == expected_floor_w)

    expected_edges_h = [
        f"h {K_CORR}",  # Top edge
        f"h {content_height}",
        f"h {K_CORR} v {K_CORR}",
        f"v {depth_tooth_size - K_CORR}",  # Right edge
        f"h {edge_width}",
        f"v {depth_tooth_size + 2*K_CORR}",
        f"h -{edge_width}",
        f"v {depth_tooth_size - K_CORR}",
        f"v {edge_width}",
        f"v {K_CORR} h -{K_CORR}",
        f"h -{height_tooth + K_CORR}",  # Bottom edge
        f"v -{edge_width}",
        f"h -{height_tooth - 2*K_CORR}",
        f"v {edge_width}",
        f"h -{height_tooth + K_CORR}",
        f"h -{K_CORR} v -{K_CORR}",
        f"v -{edge_width}",  # Left edge
        f"v -{depth_tooth_size - K_CORR}",
        f"h -{edge_width}",
        f"v -{depth_tooth_size + K_CORR*2}",
        f"h {edge_width}",
        f"v -{depth_tooth_size - K_CORR}",
        f"v -{K_CORR}",
        'z'
    ]

    assert(edges[1]['svg'] == expected_edges_h)

    expected_floor_h = [
        f"v {height_tooth - K_CORR}",
        f"h {edge_width}",
        f"v {height_tooth + 2 * K_CORR}",
        f"h -{edge_width}",
        f"v {height_tooth - K_CORR}",
        f"v {K_CORR} h -{K_CORR}"
    ]

    floor_h = floor['svg'][len(expected_floor_w):len(expected_floor_w)+len(expected_floor_h)]
    assert(floor_h == expected_floor_h)
