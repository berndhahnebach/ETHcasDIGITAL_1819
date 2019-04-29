import os
import FreeCAD
import Arch
import Draft
import importIFC
from FreeCAD import Vector as vec


eg_boden_fertig = 0.0
eg_boden_roh = -200
haus_t = 8000
haus_b = 6000
haus_h = 3000
base_x = 0
base_y = 0
trennwand_dicke = 300
seitenwand_dicke = 175
vorderwand_dicke = 125
bpl_dicke = 250
dach_dicke = 300

haus_anzahl = 4

# init of some values needed
reihenhaus_laenge = haus_anzahl * (haus_b + trennwand_dicke) - trennwand_dicke + 2 * seitenwand_dicke
hbase_x = base_x  # local x-base of every house, start with global x-base
obj_ifc = []


# **************************************************************************************

# *******************************************
# bodenplatte
bpl_place = FreeCAD.Placement(
    vec(base_x-seitenwand_dicke, base_y, eg_boden_roh),
    FreeCAD.Rotation(vec(0, 0, 1), 0)
)
bpl_base = Draft.makeRectangle(
    length=reihenhaus_laenge,
    height=haus_t,
    placement=bpl_place
)
bpl_obj = Arch.makeStructure(
    baseobj=bpl_base,
    height=bpl_dicke
)
# structure will be extruded in positive z
# thus set extrude Normale downwards
bpl_obj.Normal = vec(0, 0, -1)
doc_obj.recompute()


# *******************************************
# dach
dach_place = FreeCAD.Placement(
    vec(base_x-seitenwand_dicke, base_y, haus_h + eg_boden_roh),
    FreeCAD.Rotation(vec(0, 0, 1), 0)
)
dach_base = Draft.makeRectangle(
    length=reihenhaus_laenge,
    height=haus_t,
    placement=dach_place
)
dach_obj = Arch.makeStructure(
    baseobj=dach_base,
    height=dach_dicke
)


# *******************************************
# dachablauf
P1 = vec(
    base_x-seitenwand_dicke,
    base_y,
    haus_h+eg_boden_roh+dach_dicke,
)
P2 = vec(
    base_x-seitenwand_dicke,
    base_y+haus_t,
    haus_h+eg_boden_roh+dach_dicke,
)
P3 = vec(
    base_x-seitenwand_dicke+haus_b,
    base_y+haus_t,
    haus_h+eg_boden_roh+dach_dicke,
)
P4 = vec(
    base_x-seitenwand_dicke+haus_b,
    base_y,
    haus_h+eg_boden_roh+dach_dicke,
)
W1 = Draft.makeWire([P1, P2, P3, P4], closed=True)
App.ActiveDocument.recompute()
schwerpunkt_W1 = W1.Shape.CenterOfMass
P5 = vec(
    schwerpunkt_W1.x,
    schwerpunkt_W1.y,
    haus_h+eg_boden_roh+dach_dicke-100,
)
W2 = Draft.makeWire([P1, P2, P5], closed=True)
W3 = Draft.makeWire([P2, P3, P5], closed=True)
W4 = Draft.makeWire([P3, P4, P5], closed=True)
W5 = Draft.makeWire([P4, P1, P5], closed=True)
App.ActiveDocument.recompute()
Shell = Draft.upgrade([W1, W2, W3, W4, W5], delete=True)[0][0]
App.ActiveDocument.recompute()
Solid = Draft.upgrade([Shell], delete=True)[0][0]
App.ActiveDocument.recompute()

Arch.removeComponents([Solid],dach_obj)
App.ActiveDocument.recompute()
