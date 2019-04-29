eg_boden_fertig = 0.0
eg_boden_roh = -200
haus_t = 8000
haus_b = 6000
haus_h = 3000
haus_base = 0
trennwand_dicke = 300



import os
import FreeCAD
import Arch
import Draft
import importIFC
from FreeCAD import Vector as vec






# trennwand
trennwand_base = Draft.makeLine(
    vec(haus_base, 0, eg_boden_roh), vec(haus_base, haus_t, eg_boden_roh)
)
trennwand_wand = Arch.makeWall(
    trennwand_base,  length=None, width=trennwand_dicke, height=haus_h
)


Draft.makeLine(
    vec(0, 0, 0), vec(1, 1, 1)
)




pl_base = FreeCAD.Vector(1000,0.0,1000)
place=FreeCAD.Placement(pl_base, FreeCAD.Rotation(vec(1, 0, 0), 90))
win = Arch.makeWindowPreset(
    "Fixed",width=1000.0,height=1000.0,h1=100.0,h2=100.0,h3=100.0,w1=200.0,w2=100.0,o1=0.0,o2=100.0,placement=place
)
win.Hosts = [FreeCAD.ActiveDocument.Wall001]
App.activeDocument().recompute()


