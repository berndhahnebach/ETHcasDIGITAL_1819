import Arch
from FreeCAD import Vector as vec

App.newDocument()

terrasse_win_place = FreeCAD.Placement(
    vec(0, 0, 0),
    FreeCAD.Rotation(vec(1, 0, 0), 90)
)
terrasse_win_obj = Arch.makeWindowPreset(
    "Fixed",
    width=1000,
    height=1000,
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

App.ActiveDocument.recompute()
App.closeDocument(App.ActiveDocument.Name)
