from copy import deepcopy

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
                                "parts": [
                                    {
                                        "shape": "FEMALE",
                                        "length": 59
                                    },
                                    {
                                        "offset": 2,
                                        "shape": "FEMALE",
                                        "length": 55
                                    }
                                ]
                            },
                            {
                                "offset": 104,
                                "opposite": "2 half-divider",
                                "shape": "FEMALE",
                                "length": 59
                            },
                            {
                                "offset": 15,
                                "parts": [
                                    {
                                        "offset": 39,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 20
                                    }
                                ]
                            },
                            {
                                "offset": 15,
                                "opposite": "2 full v-divider",
                                "parts": [
                                    {
                                        "shape": "FEMALE",
                                        "length": 59
                                    },
                                    {
                                        "offset": 2,
                                        "shape": "FEMALE",
                                        "length": 55
                                    }
                                ]
                            },
                            {
                                "offset": 28,
                                "opposite": "3 full v-divider",
                                "parts": [
                                    {
                                        "shape": "FEMALE",
                                        "length": 59
                                    },
                                    {
                                        "offset": 2,
                                        "shape": "FEMALE",
                                        "length": 55
                                    }
                                ]
                            },
                            {
                                "offset": 28,
                                "opposite": "4 full v-divider",
                                "parts": [
                                    {
                                        "shape": "FEMALE",
                                        "length": 59
                                    },
                                    {
                                        "offset": 2,
                                        "shape": "FEMALE",
                                        "length": 55
                                    }
                                ]
                            },
                            {
                                "offset": 28,
                                "opposite": "5 full v-divider",
                                "parts": [
                                    {
                                        "shape": "FEMALE",
                                        "length": 59
                                    },
                                    {
                                        "offset": 2,
                                        "shape": "FEMALE",
                                        "length": 55
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "rotation": 1,
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
                                "shape": "FEMALE",
                                "length": 55,
                                "offset": 226,
                                "opposite": "1 half-divider"
                            }
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
                                "length": 55
                            },
                            {
                                "tabs": "TOP",
                                "length": 2
                            },
                            {
                                "tabs": "FEMALE",
                                "length": 59
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
                "copy_of": "1 full v-divider"
            },
            {
                "name": "3 full v-divider",
                "copy_of": "1 full v-divider"
            },
            {
                "name": "4 full v-divider",
                "copy_of": "1 full v-divider"
            },
            {
                "name": "5 full v-divider",
                "copy_of": "1 full v-divider"
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

        ],
        "small_terrain": [
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
                                "offset": 12.82,
                                "parts": [
                                    {
                                        "offset": 25.83,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    },
                                    {
                                        "offset": 14.33,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    }
                                ],
                            },
                            {
                                "offset": 12.823,
                                "parts": [
                                    {
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                ],
                                "opposite": "1 v-divider"
                            },
                            {
                                "offset": 12.82,
                                "parts": [
                                    {
                                        "offset": 25.83,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    },
                                    {
                                        "offset": 14.33,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    }
                                ],
                            },
                            {
                                "offset": 12.823,
                                "parts": [
                                    {
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                ],
                                "opposite": "2 v-divider"
                            },
                            {
                                "offset": 12.82,
                                "parts": [
                                    {
                                        "offset": 25.83,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    },
                                    {
                                        "offset": 14.33,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    }
                                ],
                            },
                            {
                                "offset": 12.823,
                                "parts": [
                                    {
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                ],
                                "opposite": "3 v-divider"
                            },
                            {
                                "offset": 12.82,
                                "parts": [
                                    {
                                        "offset": 25.83,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    },
                                    {
                                        "offset": 14.33,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    }
                                ],
                            },
                            {
                                "offset": 12.823,
                                "parts": [
                                    {
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                ],
                                "opposite": "4 v-divider"
                            },
                            {
                                "offset": 12.82,
                                "parts": [
                                    {
                                        "offset": 25.83,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    },
                                    {
                                        "offset": 14.33,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    }
                                ],
                            },
                            {
                                "offset": 12.823,
                                "parts": [
                                    {
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                ],
                                "opposite": "5 v-divider"
                            },
                            {
                                "offset": 12.82,
                                "parts": [
                                    {
                                        "offset": 25.83,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    },
                                    {
                                        "offset": 14.33,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    }
                                ],
                            },
                            {
                                "offset": 12.823,
                                "parts": [
                                    {
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                    {
                                        "offset": 2,
                                        "length": 37.33,
                                        "shape": "FEMALE"
                                    },
                                ],
                                "opposite": "6 v-divider"
                            },
                            {
                                "offset": 12.82,
                                "parts": [
                                    {
                                        "offset": 25.83,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    },
                                    {
                                        "offset": 14.33,
                                        "shape": "C_BEZIER_RECT",
                                        "width": 12.5,
                                        "length": 25
                                    }
                                ],
                            },
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
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "1 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "2 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "3 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "4 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "5 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "6 v-divider"
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
                                "offset": 37.33,
                                "opposite": "1 h-divider",
                                "shape": "START_HALF_TAB"
                            },
                            {
                                "offset": 37.33,
                                "opposite": "2 h-divider",
                                "shape": "START_HALF_TAB"
                            },
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
                "copy_of": "long side wall"
            },
            {
                "name": "short side wall 2",
                "copy_of": "short side wall"
            },
            {
                "name": "1 v-divider",
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
                                "offset": 37.33,
                                "opposite": "1 h-divider",
                                "shape": "END_HALF_TAB"
                            },
                            {
                                "offset": 37.33,
                                "opposite": "2 h-divider",
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
                                "length": 37.33
                            },
                            {
                                "tabs": "TOP",
                                "length": 2
                            },
                            {
                                "tabs": "FEMALE",
                                "length": 37.33
                            },
                            {
                                "tabs": "TOP",
                                "length": 2
                            },
                            {
                                "tabs": "FEMALE",
                                "length": 37.33
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
                "name": "2 v-divider",
                "copy_of": "1 v-divider"
            },
            {
                "name": "3 v-divider",
                "copy_of": "1 v-divider"
            },
            {
                "name": "4 v-divider",
                "copy_of": "1 v-divider"
            },
            {
                "name": "5 v-divider",
                "copy_of": "1 v-divider"
            },
            {
                "name": "6 v-divider",
                "copy_of": "1 v-divider"
            },
            {
                "name": "1 h-divider",
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
                                "length": 39.143,
                                "indent": {
                                    "offset": 12.07,
                                    "radius": 7
                                }
                            },
                            {
                                "tabs": "TOP",
                                "length": 40.143,
                                "indent": {
                                    "offset": 13.07,
                                    "radius": 7
                                }
                            },
                            {
                                "tabs": "TOP",
                                "length": 40.143,
                                "indent": {
                                    "offset": 13.07,
                                    "radius": 7
                                }
                            },
                            {
                                "tabs": "TOP",
                                "length": 40.143,
                                "indent": {
                                    "offset": 13.07,
                                    "radius": 7
                                }
                            },
                            {
                                "tabs": "TOP",
                                "length": 40.143,
                                "indent": {
                                    "offset": 13.07,
                                    "radius": 7
                                }
                            },
                            {
                                "tabs": "TOP",
                                "length": 40.143,
                                "indent": {
                                    "offset": 13.07,
                                    "radius": 7
                                }
                            },
                            {
                                "tabs": "TOP",
                                "length": 39.143,
                                "indent": {
                                    "offset": 13.07,
                                    "radius": 7
                                }
                            },
                        ],
                        "holes": [
                            {
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "1 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "2 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "3 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "4 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "5 v-divider"
                            },{
                                "offset": 38.143,
                                "shape": "START_HALF_TAB",
                                "opposite": "6 v-divider"
                            },
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
                "name": "2 h-divider",
                "copy_of": "1 h-divider"
            },
        ]
    }

    pieces = trays[tray_name]
    new_pieces = []
    for piece in pieces:
        if "copy_of" in piece:
            copyable = next( fpiece for fpiece in pieces if fpiece["name"] == piece["copy_of"])
            piece_name = deepcopy(piece["name"])
            copy = deepcopy(copyable)
            copy["name"] = piece_name
            new_pieces.append(copy)
        else:
            new_pieces.append(piece)

    for piece in new_pieces:
        for edge in piece["edges"]:
            if "opposite" in edge:
                opposite_name = edge["opposite"]
                opposite_piece = next((piece for piece in new_pieces if piece["name"] == opposite_name), None)
                edge["opposite"] = {"thickness": opposite_piece["thickness"]}
            if "holes" in edge:
                for hole in edge["holes"]:
                    if "opposite" not in hole:
                        continue
                    opposite_name = hole["opposite"]
                    opposite_piece = next((piece for piece in new_pieces if piece["name"] == opposite_name), None)
                    if opposite_piece is None or "thickness" not in opposite_piece:
                        errorFn("Opposite piece [{}] missing for piece [{}] in tray [{}]".format(opposite_name, piece["name"], tray_name))
                        opposite_piece = {"thickness": 2}
                    hole["opposite"] = {"thickness": opposite_piece["thickness"]}
    return new_pieces

