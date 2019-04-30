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


# ***************************************************************************
# to run the script a first time copy the following lines
# the script has to be in directory YOURHOME/Desktop/ETH-FreeCAD/scripts
# works on Linux and Windows
# without the ''' in the FreeCADCmd Python console
'''
import sys, os, importlib
sys.path.append(os.path.join(os.path.expanduser('~'), 'Desktop', 'ETH-FreeCAD', 'scripts'))
import reihenhaus


'''


# to reload the scrip copy the following line
# without the ''' in the FreeCADCmd Python console
'''
importlib.reload(reihenhaus)

'''

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
haus_summe = haus_anzahl * (haus_b + trennwand_dicke)
reihenhaus_laenge = haus_summe - trennwand_dicke + 2 * seitenwand_dicke
hbase_x = base_x  # local x-base of every house, start with global x-base


# ***************************************************************************
# get doc name and export name
export_file = str(__file__).rstrip('.py')
doc_name = os.path.splitext(os.path.basename(str(__file__)))[0]
doc_obj = FreeCAD.newDocument(doc_name)

# the container
site = Arch.makeSite([], name="ETH-Reihenhaus")
raeume_site = Arch.makeSite([], name="ETH-Reihenhaus")
raeume_building = Arch.makeBuilding([], name="Reihenhaus_Raeume")
Arch.addComponents(raeume_building, raeume_site)


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
bpl_building = Arch.makeBuilding([bpl_obj], name="Reihenhaus_Fundation")
Arch.addComponents(bpl_building, site)


