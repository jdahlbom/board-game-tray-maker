2023-10-23
Fusion Epilog M2 ?

Oodi


Coreldraw -> Files -> Import

The SVG library produces a scale that does not translate properly to CorelDraw.
For some reason this time the correct multiplier is 378% for both axis.
This is easiest to verify by selecting a known sized object in both Inkscape and Coreldraw and
just calculating the scale from those values.

The line width in CorelDraw has to be "Hairline" for cutting.
Supposedly any other line width would be engraving

Steps to produce:
- Set the laser head to correct height
- Set the laser head origin point to correct left top corner 
  -- remember that the printer may decide to start from some other point of your SVG 
     path and return to the topmost left point later on.
  -- Origin point must be saved by pressing the joystick down while in origin-setting mode.
- File -> Print
- Set the printer settings to match the material settings described in the workshop folder.
  - The kerf value of 0.2mm is pretty correct for cutting line width. To make tight fitting toothing this
    must be accounted for. The marginal is not big, so I recommend having a test piece for trying out the kerf
    settings.

- Air conditioning in Oodi work shop: On the opposite corner there is a air conditioning control button.
  Next to the printer there is a extension cord with a power switch that needs to be switched on before starting
  printing and off once you are done.


Design mistakes this time:

- Kerf correction is missing from the toothing - this leads to joins that do not actually stick at all
  and need to be glued together.
- There are still extra "slots" that are caused by some mistake where each actual slot gets an ending spacer,
  and thus creates a new slot for the last extra space.
  - Looks like the extra space allocation function happens too late in the process, so that side edge
    spacer holes are mismatched. The slot sizes should be fixed in the slot configuration before
    starting the actual edge generation. Any elasticity should be handled before this point.

