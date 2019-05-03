# ***************************************************************************
# *   Copyright (c) 2019 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import os

import FreeCAD
import Arch
import importIFC


# tested on FreeCAD 0.19.16587


# ***************************************************************************
# how to run in a Python console in FreeCAD Gui or in FreeCADCmd
# copy the lines without the ''' into the FreeCAD Python console

# first run after start
'''
from ethtools import columngrid

'''


# rerun the script after changes, the import needs to be done only once
'''
from importlib import reload
reload(columngrid)

'''


# ***************************************************************************
# lets start with a simple columns grid
FreeCAD.Console.PrintMessage("\nLet's start with a simple columns grid\n")


# geometry input data, all units in mm
h = 500.0  # hoehe
w1 = 2000.0  # breite 1
w2 = 2000.0  # breite 2
ax = 7500.0  # abstand x
ay = 12000.0  # abstand y
nx = 25  # anzahl x
ny = 3  # anzahl y


# get doc name and export file name
doc_name = os.path.splitext(os.path.basename(str(__file__)))[0]
export_file = os.path.join(os.path.expanduser('~'), 'Desktop', doc_name)


# create a new FreeCAD document, to have something to put the objects in
doc_obj = FreeCAD.newDocument(doc_name)


# a list to put the objects in which will be exported to ifc
obj_ifc = []


# add some columns to the document
for ix in range(nx):
    for iy in range(ny):
        col = Arch.makeStructure(None, length=w1, width=w2, height=h)
        col.Placement.Base = FreeCAD.Vector(ix * ax, iy * ay, 0.0)
        col.Label = 'Odilos Fundament'
        col.IfcType = 'Footing'
        obj_ifc.append(col)


# recompute the document
doc_obj.recompute()


# export objects to ifc
importIFC.export(obj_ifc, export_file + ".ifc")


# save and close document
doc_obj.saveAs(export_file + ".FCStd")
FreeCAD.closeDocument(doc_name)


# print some status everything worked out very well :-)
FreeCAD.Console.PrintMessage(
    '* {0} created and saved into {1}.FCStd\n'
    '* columns exported to {1}.ifc\n'
    .format(doc_name, export_file, export_file)
)
