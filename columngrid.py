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
# tested on FreeCAD 0.18.1 aka 0.18.16110


# ***************************************************************************
# how to run in a Python console in FreeCAD Gui or in FreeCADCmd

# to run the script a first time copy the following lines 
# without the ''' in the FreeCADCmd Python console
'''
import sys, os, importlib
sys.path.append(os.path.join(os.path.expanduser('~'), 'Desktop', 'ETH-FreeCAD', 'scripts'))
import columngrid


'''


# to reload the scrip copy the following line
# without the ''' in the FreeCADCmd Python console
'''
importlib.reload(columngrid)

'''


# ***************************************************************************
# lets start with a simple columns grid


# geometry input data, all units in mm
h = 6000.0  # hoehe
w1 = 400.0  # breite 1
w2 = 600.0  # breite 2
ax = 4000   # abstand x
ay = 6000   # abstand y
nx = 16     # anzahl x
ny = 10     # anzahl y


# some modul imports
import os
import FreeCAD
import Arch
import Draft
import importIFC


# get doc name and export name
doc_name = os.path.splitext(os.path.basename(str(__file__)))[0]
export_file = str(__file__).rstrip('.py')


# create a new document, to have something to put the objects in
doc_obj = FreeCAD.newDocument(doc_name)


# list to save the objects which will be exported to ifc
obj_ifc = []


# add some columns to the document
for ix in range(nx):
    for iy in range(ny):
        col = Arch.makeStructure(length=w1, width=w2, height=h)
        col.Placement.Base = FreeCAD.Vector(ix * ax, iy * ay, 0.0)
        obj_ifc.append(col)


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
