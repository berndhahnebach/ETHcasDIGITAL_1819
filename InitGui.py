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


from os.path import join


# print(join(FreeCAD.ConfigGet("AppHomePath"), "Mod"))  # if module is in FreeCAD App path
# print(join(FreeCAD.ConfigGet("UserAppData"), "Mod"))  # if module is in FreeCAD users data path
moduledir = join(FreeCAD.ConfigGet("UserAppData"), "Mod", "ETHcasDIGITAL_1819")
FreeCADGui.addIconPath(join(moduledir, 'icons'))


class EthCasDigitalWorkbench(Workbench):

    MenuText = 'ETHcasDIGITAL'                                 
    ToolTip = 'ETHcasDIGITAL workbench'
    Icon = 'eth_casdigital_workbench.svg'

    def GetClassName(self):
        return 'Gui::PythonWorkbench'

    def Initialize(self):
        from ethcommands import commands

        tools = [
            'Columngrid',
            'Reihenhaus'
        ]

        FreeCADGui.addCommand(tools[0], commands.RunColumgrid())
        FreeCADGui.addCommand(tools[1], commands.RunReihenhaus())

        self.appendToolbar('ETHcasDIGITAL', tools)
        self.appendMenu('ETHcasDIGITAL', tools)


FreeCADGui.addWorkbench(EthCasDigitalWorkbench())
