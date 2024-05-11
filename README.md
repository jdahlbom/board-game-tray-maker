Board game tray generator
=========================

SVG generator script for generating board game trays from high level description
of component sizes.

The tray generator aims to one day generate board game trays from just
the information about number, size and possible grouping of components
and the dimensions of the containing game box.

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

I owe a debt of gratitude to Hutchison and White
for giving a valuable starting point, and few improvements that they have added
during the lifetime of this project.

Usage
-----
`python3 main.py <specsfile.json> [ 'Single tray name']`
