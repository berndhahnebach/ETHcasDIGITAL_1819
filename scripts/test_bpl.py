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
