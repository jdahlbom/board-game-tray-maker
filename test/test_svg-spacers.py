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

    col_widths = [100]
    spacer_indents = [ False ]
    content_width = 100
    spacer_width = spacer_material_thickness
    l_edge_width = edge_material_thickness
    r_edge_width = edge_material_thickness
    depth = 60

    res = svg.generate_horiz_spacer(col_widths, spacer_indents, content_width, spacer_width, l_edge_width, r_edge_width, depth)
    expected = [
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
    spacer_material_thickness = 2
    edge_material_thickness = 3
    depth = 20

    col_widths = [100]

    columns = [
        {
            "width": col_widths[0],
            "slots": [  # Two slots in single column, no indent, simplest spacer
                {
                    "forbid_indent": True
                },
                {
                    "forbid_indent": True
                }

            ]
        }
    ]
    res = svg.generate_horizontal_spacers(columns, edge_material_thickness, spacer_material_thickness, depth)
    expected = [
        f"h {edge_material_thickness + K_CORR}",
        f"h {col_widths[0]}",
        f"h {edge_material_thickness + K_CORR}",
        f"v {INDENT_DEPTH + K_CORR * 2}",
        f"h -{edge_material_thickness}",
        f"v {depth-INDENT_DEPTH}",
        f"h -{col_widths[0] + K_CORR * 2}",
        f"v -{depth-INDENT_DEPTH}",
        f"h -{edge_material_thickness}",
        f"v -{INDENT_DEPTH + K_CORR * 2}",
        "z"
    ]

    assert(len(res) == 1)
    assert(res[0] == expected)


def test_generate_vert_spacer():
    spacer_width = 2
    edge_width = 3
    content_width = 30
    tray_spec = fixtures.get_simple_two_column_tray_spec(spacer_width, edge_width, content_width)