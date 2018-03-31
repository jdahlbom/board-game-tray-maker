def tray_setup(tray_name, errorFn):
    trays = {
        "effects": [
            {
                "name": "bottom",
                "width": 279,
                "height": 116,
                "thickness": 3,
                "edges": [
                    {
                        "rotation": 0,
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 279
                            }
                        ],
                        "holes": [
                            {
                                "offset": 21,
                                "opposite": "1 full v-divider",
                                "shape": "FEMALE"
                            },
                            {
                                "offset": 104,
                                "opposite": "2 half-divider",
                                "shape": "FEMALE",
                                "length": 59
                            },
                            {
                                "offset": 30,
                                "opposite": "2 full v-divider",
                                "shape": "FEMALE"
                            },
                            {
                                "offset": 28,
                                "opposite": "3 full v-divider",
                                "shape": "FEMALE"
                            },
                            {
                                "offset": 28,
                                "opposite": "4 full v-divider",
                                "shape": "FEMALE"
                            },
                            {
                                "offset": 28,
                                "opposite": "5 full v-divider",
                                "shape": "FEMALE"
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
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 279
                            }
                        ],
                        "holes": [
                            {
                                "offset": 226,
                                "opposite": "1 half-divider",
                                "shape": "FEMALE",
                                "length": 55
                            },
                        ]
                    },
                    {
                        "rotation": 3,
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
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,

                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 279,
                                "pin_height": 0.5
                            }
                        ],
                        "holes": [
                            {
                                "offset": 21,
                                "opposite": "1 full v-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 104,
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
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 279,
                                "notch_depth": 0.5
                            }
                        ]
                    },
                    {
                        "rotation": 3,
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
                "edges": [
                    {
                        "rotation": 0,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 116
                            }
                        ],
                        "holes": [
                            {
                                "opposite": "middle h-divider",
                                "offset": 59,
                                "shape": "START_HALF_TAB"
                            }
                        ]
                    },
                    {
                        "rotation": 1,
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
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 279,
                                "pin_height": 0.5
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
                                "opposite": "1 half-divider",
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
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "MALE",
                                "length": 279,
                                "notch_depth": 0.5
                            }
                        ]
                    },
                    {
                        "rotation": 3,
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
                "edges": [
                    {
                        "rotation": 0,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 116
                            }
                        ],
                        "holes": [
                            {
                                "opposite": "middle h-divider",
                                "offset": 55,
                                "shape": "START_HALF_TAB"
                            }
                        ]
                    },
                    {
                        "rotation": 1,
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
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 129,
                                "indent": {
                                    "offset": 80,
                                    "radius": 7
                                }
                            },
                            {
                                "tabs": "TOP",
                                "length": 30,
                                "indent": {
                                    "offset": 8,
                                    "radius": 7
                                }

                            },
                            {
                                "tabs": "TOP",
                                "length": 120
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
                                "offset": 74,
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
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 279
                            }
                        ]
                    },
                    {
                        "rotation": 3,
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
            {
                "name": "1 full v-divider",
                "width": 116,
                "height": 12,
                "thickness": 2,
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 116
                            }
                        ],
                        "holes": [
                            {
                                "offset": 59,
                                "opposite": "middle h-divider",
                                "shape": "END_HALF_TAB"
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "START_HALF_TAB",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "END_HALF_TAB",
                                "length": 12
                            }
                        ]
                    }
                ],

            },

            {
                "name": "2 full v-divider",
                "width": 116,
                "height": 12,
                "thickness": 2,
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 116
                            }
                        ],
                        "holes": [
                            {
                                "offset": 59,
                                "opposite": "middle h-divider",
                                "shape": "END_HALF_TAB"
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "START_HALF_TAB",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "END_HALF_TAB",
                                "length": 12
                            }
                        ]
                    }
                ],

            },
            {
                "name": "3 full v-divider",
                "width": 116,
                "height": 12,
                "thickness": 2,
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 116
                            }
                        ],
                        "holes": [
                            {
                                "offset": 59,
                                "opposite": "middle h-divider",
                                "shape": "END_HALF_TAB"
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "START_HALF_TAB",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "END_HALF_TAB",
                                "length": 12
                            }
                        ]
                    }
                ],

            },
            {
                "name": "4 full v-divider",
                "width": 116,
                "height": 12,
                "thickness": 2,
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 116
                            }
                        ],
                        "holes": [
                            {
                                "offset": 59,
                                "opposite": "middle h-divider",
                                "shape": "END_HALF_TAB"
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "START_HALF_TAB",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "END_HALF_TAB",
                                "length": 12
                            }
                        ]
                    }
                ],

            },
            {
                "name": "5 full v-divider",
                "width": 116,
                "height": 12,
                "thickness": 2,
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 116
                            }
                        ],
                        "holes": [
                            {
                                "offset": 59,
                                "opposite": "middle h-divider",
                                "shape": "END_HALF_TAB"
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "START_HALF_TAB",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 116
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "END_HALF_TAB",
                                "length": 12
                            }
                        ]
                    }
                ],

            },
            {
                "name": "1 half-divider",
                "width": 55,
                "height": 12,
                "thickness": 2,
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 55
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "opposite": "long side wall 2",
                        "parts": [
                            {
                                "tabs": "START_HALF_TAB",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 55
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "opposite": "middle h-divider",
                        "parts": [
                            {
                                "tabs": "END_HALF_TAB",
                                "length": 12
                            }
                        ]
                    }
                ],

            },
            {
                "name": "2 half-divider",
                "width": 59,
                "height": 12,
                "thickness": 2,
                "edges": [
                    {
                        "rotation": 0,
                        "depth": 12,
                        "parts": [
                            {
                                "tabs": "TOP",
                                "length": 59
                            }
                        ]
                    },
                    {
                        "rotation": 1,
                        "opposite": "long side wall",
                        "parts": [
                            {
                                "tabs": "START_HALF_TAB",
                                "length": 12
                            }
                        ]
                    },
                    {
                        "rotation": 2,
                        "opposite": "bottom",
                        "parts": [
                            {
                                "tabs": "FEMALE",
                                "length": 59
                            }
                        ]
                    },
                    {
                        "rotation": 3,
                        "opposite": "middle h-divider",
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
                            errorFn("Opposite piece [{}] missing for piece [{}]".format(opposite_name, piece["name"]))
                            opposite_piece = {"thickness": 2}
                        hole["opposite"] = {"thickness": opposite_piece["thickness"]}

    return trays[tray_name]


