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


import sys
from importlib import reload

import FreeCAD
import FreeCADGui


# since we have no def in columngrid code will be executed on import of columngrid
# https://stackoverflow.com/questions/30483246/how-to-check-if-a-python-module-has-been-imported


class RunColumgrid():
    def GetResources(self):
        return {'Pixmap': 'eth_run_columngrid.svg',
                'MenuText': 'run Columngrid',
                'ToolTip': 'run Columngrid'}

    def IsActive(self):
        # the tool is always active, we could omit this dev
        return True

    def Activated(self):
        modulename = 'columngrid'
        modulfullname = 'ethtools.columngrid'
        if modulename not in sys.modules and modulfullname not in sys.modules:
            FreeCAD.Console.PrintMessage('import {}\n'.format(modulename))
            from ethtools import columngrid
        else:
            FreeCAD.Console.PrintMessage('reload {}\n'.format(modulename))
            from ethtools import columngrid
            reload(columngrid)


class RunReihenhaus():
    def GetResources(self):
        return {'Pixmap': 'eth_run_reihenhaus.svg',
                'MenuText': 'run Reihenhaus',
                'ToolTip': 'run Reihenhaus'}

    def IsActive(self):
        # the tool is always active, we could omit this dev
        return True

    def Activated(self):
        modulename = 'reihenhaus'
        modulfullname = 'ethtools.reihenhaus'
        if modulename not in sys.modules and modulfullname not in sys.modules:
            FreeCAD.Console.PrintMessage('import {}\n'.format(modulename))
            from ethtools import reihenhaus
        else:
            FreeCAD.Console.PrintMessage('reload {}\n'.format(modulename))
            from ethtools import reihenhaus
            reload(reihenhaus)


class calculateRaumflaechen():
    def GetResources(self):
        return {'Pixmap': 'eth_calculate_raumflaechen.svg',
                'MenuText': 'calculate Raumflaechen',
                'ToolTip': 'calculate Raumflaechen'}

    def IsActive(self):
        # the tool is always active, we could omit this dev
        return True

    def Activated(self):
        from ethtools.raumflaechen import calculate_raumflaechen as calcrm
        calcrm()

