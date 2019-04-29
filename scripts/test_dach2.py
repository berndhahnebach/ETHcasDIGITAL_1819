# ***************************************************************************
import os
import FreeCAD
import Arch
import Draft
import importIFC
from FreeCAD import Vector as vec


# ***************************************************************************
# geometry input data, all units in mm
haus_t = 8000  # Aeusseres Rohbaumass
haus_b = 6000  # Abstand zwischen Wandinnenseiten (nutzbare breite)
haus_h = 3000  # OK roh BPL bis UK roh decke
base_x = 0
base_y = 0
eg_boden_fertig = 0.0  # base_z
eg_boden_roh = -200  # Bodenaufbau im EG
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

import Part
l1 = Part.makeLine(P1, P2)
l2 = Part.makeLine(P2, P3)
l3 = Part.makeLine(P3, P4)
l4 = Part.makeLine(P4, P1)
face1 = Part.Face(Part.Wire([l1, l2, l3, l4]))
schwerpunkt_face1 = face1.CenterOfMass
P5 = vec(
    schwerpunkt_face1.x,
    schwerpunkt_face1.y,
    haus_h+eg_boden_roh+dach_dicke-100,
)
l5 = Part.makeLine(P1, P5)
l6 = Part.makeLine(P2, P5)
l7 = Part.makeLine(P3, P5)
l8 = Part.makeLine(P4, P5)
face2 = Part.Face(Part.Wire([l1, l6, l5]))
face3 = Part.Face(Part.Wire([l2, l7, l6]))
face4 = Part.Face(Part.Wire([l3, l8, l7]))
face5 = Part.Face(Part.Wire([l4, l5, l8]))
dablauf_partobj = FreeCAD.ActiveDocument.addObject("Part::Feature","dablauf_solid")
dablauf_partobj.Shape = Part.Solid(Part.Shell([face1, face2, face3, face4, face5,]))
dablauf_obj = Arch.makeStructure(baseobj=dablauf_partobj)
Arch.removeComponents([dablauf_obj],dach_obj)
App.ActiveDocument.recompute()
