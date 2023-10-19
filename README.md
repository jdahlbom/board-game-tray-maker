Board game tray generator
=========================

SVG generator script for generating board game trays from high level description
of component sizes.

Measurement dimensions
======================
In code I use dimensions *width*, *height* and *depth*. These are used as if I were looking
at a game box / component tray from above: Depth dimension is the one depicting the up/down 
measurement while width and height are horizontal directions.


ACKNOWLEDGEMENTS
----------------
This generator project started out as a fork of TabbedBoxMaker:
"Original box maker by Elliot White - http://www.twot.eu/111000/111000.html 
Heavily modified by Paul Hutchison"
https://github.com/paulh-rnd/TabbedBoxMaker

It served as a easy way into SVG generation and using Inkscape for laser cutting files.
I have since rewritten the whole codebase to use different abstraction, and using 
Python 3 while at it. Inkscape no longer has any part in the SVG generation, although
I primarily use Inkscape to view what I have generated.


Usage
-----
`python3 generate-svg-from-columns.py games/<game>/<trayspec.json>`