for i, hs in enumerate(range(haus_anzahl)):

    # *******************************************
    # helper to easily find anfangshaus and endhaus
    anfhaus = True if i == 0 else False
    endhaus = True if i == (haus_anzahl - 1) else False

    # *******************************************
    # group objs
    building = Arch.makeBuilding([], name="Haus_"+str(i+1))
    Arch.addComponents(building, site)

    # *******************************************
    # trennwand
    trennwand_name = "Trennwand" + str(i + 1)
    trennwand_base = Draft.makeLine(
        vec(hbase_x, base_y, eg_boden_roh),
        vec(hbase_x, haus_t, eg_boden_roh)
    )
    if anfhaus:
        # trennwand ist Seitenwand
        trennwand_width = seitenwand_dicke
    else:
        trennwand_width = trennwand_dicke
    trennwand_obj = Arch.makeWall(
        trennwand_base,
        length=None,
        width=trennwand_width,
        height=haus_h,
        align="Right",
        name=trennwand_name
    )
    trennwand_obj.IfcProperties = {
        'FireRating': 'Pset_ETHCommon;;IfcLabel;;EI90',
        'IsExternal': 'Pset_ETHCommon;;IfcBoolean;;False',
        'LoadBearing': 'Pset_ETHCommon;;IfcBoolean;;True',
        'Status': 'Pset_ETHCommon;;IfcLabel;;New'
    }
    Arch.addComponents(trennwand_obj, building)

    # *******************************************
    # endwand
    if endhaus:
        endwand_base = Draft.makeLine(
            vec(hbase_x + haus_b + seitenwand_dicke, base_y, eg_boden_roh),
            vec(hbase_x + haus_b + seitenwand_dicke, haus_t, eg_boden_roh)
        )
        endwand_obj = Arch.makeWall(
                endwand_base,
                length=None,
                width=seitenwand_dicke,
                height=haus_h,
                align="Right",
                name="Endwand"
        )
        endwand_obj.IfcProperties = {
            'FireRating': 'Pset_ETHCommon;;IfcLabel;;EI90',
            'IsExternal': 'Pset_ETHCommon;;IfcBoolean;;False',
            'LoadBearing': 'Pset_ETHCommon;;IfcBoolean;;True',
            'Status': 'Pset_ETHCommon;;IfcLabel;;New'
        }
        Arch.addComponents(endwand_obj, building)

    # *******************************************
    # vorderwand
    vorderwand_base = Draft.makeLine(
        vec(hbase_x, base_y, eg_boden_roh),
        vec(hbase_x + haus_b, base_y, eg_boden_roh)
    )
    vor_wand_name = "Vorwand" + str(i + 1)
    vorderwand_obj = Arch.makeWall(
        vorderwand_base,
        length=None,
        width=vorderwand_dicke,
        height=haus_h,
        align="Right",
        name=vor_wand_name
    )
    vorderwand_obj.IfcProperties = {
        'FireRating': 'Pset_ETHCommon;;IfcLabel;;EI90',
        'IsExternal': 'Pset_ETHCommon;;IfcBoolean;;False',
        'LoadBearing': 'Pset_ETHCommon;;IfcBoolean;;True',
        'Status': 'Pset_ETHCommon;;IfcLabel;;New'
    }
    Arch.addComponents(vorderwand_obj, building)

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
    eg_win_obj.IfcProperties = {
        'FireRating': 'Pset_ETHCommon;;IfcLabel;;EI90',
        'IsExternal': 'Pset_ETHCommon;;IfcBoolean;;False',
        'LoadBearing': 'Pset_ETHCommon;;IfcBoolean;;True',
        'Status': 'Pset_ETHCommon;;IfcLabel;;New'
    }
    doc_obj.recompute()

    # *******************************************
    # tuer in vorderwand
    haupttuer_place = FreeCAD.Placement(
        vec(hbase_x + 4000, 0.0, eg_boden_roh),
        FreeCAD.Rotation(vec(1, 0, 0), 90)
    )
    haupttuer_obj = Arch.makeWindowPreset(
        "Glass door",
        width=1000.0,
        height=2000.0,
        h1=100.0,
        h2=100.0,
        h3=100.0,
        w1=200.0,
        w2=100.0,
        o1=0.0,
        o2=100.0,
        placement=haupttuer_place
    )
    haupttuer_obj.Hosts = [vorderwand_obj]
    haupttuer_obj.IfcProperties = {
        'FireRating': 'Pset_ETHCommon;;IfcLabel;;EI90',
        'IsExternal': 'Pset_ETHCommon;;IfcBoolean;;False',
        'LoadBearing': 'Pset_ETHCommon;;IfcBoolean;;True',
        'Status': 'Pset_ETHCommon;;IfcLabel;;New'
    }
    doc_obj.recompute()

    # *******************************************
    # rueckwand als riesenfenster
    terrasse_win_place = FreeCAD.Placement(
        vec(hbase_x, haus_t-200, eg_boden_roh),
        FreeCAD.Rotation(vec(1, 0, 0), 90)
    )
    terrasse_win_obj = Arch.makeWindowPreset(
        "Fixed",
        width=haus_b,
        height=haus_h,
        h1=100.0,
        h2=100.0,
        h3=100.0,
        w1=200.0,
        w2=100.0,
        o1=0.0,
        o2=100.0,
        placement=terrasse_win_place
    )
    terrasse_win_obj.Hosts = []
    terrasse_win_obj.IfcProperties = {
        'FireRating': 'Pset_ETHCommon;;IfcLabel;;EI90',
        'IsExternal': 'Pset_ETHCommon;;IfcBoolean;;False',
        'LoadBearing': 'Pset_ETHCommon;;IfcBoolean;;True',
        'Status': 'Pset_ETHCommon;;IfcLabel;;New'
    }
    doc_obj.recompute()
    Arch.addComponents(terrasse_win_obj, building)

    # *******************************************
    # dach mit ablauf
    if anfhaus:
        P1 = vec(
            hbase_x-seitenwand_dicke,
            base_y,
            haus_h+eg_boden_roh+dach_dicke,
        )
        P2 = vec(
            hbase_x-seitenwand_dicke,
            base_y+haus_t,
            haus_h+eg_boden_roh+dach_dicke,
        )
    else:
        P1 = vec(
            hbase_x-0.5*trennwand_dicke,
            base_y,
            haus_h+eg_boden_roh+dach_dicke,
        )
        P2 = vec(
            hbase_x-0.5*trennwand_dicke,
            base_y+haus_t,
            haus_h+eg_boden_roh+dach_dicke,
        )
    if endhaus:
        P3 = vec(
            hbase_x+haus_b+seitenwand_dicke,
            base_y+haus_t,
            haus_h+eg_boden_roh+dach_dicke,
        )
        P4 = vec(
            hbase_x+haus_b+seitenwand_dicke,
            base_y,
            haus_h+eg_boden_roh+dach_dicke,
        )
    else:
        P3 = vec(
            hbase_x+haus_b+0.5*trennwand_dicke,
            base_y+haus_t,
            haus_h+eg_boden_roh+dach_dicke,
        )
        P4 = vec(
            hbase_x+haus_b+0.5*trennwand_dicke,
            base_y,
            haus_h+eg_boden_roh+dach_dicke,
        )
        # make lines and Faces out of the Points
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
    dablauf_partobj = FreeCAD.ActiveDocument.addObject("Part::Feature", "dablauf_solid")
    dablauf_partobj.Shape = Part.Solid(Part.Shell([face1, face2, face3, face4, face5]))

    # arch ablaufobjekt (riesen aussparung)
    dablauf_obj = Arch.makeStructure(baseobj=dablauf_partobj)

    # dach
    dach_base = Draft.makeWire([P1, P2, P3, P4], closed=True)
    dach_obj = Arch.makeStructure(
        baseobj=dach_base,
        height=dach_dicke
    )
    # geneigtes dach mit ablauf, remove dachablauf from dach
    Arch.removeComponents([dablauf_obj], dach_obj)
    doc_obj.recompute()
    dach_obj.IfcType = 'Roof'
    dach_obj.IfcProperties = {
        'FireRating': 'Pset_ETHCommon;;IfcLabel;;EI90',
        'IsExternal': 'Pset_ETHCommon;;IfcBoolean;;False',
        'LoadBearing': 'Pset_ETHCommon;;IfcBoolean;;True',
        'Status': 'Pset_ETHCommon;;IfcLabel;;New'
    }
    Arch.addComponents(dach_obj, building)

    # *******************************************
    # raeume
    raum_partobj = doc_obj.addObject("Part::Box", "Raum_part")
    raum_partobj.Length = haus_b
    raum_partobj.Width = haus_t
    raum_partobj.Height = haus_h
    raum_partobj.Placement.Base = (hbase_x, base_y, eg_boden_roh)
    raum_obj = Arch.makeSpace(raum_partobj)
    doc_obj.recompute()
    raum_obj.IfcProperties = {
        'FireRating': 'Pset_ETHCommon;;IfcLabel;;EI90',
        'IsExternal': 'Pset_ETHCommon;;IfcBoolean;;False',
        'LoadBearing': 'Pset_ETHCommon;;IfcBoolean;;True',
        'Status': 'Pset_ETHCommon;;IfcLabel;;New'
    }
    Arch.addComponents(raum_obj, raeume_building)

    # *******************************************
    #  set hbase_x to the next haus
    hbase_x += (haus_b + trennwand_dicke)
doc_obj.recompute()


# ***************************************************************************
# nice model display in Gui
if FreeCAD.GuiUp:
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.ActiveDocument.activeView().viewIsometric()


# export objects to ifc
importIFC.export(site, export_file + "_std.ifc")
importIFC.export(raeume_site, export_file + "_raeume.ifc")

# save and close document
doc_obj.saveAs(export_file + ".FCStd")
FreeCAD.closeDocument(doc_name)


# print some status everything worked out very well :-)
print(
    '\n* {0} created and saved into {1}.FCStd\n'
    '* objects exported to {1}_std.ifc\n'
    '* spaces exported to {1}_raeume.ifc\n'
    .format(doc_name, export_file, export_file)
)


'''
importlib.reload(reihenhaus)

'''
