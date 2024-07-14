from llist import dllist


def get_single_column_single_slot_tray_spec(edge_width, depth, content_width, content_height):
    return {
        'name': 'Test tray',
        'spacer_width': 12345,
        'edge_width': edge_width,
        'tray_depth': depth,
        'tray_width': content_width + 2*edge_width,  # Lets test this without the elasticity, with exactly sized content
        'tray_height': content_height + 2*edge_width,
        'columns': dllist([
            {
                'width': content_width,
                'slots': [
                    {
                        'height': content_height,
                        'forbid_indent': True
                    }
                ]
            }
        ])
    }


def get_single_column_two_slot_tray_spec(spacer_width, edge_width, depth, content_width):
    return {
        'name': 'Test tray',
        'spacer_width': spacer_width,
        'edge_width': edge_width,
        'tray_depth': depth,
        'tray_width': content_width + 2*edge_width,  # Lets test this without the elasticity, with exactly sized content
        'tray_height': content_width + 2*edge_width,
        'columns': dllist([
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
        ])
    }


def get_simple_two_column_tray_spec(spacer_width, edge_width, content_width):
    return {
        'name': 'Test tray',
        'spacer_width': spacer_width,
        'edge_width': edge_width,
        'tray_depth': 111,
        'tray_width': content_width + 2*edge_width,  # Lets test this without the elasticity, with exactly sized content
        'tray_height': content_width + 2*edge_width,
        'columns': [
            {
                'width': (content_width - spacer_width) / 2.0,
                'slots': dllist([
                    {
                        'height': content_width,
                        'forbid_indent': True
                    }
                ])
            },
            {
                'width': (content_width - spacer_width) / 2.0,
                'slots': dllist([
                    {
                        'height': content_width,
                        'forbid_indent': True
                    }
                ])
            }
        ]
    }


def get_object_list_with_two_thicknesses_and_bins():
    return [
        {
            "width": 40.0,
            "height": 60.0,
            "tray": "first",
            "thickness": 3,
            "id_in_tray": 1,
            "offset_x": 0,
            "offset_y": 0
        },
        {
            "width": 40.0,
            "height": 30.0,
            "tray": "first",
            "thickness": 3,
            "id_in_tray": 2,
            "offset_x": 0,
            "offset_y": 0
        },
        {
            "width": 40.0,
            "height": 30.0,
            "tray": "first",
            "thickness": 3,
            "id_in_tray": 3,
            "offset_x": 0,
            "offset_y": 0
        },
        {
            "width": 40.0,
            "height": 40.0,
            "tray": "first",
            "thickness": 1,
            "id_in_tray": 4,
            "offset_x": 0,
            "offset_y": 0
        }
    ]


def get_four_objects_to_lay_out():
    return [
        {
            'width': 98,
            'height': 70,
            'offset_x': 0,
            'offset_y': 0,
            'thickness': 3,
            'tray': 'power-cards',
            'id_in_tray': 0
        },
        {
            'width': 98,
            'height': 70,
            'offset_x': 0,
            'offset_y': 0,
            'thickness': 3,
            'tray': 'power-cards',
            'id_in_tray': 2
        },
        {
            'width': 92,
            'height': 70,
            'offset_x': 3,
            'offset_y': 0,
            'thickness': 3,
            'tray': 'power-cards',
            'id_in_tray': 1
        },
        {
            'width': 92,
            'height': 70,
            'offset_x': 3,
            'offset_y': 0,
            'thickness': 3,
            'tray': 'power-cards',
            'id_in_tray': 3
        }
    ]