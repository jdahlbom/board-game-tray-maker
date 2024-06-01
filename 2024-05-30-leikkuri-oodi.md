2024-05-30

Epilog Fusion M2 laser cutter
CorelDraw
Inkscape

Cutting Spirit Island tray

- Inkscape shows different mm widths than specification file shows.
- Card tray base is specified as 94.5 mm wide. Unscaled result in Inkscape is
  25.321 mm. Let's assume everything needs to be scale up by 3.732.
  - Previous log used 378% as the scaling multiplier. I assume this is the
    same problem as back then.
    
- Let's print the power card trays first, as this was the primary goal.

- The spacers have some off by few mm -error, this probably is due to changes
  to the indentation feature. Will have to try and fit the pieces together.
  
- Didn't have time enough: 35 min went to organizing stuff in Inkscape and figuring
out the scaling ratio. 15 min to cutting 3mm plywood and 5+5 minutes to troubleshooting
and cutting 1mm plywood.

- Card slots are too narrow by 3-5 mm. Will have to track the error down.
  - Error was in the card dimensions: I took them directly from Mayday Standard Sleeve
    package, but didn't realize that was the max size of a card, not the outer dimensions
    of the sleeve.

- Resizing the elements and manually laying out the separate objects is a nuisance
  that takes too much precious laser cutter lab time. Will have to prioritize these
  fixes soon.


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

