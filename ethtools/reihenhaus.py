# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2019 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import os

import FreeCAD
import Arch
import Draft
import Part
import importIFC
from FreeCAD import Vector as vec
if FreeCAD.GuiUp:
    import FreeCADGui


# tested on FreeCAD 0.19.16587


# ***************************************************************************
# how to run in a Python console in FreeCAD Gui or in FreeCADCmd
# copy the lines without the ''' into the FreeCAD Python console

# first run after start
'''
from ethtools import reihenhaus

'''


# rerun the script after changes, the import needs to be done only once
'''
from importlib import reload
reload(reihenhaus)

'''


# ***************************************************************************
FreeCAD.Console.PrintMessage(
    "\nETH-Reihenhaus, a more sophisticated example\n"
)
if FreeCAD.GuiUp:
    FreeCADGui.updateGui()
    # this will print message above immediately


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
haus_summe = haus_anzahl * (haus_b + trennwand_dicke)
reihenhaus_laenge = haus_summe - trennwand_dicke + 2 * seitenwand_dicke
hbase_x = base_x  # local x-base of every house, start with global x-base


# ***************************************************************************
# get doc name and export file name, create a new document
doc_name = os.path.splitext(os.path.basename(str(__file__)))[0]
export_file = os.path.join(os.path.expanduser('~'), 'Desktop', doc_name)
doc_obj = FreeCAD.newDocument(doc_name)

# the container
site = Arch.makeSite([], name="ETH-Reihenhaus")
raeume_site = Arch.makeSite([], name="ETH-Reihenhaus")
raeume_building = Arch.makeBuilding([], name="Reihenhaus_Raeume")
Arch.addComponents(raeume_building, raeume_site)

# the materials, windows, doors and spaces do not get a material
brick = Arch.makeMaterial('Backstein')
concrete = Arch.makeMaterial('Beton')
brick.Color = (1.0, 0.502, 0.0, 0.0)
concrete.Color = (0.439, 1.0, 0.439, 0.0)

# ***************************************************************************
# lets start with geometry creation

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
bpl_obj.IfcType = 'Footing'
bpl_obj.PredefinedType = 'USERDEFINED'
bpl_obj.IfcProperties = {
    'FireRating': 'Pset_ETHCommon;;IfcLabel;;EI90',
    'IsExternal': 'Pset_ETHCommon;;IfcBoolean;;False',
    'LoadBearing': 'Pset_ETHCommon;;IfcBoolean;;True',
    'Status': 'Pset_ETHCommon;;IfcLabel;;New'
}
bpl_obj.Material = concrete
doc_obj.recompute()
bpl_building = Arch.makeBuilding([bpl_obj], name="Reihenhaus_Fundation")
Arch.addComponents(bpl_building, site)


doc_obj.recompute()


# ***************************************************************************
# nice model display in Gui
if FreeCAD.GuiUp:
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.ActiveDocument.activeView().viewIsometric()


# export objects to ifc
importIFC.export(site, export_file + "_std.ifc")
# importIFC.export(raeume_site, export_file + "_raeume.ifc")

# save and close document
doc_obj.saveAs(export_file + ".FCStd")
FreeCAD.closeDocument(doc_name)


# print some status everything worked out very well :-)
FreeCAD.Console.PrintMessage(
    '* {0} created and saved into {1}.FCStd\n'
    '* objects exported to {1}_std.ifc\n'
    '* spaces exported to {1}_raeume.ifc\n'
    .format(doc_name, export_file, export_file)
)


'''
reload(reihenhaus)

'''
