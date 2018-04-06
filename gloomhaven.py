from copy import deepcopy

def tray_setup(tray_name, errorFn):
    trays = {
        "effects": {
                "dimensions": {
                    "width": 279,
                    "height": 116,
                    "depth": 12
                },
                "pieces": [
                    {
                        "name": "bottom",
                        "width": "tray.width",
                        "height": "tray.height",
                        "thickness": 3,
                        "edges": [
                            {
                                "rotation": 0,
                                "opposite": "long side wall",
                                "parts": [
                                    {
                                        "tabs": "FEMALE",
                                        "length": "piece.width"
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
                                        "length": "piece.height"
                                    }
                                ]
                            },
                            {
                                "rotation": 2,
                                "opposite": "long side wall 2",
                                "parts": [
                                    {
                                        "tabs": "FEMALE",
                                        "length": "piece.width"
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
                                        "length": "piece.height"
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
                                "parts": [
                                    {
                                        "tabs": "TOP",
                                        "length": "piece.width",
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
                                        "length": "piece.height"
                                    }
                                ]
                            },
                            {
                                "rotation": 2,
                                "opposite": "bottom",
                                "parts": [
                                    {
                                        "tabs": "MALE",
                                        "length": "piece.width",
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
                                        "length": "piece.height"
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
                                        "length": "piece.width"
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
                                        "length": "piece.height"
                                    }
                                ]
                            },
                            {
                                "rotation": 2,
                                "opposite": "bottom",
                                "parts": [
                                    {
                                        "tabs": "MALE",
                                        "length": "piece.width"
                                    }
                                ]
                            },
                            {
                                "rotation": 3,
                                "opposite": "long side wall",
                                "parts": [
                                    {
                                        "tabs": "FEMALE",
                                        "length": "piece.height"
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
                                "parts": [
                                    {
                                        "tabs": "TOP",
                                        "length": "piece.width",
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
                                        "length": "piece.height"
                                    }
                                ]
                            },
                            {
                                "rotation": 2,
                                "opposite": "bottom",
                                "parts": [
                                    {
                                        "tabs": "MALE",
                                        "length": "piece.width",
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
                                        "length": "piece.height"
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
                                        "length": "piece.width"
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
                                        "length": "piece.height"
                                    }
                                ]
                            },
                            {
                                "rotation": 2,
                                "opposite": "bottom",
                                "parts": [
                                    {
                                        "tabs": "MALE",
                                        "length": "piece.width"
                                    }
                                ]
                            },
                            {
                                "rotation": 3,
                                "opposite": "long side wall",
                                "parts": [
                                    {
                                        "tabs": "FEMALE",
                                        "length": "piece.height"
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
                                        "length": "piece.height"
                                    }
                                ]
                            },
                            {
                                "rotation": 2,
                                "opposite": "bottom",
                                "parts": [
                                    {
                                        "tabs": "TOP",
                                        "length": "piece.width"
                                    }
                                ]
                            },
                            {
                                "rotation": 3,
                                "opposite": "short side wall 2",
                                "parts": [
                                    {
                                        "tabs": "END_HALF_TAB",
                                        "length": "piece.height"
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
                                "parts": [
                                    {
                                        "tabs": "TOP",
                                        "length": "piece.width"
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
                                        "length": "piece.height"
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
                                        "length": "piece.height"
                                    }
                                ]
                            }
                        ]
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
                                "parts": [
                                    {
                                        "tabs": "TOP",
                                        "length": "piece.width"
                                    }
                                ]
                            },
                            {
                                "rotation": 1,
                                "opposite": "long side wall 2",
                                "parts": [
                                    {
                                        "tabs": "START_HALF_TAB",
                                        "length": "piece.height"
                                    }
                                ]
                            },
                            {
                                "rotation": 2,
                                "opposite": "bottom",
                                "parts": [
                                    {
                                        "tabs": "FEMALE",
                                        "length": "piece.width"
                                    }
                                ]
                            },
                            {
                                "rotation": 3,
                                "opposite": "middle h-divider",
                                "parts": [
                                    {
                                        "tabs": "END_HALF_TAB",
                                        "length": "piece.height"
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
                                "parts": [
                                    {
                                        "tabs": "TOP",
                                        "length": "piece.width"
                                    }
                                ]
                            },
                            {
                                "rotation": 1,
                                "opposite": "long side wall",
                                "parts": [
                                    {
                                        "tabs": "START_HALF_TAB",
                                        "length": "piece.height"
                                    }
                                ]
                            },
                            {
                                "rotation": 2,
                                "opposite": "bottom",
                                "parts": [
                                    {
                                        "tabs": "FEMALE",
                                        "length": "piece.width"
                                    }
                                ]
                            },
                            {
                                "rotation": 3,
                                "opposite": "middle h-divider",
                                "parts": [
                                    {
                                        "tabs": "END_HALF_TAB",
                                        "length": "piece.height"
                                    }
                                ]
                            }
                        ],

                    },

                ]
            },
        "small_terrain": {
            "dimensions": {
                "width": 279,
                "height": 116,
                "depth": 12
            },
            "pieces": [
                {
                    "name": "bottom",
                    "width": "tray.width",
                    "height": "tray.height",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,
                            "opposite": "long side wall",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
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
                            "opposite": "short side wall",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "long side wall 2",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "short side wall 2",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "long side wall",
                    "width": "tray.width",
                    "height": "tray.depth",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,

                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width",
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
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.width",
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
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "short side wall",
                    "width": "tray.height",
                    "height": "tray.depth",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
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
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.width"
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "long side wall",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.height"
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
                    "width": "tray.height",
                    "height": "tray.depth",
                    "thickness": 2,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
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
                                    "length": "piece.height"
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
                                    "length": "piece.height"
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
                    "width": "tray.width",
                    "height": "tray.depth",
                    "thickness": 2,
                    "edges": [
                        {
                            "rotation": 0,
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
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "short side wall 2",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
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
        },
        "large_terrain": {
            "dimensions": {
                "width": 279,
                "height": 116,
                "depth": 13
            },
            "pieces": [
                {
                    "name": "bottom",
                    "width": "tray.width",
                    "height": "tray.height",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,
                            "opposite": "long side wall",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 4,
                                    "parts": [
                                        {
                                            "offset": 36,
                                            "shape": "C_BEZIER_RECT",
                                            "width": 14,
                                            "length": 10
                                        }
                                    ],
                                },
                                {
                                    "offset": 4,
                                    "parts": [
                                        {
                                            "length": 46,
                                            "shape": "FEMALE"
                                        }
                                    ],
                                    "opposite": "1 up v-divider"
                                },
                                {
                                    "offset": 21,
                                    "parts": [
                                        {
                                            "offset": 20,
                                            "shape": "C_BEZIER_RECT",
                                            "width": 16,
                                            "length": 20
                                        }
                                    ],
                                },
                                {
                                    "offset": 25,
                                    "parts": [
                                        {
                                            "length": 46,
                                            "shape": "FEMALE"
                                        }
                                    ],
                                    "opposite": "2 up v-divider"
                                },
                                {
                                    "offset": 58,
                                    "shape": "FEMALE",
                                    "length": 46,
                                    "opposite": "3 up v-divider"
                                },
                                {
                                    "offset": 25.5,
                                    "parts": [
                                        {
                                            "offset": 11,
                                            "length": 20,
                                            "width": 16,
                                            "shape": "C_BEZIER_RECT"

                                        },
                                    ],
                                },
                                {
                                    "offset": 25,
                                    "length": 46,
                                    "shape": "FEMALE",
                                    "opposite": "4 up v-divider"
                                },
                                {
                                    "offset": 23,
                                    "parts": [
                                        {
                                            "offset": 11,
                                            "shape": "C_BEZIER_RECT",
                                            "width": 16,
                                            "length": 24
                                        }
                                    ],
                                },
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "short side wall",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.height"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 22,
                                    "opposite": "2 small h-divider",
                                    "parts": [
                                        {
                                            "length": 21,
                                            "shape": "FEMALE",
                                        },
                                        {
                                            "offset": 20,
                                            "length": 21,
                                            "shape": "FEMALE"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "long side wall 2",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 11.5,
                                    "parts": [
                                        {
                                            "offset": 23.5,
                                            "shape": "C_BEZIER_RECT",
                                            "width": 16,
                                            "length": 20
                                        }
                                    ],
                                },
                                {
                                    "offset": 11.5,
                                    "parts": [
                                        {
                                            "length": 67,
                                            "shape": "FEMALE"
                                        }
                                    ],
                                    "opposite": "1 down v-divider"
                                },
                                {
                                    "offset": 11.5,
                                    "parts": [
                                        {
                                            "offset": 23.5,
                                            "shape": "C_BEZIER_RECT",
                                            "width": 16,
                                            "length": 20
                                        }
                                    ],
                                },
                                {
                                    "offset": 11.5,
                                    "parts": [
                                        {
                                            "length": 67,
                                            "shape": "FEMALE"
                                        }
                                    ],
                                    "opposite": "2 down v-divider"
                                },
                                {
                                    "offset": 11.5,
                                    "parts": [
                                        {
                                            "offset": 23.5,
                                            "shape": "C_BEZIER_RECT",
                                            "width": 16,
                                            "length": 20
                                        }
                                    ],
                                },
                                {
                                    "offset": 11.5,
                                    "parts": [
                                        {
                                            "length": 67,
                                            "shape": "FEMALE"
                                        }
                                    ],
                                    "opposite": "3 down v-divider"
                                },
                                {
                                    "offset": 11.5,
                                    "parts": [
                                        {
                                            "offset": 23.5,
                                            "shape": "C_BEZIER_RECT",
                                            "width": 16,
                                            "length": 20
                                        }
                                    ],
                                },
                                {
                                    "offset": 11.5,
                                    "parts": [
                                        {
                                            "length": 67,
                                            "shape": "FEMALE"
                                        }
                                    ],
                                    "opposite": "4 down v-divider"
                                },
                                {
                                    "offset": 15,
                                    "parts": [
                                        {
                                            "offset": 23.5,
                                            "shape": "C_BEZIER_RECT",
                                            "width": 16,
                                            "length": 20
                                        }
                                    ],
                                },
                                {
                                    "offset": 44,
                                    "parts": [
                                        {
                                            "offset": 23.5,
                                            "shape": "C_BEZIER_RECT",
                                            "width": 16,
                                            "length": 20
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "short side wall 2",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.height"
                                },
                            ],
                            "holes": [
                                {
                                    "shape": "FEMALE",
                                    "offset": 67,
                                    "opposite": "middle h-divider"
                                },
                                {
                                    "offset": 28,
                                    "opposite": "1 small h-divider",
                                    "parts": [
                                        {
                                            "offset": 24,
                                            "length": 21,
                                            "shape": "FEMALE"
                                        },
                                        {
                                            "offset": 20,
                                            "length": 21,
                                            "shape": "FEMALE"
                                        }
                                    ]
                                }

                            ]
                        }
                    ],
                },
                {
                    "name": "long side wall",
                    "width": "tray.width",
                    "height": "tray.depth",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,

                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width",
                                    "pin_height": 0.5
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 22,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "1 up v-divider"
                                },{
                                    "offset": 62,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "2 up v-divider"
                                },{
                                    "offset": 58,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "3 up v-divider"
                                },{
                                    "offset": 67,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "4 up v-divider"
                                }
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "short side wall",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.width",
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
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "short side wall",
                    "width": "tray.height",
                    "height": "tray.depth",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 46,
                                    "opposite": "middle h-divider",
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
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.width"
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "long side wall",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "long side wall 2",
                    "width": "tray.width",
                    "height": "tray.depth",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width",
                                    "pin_height": 0.5
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 39,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "1 down v-divider"
                                },{
                                    "offset": 39,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "2 down v-divider"
                                },{
                                    "offset": 39,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "3 down v-divider"
                                },{
                                    "offset": 39,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "4 down v-divider"
                                }
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "short side wall",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.width",
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
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "short side wall 2",
                    "copy_of": "short side wall"
                },
                {
                    "name": "1 up v-divider",
                    "width": 46,
                    "height": "tray.depth",
                    "thickness": 2,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 16,
                                    "opposite": "1 small h-divider",
                                    "shape": "START_HALF_TAB"
                                }
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "long side wall",
                            "parts": [
                                {
                                    "tabs": "START_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                },
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "middle h-divider",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "2 up v-divider",
                    "copy_of": "1 up v-divider"
                },
                {
                    "name": "3 up v-divider",
                    "width": 46,
                    "height": "tray.depth",
                    "thickness": 2,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width",
                                    "indent": {
                                        "radius": 8,
                                        "offset": 15
                                    }
                                }
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "long side wall",
                            "parts": [
                                {
                                    "tabs": "START_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                },
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "long side wall 2",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "4 up v-divider",
                    "width": 46,
                    "height": "tray.depth",
                    "thickness": 2,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 22,
                                    "opposite": "2 small h-divider",
                                    "shape": "START_HALF_TAB"
                                }
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "long side wall",
                            "parts": [
                                {
                                    "tabs": "START_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                },
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "middle h-divider",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "1 down v-divider",
                    "width": 67,
                    "height": "tray.depth",
                    "thickness": 2,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width",
                                    "indent": {
                                        "offset": 25.5,
                                        "radius": 8
                                    }
                                }
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "long side wall 2",
                            "parts": [
                                {
                                    "tabs": "START_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                },
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "middle h-divider",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "2 down v-divider",
                    "copy_of": "1 down v-divider"

                },
                {
                    "name": "3 down v-divider",
                    "copy_of": "1 down v-divider"

                },
                {
                    "name": "4 down v-divider",
                    "copy_of": "1 down v-divider"

                },
                {
                    "name": "middle h-divider",
                    "width": "tray.width",
                    "height": "tray.depth",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": 24,
                                    "indent": {
                                        "offset": 3,
                                        "radius": 8
                                    }
                                },
                                {
                                    "tabs": "TOP",
                                    "length": 64,
                                    "indent": {
                                        "offset": 23,
                                        "radius": 8
                                    }
                                },
                                {
                                    "tabs": "TOP",
                                    "length": 191
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 22,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "1 up v-divider"
                                },{
                                    "offset": 62,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "2 up v-divider"
                                },{
                                    "offset": 26,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "4 down v-divider"
                                },{
                                    "offset": 30,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "3 up v-divider"
                                },{
                                    "offset": 7,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "3 down v-divider"
                                },{
                                    "offset": 39,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "2 down v-divider"
                                },{
                                    "offset": 16,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "4 up v-divider"
                                },{
                                    "offset": 21,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "1 down v-divider"
                                },
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "short side wall",
                            "parts": [
                                {
                                    "tabs": "START_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "short side wall 2",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],

                },

                {
                    "name": "1 small h-divider",
                    "width": 62,
                    "height": "tray.depth",
                    "thickness": 2,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
                                }
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "1 up v-divider",
                            "parts": [
                                {
                                    "tabs": "START_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "length": 21,
                                    "tabs": "FEMALE",
                                },
                                {
                                    "length": 20,
                                    "tabs": "TOP"
                                },
                                {
                                    "length": 21,
                                    "tabs": "FEMALE"

                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "2 up v-divider",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],

                },
                {
                    "name": "2 small h-divider",
                    "copy_of": "1 small h-divider"
                },
            ]
        },
        "monsters": {
            "dimensions": {
                "width": 269,
                "height": 124,
                "depth": 15
            },
            "pieces": [
                {
                    "name": "bottom",
                    "width": "tray.width",
                    "height": "tray.height",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,
                            "opposite": "long side wall",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 59,
                                    "parts": [
                                        {
                                            "length": 40,
                                            "shape": "FEMALE"
                                        },
                                        {
                                            "offset": 2,
                                            "shape": "FEMALE",
                                            "length": 40
                                        },
                                        {
                                            "offset": 2,
                                            "shape": "FEMALE",
                                            "length": 40
                                        }
                                    ],
                                    "opposite": "1 v-divider"
                                },
                                {
                                    "offset": 72,
                                    "parts": [
                                        {
                                            "length": 40,
                                            "shape": "FEMALE"
                                        },
                                        {
                                            "offset": 2,
                                            "shape": "FEMALE",
                                            "length": 40
                                        },
                                        {
                                            "offset": 2,
                                            "shape": "FEMALE",
                                            "length": 40
                                        }
                                    ],
                                    "opposite": "2 v-divider"
                                },
                                {
                                    "offset": 72,
                                    "opposite": "3 v-divider",
                                    "parts": [
                                        {
                                            "length": 40,
                                            "shape": "FEMALE"
                                        },
                                        {
                                            "offset": 2,
                                            "shape": "FEMALE",
                                            "length": 40
                                        },
                                        {
                                            "offset": 2,
                                            "shape": "FEMALE",
                                            "length": 40
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
                                    "length": "piece.height"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 40,
                                    "shape": "FEMALE",
                                    "opposite": "1 h-divider"
                                },
                                {
                                    "offset": 40,
                                    "shape": "FEMALE",
                                    "opposite": "2 h-divider"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "long side wall 2",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "short side wall 2",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.height"
                                },
                            ]
                        }
                    ],
                },
                {
                    "name": "long side wall",
                    "width": "tray.width",
                    "height": "tray.depth",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,

                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width",
                                    "pin_height": 0.5
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 59,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "1 v-divider"
                                },
                                {
                                    "offset": 72,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "2 v-divider"
                                },
                                {
                                    "offset": 72,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "3 v-divider"
                                }
                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "short side wall",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.width",
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
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "short side wall",
                    "width": "tray.height",
                    "height": "tray.depth",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 40,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "1 h-divider"
                                },
                                {
                                    "offset": 40,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "2 h-divider"
                                }
                            ]

                        },
                        {
                            "rotation": 1,
                            "opposite": "long side wall 2",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "MALE",
                                    "length": "piece.width"
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "long side wall",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.height"
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
                    "width": "tray.height",
                    "height": "tray.depth",
                    "thickness": 2,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 40,
                                    "opposite": "1 h-divider",
                                    "shape": "END_HALF_TAB"
                                },
                                {
                                    "offset": 40,
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
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "length": 40,
                                    "tabs": "FEMALE"
                                },
                                {
                                    "length": 2,
                                    "tabs": "TOP"
                                },
                                {
                                    "offset": 40,
                                    "tabs": "FEMALE",
                                    "length": 40
                                },
                                {
                                    "length": 2,
                                    "tabs": "TOP"
                                },
                                {
                                    "offset": 40,
                                    "tabs": "FEMALE",
                                    "length": 40
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "long side wall 2",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "2 v-divider",
                    "width": "tray.height",
                    "height": "tray.depth",
                    "thickness": 3,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width"
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 40,
                                    "opposite": "1 h-divider",
                                    "shape": "END_HALF_TAB"
                                },
                                {
                                    "offset": 40,
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
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "length": 40,
                                    "tabs": "FEMALE"
                                },
                                {
                                    "length": 2,
                                    "tabs": "TOP"
                                },
                                {
                                    "offset": 40,
                                    "tabs": "FEMALE",
                                    "length": 40
                                },
                                {
                                    "length": 2,
                                    "tabs": "TOP"
                                },
                                {
                                    "offset": 40,
                                    "tabs": "FEMALE",
                                    "length": 40
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "long side wall 2",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "3 v-divider",
                    "copy_of": "1 v-divider"
                },
                {
                    "name": "1 h-divider",
                    "width": "tray.width",
                    "height": "tray.depth",
                    "thickness": 2,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "tabs": "TOP",
                                    "length": "piece.width",
                                }
                            ],
                            "holes": [
                                {
                                    "offset": 59,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "1 v-divider"
                                },
                                {
                                    "offset": 72,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "2 v-divider"
                                },
                                {
                                    "offset": 72,
                                    "shape": "START_HALF_TAB",
                                    "opposite": "3 v-divider"
                                }

                            ]
                        },
                        {
                            "rotation": 1,
                            "opposite": "short side wall",
                            "parts": [
                                {
                                    "tabs": "START_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        },
                        {
                            "rotation": 2,
                            "opposite": "bottom",
                            "parts": [
                                {
                                    "tabs": "FEMALE",
                                    "length": "piece.width"
                                }
                            ]
                        },
                        {
                            "rotation": 3,
                            "opposite": "short side wall 2",
                            "parts": [
                                {
                                    "tabs": "END_HALF_TAB",
                                    "length": "piece.height"
                                }
                            ]
                        }
                    ],
                },
                {
                    "name": "2 h-divider",
                    "copy_of": "1 h-divider"
                },
                {
                    "name": "base plate short",
                    "thickness": 2,
                    "width": 39.5,
                    "height": 50,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "length": "piece.width",
                                    "tabs": "TOP"
                                }
                            ],
                        },
                        {
                            "rotation": 1,
                            "parts": [
                                {
                                    "length": "piece.height",
                                    "tabs": "TOP"
                                }
                            ],
                        },
                        {
                            "rotation": 2,
                            "parts": [
                                {
                                    "length": "piece.width",
                                    "tabs": "TOP"
                                }
                            ],
                        },
                        {
                            "rotation": 3,
                            "parts": [
                                {
                                    "length": "piece.height",
                                    "tabs": "TOP"
                                }
                            ],
                        }
                    ]
                },
                {
                    "name": "base plate short 2",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 3",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 4",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 5",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 6",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 7",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 8",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 9",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 10",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 11",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 12",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 13",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 14",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 15",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 16",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 17",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base plate short 18",
                    "copy_of": "base plate short"
                },
                {
                    "name": "base angle short",
                    "thickness": 2,
                    "width": 39.5,
                    "height": 9.3,
                    "edges": [
                        {
                            "rotation": 0,
                            "parts": [
                                {
                                    "length": "piece.width",
                                    "tabs": "TOP"
                                }
                            ],
                        },
                        {
                            "rotation": 1,
                            "parts": [
                                {
                                    "length": "piece.height",
                                    "tabs": "TOP"
                                }
                            ],
                        },
                        {
                            "rotation": 2,
                            "parts": [
                                {
                                    "length": "piece.width",
                                    "tabs": "TOP"
                                }
                            ],
                        },
                        {
                            "rotation": 3,
                            "parts": [
                                {
                                    "length": "piece.height",
                                    "tabs": "TOP"
                                }
                            ],
                        }
                    ]
                },
                {
                    "name": "base angle short 2",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 3",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 4",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 5",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 6",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 7",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 8",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 9",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 10",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 11",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 12",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 13",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 14",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 15",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 16",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 17",
                    "copy_of": "base angle short"
                },
                {
                    "name": "base angle short 18",
                    "copy_of": "base angle short"
                },
            ]
        }
    }

    dimensions = trays[tray_name]["dimensions"]
    dims = {
        "tray.width": dimensions["width"],
        "tray.height": dimensions["height"],
        "tray.depth": dimensions["depth"]
    }
    pieces = trays[tray_name]["pieces"]
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
        for dim_key in ["width", "height"]:
            if piece[dim_key] in dims.keys():
                piece[dim_key] = dims[piece[dim_key]]

        piece_width = piece["width"]
        piece_height = piece["height"]

        for edge in piece["edges"]:
            for part in edge["parts"]:
                if part["length"] is "piece.width":
                    part["length"] = piece_width
                elif part["length"] is "piece.height":
                    part["length"] = piece_height

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

