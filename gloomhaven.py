def tray_setup(tray_name):
    trays = {
        "effects": [
            {
                "name": "bottom",
                "width": 279,
                "height": 116,
                "thickness": 3,
                "offset":  (5, 5),
                "edges": [
                    {
                        "rotation": 0,
                        "translation": (0, 0),
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 279
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "translation": (279, 0),
                        "opposite": "short side wall",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "translation": (279, 116),
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 279
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "translation": (0, 116),
                        "opposite": "short side wall 2",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 116
                            }
                        ]
                    }
                ],
            },
            {
                "name": "long side wall",
                "width": 279,
                "height": 12,
                "thickness": 3,
                "offset":  (5, 125),
                "edges": [
                    {
                        "rotation": 0,
                        "translation": (0, 0),
                        "depth": 12,

                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 279
                            }
                        ],
                        "holes": [
                            {
                                "offset": 21,
                                "opposite": "1 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 103,
                                "opposite": "2 half-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 30,
                                "opposite": "2 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "3 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "4 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "5 full v-divider",
                                "shape": "START_HALF_TAB"
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "translation": (279, 0),
                        "opposite": "short side wall",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "translation": (279, 12),
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 279
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "translation": (0, 12),
                        "opposite": "short side wall 2",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 12
                            }
                        ]
                    }
                ],
            },
            {
                "name": "short side wall",
                "width": 116,
                "height": 12,
                "thickness": 3,
                "offset":  (5, 160),
                "edges": [
                    {
                        "rotation": 0,
                        "translation": (0, 0),
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "translation": (116, 0),
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "translation": (116, 12),
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "translation": (0, 12),
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 12
                            }
                        ]
                    }
                ],
            },

            {
                "name": "long side wall 2",
                "width": 279,
                "height": 12,
                "thickness": 3,
                "offset":  (5, 180),
                "edges": [
                    {
                        "rotation": 0,
                        "translation": (0, 0),
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 279
                            }
                        ],
                        "holes": [
                            {
                                "offset": 28,
                                "opposite": "5 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "4 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "3 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "2 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 106,
                                "opposite": "1 half divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "1 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                        ]
                    },
                    {
                        "rotation": 1,
                        "translation": (279, 0),
                        "opposite": "short side wall",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "translation": (279, 12),
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 279
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "translation": (0, 12),
                        "opposite": "short side wall 2",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 12
                            }
                        ]
                    }
                ],

            },
            {
                "name": "short side wall 2",
                "width": 116,
                "height": 12,
                "thickness": 3,
                "offset":  (5, 200),
                "edges": [
                    {
                        "rotation": 0,
                        "translation": (0, 0),
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "translation": (116, 0),
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "translation": (116, 12),
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "translation": (0, 12),
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 12
                            }
                        ]
                    }
                ],
            },
            {
                "name": "middle h-divider",
                "width": 279,
                "height": 12,
                "thickness": 2,
                "offset":  (5, 240),
                "edges": [
                    {
                        "rotation": 0,
                        "translation": (0, 0),
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 279
                            }
                        ],
                        "holes": [
                            {
                                "offset": 21,
                                "opposite": "1 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "1 half-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 73,
                                "opposite": "1 half-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 30,
                                "opposite": "2 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "3 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "4 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 28,
                                "opposite": "5 full v-divider",
                                "shape": "START_HALF_TAB"
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "translation": (279, 0),
                        "opposite": "short side wall",
                        "parts": [
                            {
                                "tabs": "START_HALF_TAB",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "translation": (279, 12),
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 279
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "translation": (0, 12),
                        "opposite": "short side wall 2",
                        "parts": [
                            {
                                "tabs": "END_HALF_TAB",
                                "length": 12
                            }
                        ]
                    }
                ],

            },

        ]
    }

    for key, pieces in trays.iteritems():
        for piece in pieces:
            for edge in piece["edges"]:
                if "opposite" in edge:
                    opposite_name = edge["opposite"]
                    opposite_piece = next((piece for piece in pieces if piece["name"] == opposite_name), None)
                    edge["opposite"] = {"thickness": opposite_piece["thickness"]}
                if "holes" in edge:
                    for hole in edge["holes"]:
                        opposite_name = hole["opposite"]
                        opposite_piece = next((piece for piece in pieces if piece["name"] == opposite_name), None)
                        if opposite_piece is None:
                            opposite_piece = {"thickness": 2}
                        hole["opposite"] = {"thickness": opposite_piece["thickness"]}

    return trays[tray_name]


