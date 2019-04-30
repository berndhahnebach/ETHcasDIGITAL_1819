

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



hbase_x = base_x

# vorderwand
vorderwand_base = Draft.makeLine(
    vec(hbase_x, base_y, eg_boden_roh),
    vec(hbase_x + haus_b, base_y, eg_boden_roh)
)
vor_wand_name = "Vorwand"
vorderwand_obj = Arch.makeWall(
    vorderwand_base,
    length=None,
    width=vorderwand_dicke,
    height=haus_h,
    align="Right",
    name=vor_wand_name
)

App.ActiveDocument.recompute()

# *******************************************
# fenster in vorderwand
eg_win_place = FreeCAD.Placement(
    vec(hbase_x + 1000, 0.0, 1000),
    FreeCAD.Rotation(vec(1, 0, 0), 90)
)
eg_win_obj = Arch.makeWindowPreset(
    "Fixed",
    width=1000.0,
    height=1000.0,
    h1=100.0,
    h2=100.0,
    h3=100.0,
    w1=200.0,
    w2=100.0,
    o1=0.0,
    o2=100.0,
    placement=eg_win_place
)
eg_win_obj.Hosts = [vorderwand_obj]

App.ActiveDocument.recompute()




