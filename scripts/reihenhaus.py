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


# ***************************************************************************
import os
import FreeCAD
import Arch
import Draft
import importIFC
from FreeCAD import Vector as vec


# ***************************************************************************
# tested on FreeCAD 0.19 dev (patched by Bernd)


# ***************************************************************************
# how to run in a Python console in FreeCAD Gui or in FreeCADCmd

# to run the script a first time copy the following lines
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

haus_anzahl = 4


# get doc name and export name
doc_name = os.path.splitext(os.path.basename(str(__file__)))[0]
export_file = str(__file__).rstrip('.py')


# create a new document, to have something to put the objects in
doc_obj = FreeCAD.newDocument(doc_name)


# list to save the objects which will be exported to ifc
obj_ifc = []


# add some columns to the document
for i, hs in enumerate(range(haus_anzahl)):

    # *******************************************
    anfhaus = 0
    endhaus = haus_anzahl - 1

    # *******************************************
    # trennwaende, anfangswand
    Trenn_wand_name = "Trennwand" + str(i + 1)
    trennwand_base = Draft.makeLine(
        vec(base_x, base_y, eg_boden_roh),
        vec(base_x, haus_t, eg_boden_roh)
    )
    if i == anfhaus:
        anfangswand_wand = Arch.makeWall(
            trennwand_base,
            length=None,
            width=seitenwand_dicke,
            height=haus_h,
            align="Left",
            name="Anfwand"
        )
        obj_ifc.append(anfangswand_wand)
    else:
        trennwand_wand = Arch.makeWall(
            trennwand_base,
            length=None,
            width=trennwand_dicke,
            height=haus_h,
            align="Left",
            name=Trenn_wand_name
        )
        obj_ifc.append(trennwand_wand)

    # *******************************************
    # endwand
    if i == endhaus:
        endwand_base = Draft.makeLine(
            vec(base_x + haus_b + seitenwand_dicke, base_y, eg_boden_roh),
            vec(base_x + haus_b + seitenwand_dicke, haus_t, eg_boden_roh)
        )
        endwand_wand = Arch.makeWall(
                endwand_base,
                length=None,
                width=seitenwand_dicke,
                height=haus_h,
                align="Left",
                name="Endwand"
        )
        obj_ifc.append(endwand_wand)

    # *******************************************
    # vorderwand
    if i == anfhaus:
        vorderwand_base = Draft.makeLine(
            vec(base_x + seitenwand_dicke, base_y, eg_boden_roh),
            vec(base_x + haus_b, base_y, eg_boden_roh)
        )
    elif i == endhaus:
        vorderwand_base = Draft.makeLine(
            vec(base_x + trennwand_dicke, base_y, eg_boden_roh),
            vec(base_x + haus_b + seitenwand_dicke, base_y, eg_boden_roh)
        )
    else:
        vorderwand_base = Draft.makeLine(
            vec(base_x + trennwand_dicke, base_y, eg_boden_roh),
            vec(base_x + haus_b, base_y, eg_boden_roh)
        )
    vor_wand_name = "Vorwand" + str(i + 1)
    vorderwand_wand = Arch.makeWall(
        vorderwand_base,
        length=None,
        width=vorderwand_dicke,
        height=haus_h,
        align="Right",
        name=vor_wand_name
    )
    obj_ifc.append(vorderwand_wand)
    doc_obj.recompute()

    # *******************************************
    # fenster in vorderwand
    place = FreeCAD.Placement(
        vec(base_x + 1000, 0.0, 1000),
        FreeCAD.Rotation(vec(1, 0, 0), 90)
    )
    win = Arch.makeWindowPreset(
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
        placement=place
    )
    win.Hosts = [vorderwand_wand]
    doc_obj.recompute()

    # *******************************************
    # tuer in vorderwand
    place = FreeCAD.Placement(
        vec(base_x + 4000, 0.0, eg_boden_roh),
        FreeCAD.Rotation(vec(1, 0, 0), 90)
    )
    win = Arch.makeWindowPreset(
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
        placement=place
    )
    win.Hosts = [vorderwand_wand]
    doc_obj.recompute()

    # *******************************************
    # rueckwand als riesenfenster 
    if i == anfhaus:
        pass
    elif i == endhaus:
        pass
    
    else:
        pass
    
    place = FreeCAD.Placement(
        vec(base_x + trennwand_dicke, haus_t-200, eg_boden_roh),
        FreeCAD.Rotation(vec(1, 0, 0), 90)
    )
    win = Arch.makeWindowPreset(
        "Fixed",
        width=haus_b-trennwand_dicke,
        height=haus_h,
        h1=100.0,
        h2=100.0,
        h3=100.0,
        w1=200.0,
        w2=100.0,
        o1=0.0,
        o2=100.0,
        placement=place
    )
    win.Hosts = []
    doc_obj.recompute()

    # *******************************************
    base_x += haus_b


'''
# dimensions
dim1 = Draft.makeDimension(
    vec(base_x, base_y, eg_boden_roh), vec(base_x, base_y, eg_boden_roh)
)
'''

# recompute the document
doc_obj.recompute()


# export objects to ifc
importIFC.export(obj_ifc, export_file + ".ifc")


# save and close document
doc_obj.saveAs(export_file + ".FCStd")
FreeCAD.closeDocument(doc_name)


# print some status everything worked out very well :-)
print(
    '\n{} created and saved into {}.FCStd\n'
    'as well as exported to {}.ifc\n'
    .format(doc_name, export_file, export_file)
)
