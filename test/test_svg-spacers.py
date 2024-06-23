import svg
import test.fixtures as fixtures

#These NEED to be in a configuration file, not hard coded!
STROKE = 0.001
MIN_TOOTH_WIDTH = 7.0
INDENT_DEPTH = 10
KERF = 0.2
K_CORR = KERF/2.0


def test_single_column_horizontal_spacer_without_indent():
    spacer_material_thickness = 2
    edge_material_thickness = 3
    content_width = 100
    depth = 60

    tray_spec = fixtures.get_single_column_two_slot_tray_spec(spacer_material_thickness, edge_material_thickness, depth, content_width)
    col_widths = [ tray_spec['columns'][0]['width']]
    spacer_indents = [ False ]
    spacer_width = spacer_material_thickness
    l_edge_width = edge_material_thickness
    r_edge_width = edge_material_thickness

    res = svg.generate_horiz_spacer(col_widths, spacer_indents, content_width, spacer_width, l_edge_width, r_edge_width, depth)
    expected_svg = [
        f"h {l_edge_width + K_CORR}",
        f"h {col_widths[0]}",
        f"h {r_edge_width + K_CORR}",
        f"v {INDENT_DEPTH + K_CORR * 2}",
        f"h -{r_edge_width}",
        f"v {depth-INDENT_DEPTH}",
        f"h -{col_widths[0] + K_CORR * 2}",
        f"v -{depth-INDENT_DEPTH}",
        f"h -{l_edge_width}",
        f"v -{INDENT_DEPTH + K_CORR * 2}",
        "z"
    ]
    expected = {
        'svg': expected_svg,
        'width': content_width + l_edge_width + r_edge_width + 2 * K_CORR,
        'height': depth + 2 * K_CORR,
        'offset_x': 0,
        'offset_y': 0,
        'thickness': spacer_width
    }
    assert(expected == res)


def test_generate_horizontal_spacers_single_slot_should_create_no_spacers():
    spacer_material_thickness = 2
    edge_material_thickness = 3
    depth = 20

    columns = [
        {
            "width": 100,
            "slots": [
                {
                    "forbid_indent": True
                }
            ]
        }
    ]
    res = svg.generate_horizontal_spacers(columns, edge_material_thickness, spacer_material_thickness, depth)
    assert(res == [])


def test_generate_horizontal_spacers_two_slots_should_create_simplest_spacer():
    spacer_width = 2
    edge_width = 3
    depth = 20
    content_width = 100
    tray_spec = fixtures.get_single_column_two_slot_tray_spec(spacer_width, edge_width, depth, content_width)

    columns = tray_spec['columns']
    first_column_width = columns[0]['width']
    res = svg.generate_horizontal_spacers(columns, edge_width, spacer_width, depth)
    expected_svg = [
        f"h {edge_width + K_CORR}",
        f"h {first_column_width}",
        f"h {edge_width + K_CORR}",
        f"v {INDENT_DEPTH + K_CORR * 2}",
        f"h -{edge_width}",
        f"v {depth-INDENT_DEPTH}",
        f"h -{first_column_width + K_CORR * 2}",
        f"v -{depth-INDENT_DEPTH}",
        f"h -{edge_width}",
        f"v -{INDENT_DEPTH + K_CORR * 2}",
        "z"
    ]
    expected = [{
        'svg': expected_svg,
        'width': first_column_width + 2 * edge_width + 2 * K_CORR,
        'height': depth + 2 * K_CORR,
        'offset_x': 0,
        'offset_y': 0,
        'thickness': spacer_width
    }]
    assert(res == expected)


def test_generate_vert_spacer():
    spacer_width = 2
    edge_width = 3
    content_width = 30
    depth = 20
    indent_depth = svg.INDENT_DEPTH
    tooth_width = svg.MIN_TOOTH_WIDTH
    tray_spec = fixtures.get_simple_two_column_tray_spec(spacer_width, edge_width, content_width)

    indent_spacing = svg.create_vertical_spacer_combined_slot_list(tray_spec['columns'], spacer_width)
    assert(indent_spacing[0] == [{'length': content_width}])

    res = svg.generate_vert_spacer(indent_spacing[0], content_width, depth, edge_width, spacer_width)

    top_left_corner = [f"h {K_CORR}"]
    top_edge = [
        f"h {edge_width}",
        f"h {content_width}",
        f"h {edge_width}"
    ]
    top_right_corner = [f"h {K_CORR} v {K_CORR}"]
    right_edge = [
        f"v {indent_depth}",
        f"v {K_CORR} h -{K_CORR}",
        f"h -{edge_width}",
        f"v {depth-indent_depth}"
    ]
    bottom_edge = [
        f"h -{(content_width-tooth_width)/2.0 - K_CORR}",
        f"v {edge_width + K_CORR}",
        f"h -{(tooth_width + 2 * K_CORR)}",
        f"v -{edge_width + K_CORR}",
        f"h -{(content_width-tooth_width)/2.0 - K_CORR}"
    ]
    left_edge = [
        f"v -{depth-indent_depth}",
        f"h -{edge_width}",
        f"h -{K_CORR} v -{K_CORR}",
        f"v -{indent_depth}"
    ]
    top_left_corner_again = [f"v -{K_CORR}"]
    close_path = ['z']

    expected_svg = top_left_corner +\
        top_edge +\
        top_right_corner +\
        right_edge +\
        bottom_edge +\
        left_edge +\
        top_left_corner_again +\
        close_path

    expected = {
        'svg': expected_svg,
        'width': tray_spec['columns'][0]['slots'][0]['height'] + 2 * edge_width + 2 * K_CORR,
        'height': depth + edge_width + 3 * K_CORR,
        'offset_x': 0,
        'offset_y': 0,
        'thickness': spacer_width
    }
    assert(res == expected)
