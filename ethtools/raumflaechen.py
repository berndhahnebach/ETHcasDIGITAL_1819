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



def calculate_raumflaechen():

    # TODO fix ifc export of faces, to be able to export result to ifc

    import os

    import Arch
    import Part
    import Draft
    import FreeCAD

    mydoc = FreeCAD.ActiveDocument

    # the ifc container
    raumflaechen_site = Arch.makeSite([], name="ETH-Reihenhaus")
    raumflaechen_build = Arch.makeBuilding([], name="Reihenhaus_Raumflaechen")
    Arch.addComponents(raumflaechen_build, raumflaechen_site)
    textgrp = mydoc.addObject("App::DocumentObjectGroup", "Texte")

    # save the raumflaechen area
    areas = []

    #
    for o in mydoc.Objects:
        if hasattr(o, "IfcType") and o.IfcType == 'Space':
            print('We found the Space object: {}'.format(o.Label))
            sh = o.Shape
            if sh.ShapeType == 'Solid':
                for face in o.Shape.Faces:
                    # print('\n')
                    nv = face.normalAt(50, 50)  # normalen vector
                    # print(nv)
                    # Seitenflaeche, z-koord des normalen vektors is null
                    # if -0.001 < f.normalAt(50, 50).z < 0.001:  
                    # Bottomflaeche, z-koord des normalen vektors is -1 und x und y sind null
                    
                    if -0.001 < nv.x < 0.001 and -0.001 < nv.y < 0.001 and -1.001 < nv.z < -0.999:
                        print('Found Bottomflaeche')
                        raumflaeche_partobj = mydoc.addObject(
                            "Part::Feature", "Flaeche"
                        )
                        raumflaeche_partobj.Shape = face
                        raumflaeche_obj = Arch.makeComponent(
                            baseobj=raumflaeche_partobj,
                            name="Raumflaeche_" + o.Label
                        )
                        raumflaeche_obj.ViewObject.ShapeColor = (0.33 , 0.67 , 1.0 , 0.0)
                        Arch.addComponents(raumflaeche_obj, raumflaechen_build)
                        rf_name = raumflaeche_obj.Label
                        rf_area = round(raumflaeche_obj.Shape.Area * 1E-6, 2)  # TODO use unit system
                        rftext_vec = face.CenterOfMass + FreeCAD.Vector(0, 0, 10)  # to be above face
                        rftext_vec = rftext_vec + FreeCAD.Vector(-1000, 0, 0)  # haaack
                        rftext_obj = Draft.makeText(str(rf_area) + ' m2', rftext_vec)
                        rftext_obj.ViewObject.FontSize = 1000
                        textgrp.addObject(rftext_obj)
                        areas.append((rf_name, rf_area))

    mydoc.recompute()
    # print(areas)

    export_file = os.path.join(os.path.expanduser('~'), 'Desktop', 'raumflaechen')
    write_areas2csv(areas, export_file)
    write_areas2yaml(areas, export_file)

    return True


def write_areas2csv(areas, csvfile):
    # write to csv
    csvfilename = csvfile + ".csv"
    f = open(csvfilename, "w")
    f.write('IfcSpace Name, Area in m2\n')
    for area in areas:
        f.write('{}, {}\n'.format(area[0], area[1]))
    f.close()


def write_areas2yaml(areas, yamlfile):
    # write to yaml
    import yaml
    ymlfilename = yamlfile + ".yml"
    f = open(ymlfilename, "w")
    f.write("# file created by FreeCAD\n")
    f.write('\n')
    f.write('# raumflaechen\n')
    import yaml
    f.write(yaml.dump(areas, default_flow_style=False))
    f.close()
