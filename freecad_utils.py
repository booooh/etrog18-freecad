import FreeCAD
import Draft
import Arch
from FreeCAD import Vector, Placement, Rotation


class Segments:
    def __init__(self, origin=None):
        self.origin = origin if origin else Vector(0, 0, 0)
        self.points = [self.origin]

    def add_segment(self, point):
        last_point = self.points[-1]

        # add segment relative to the last point
        new_point = last_point + point
        print("adding point", new_point)
        self.points.append(new_point)
        return self

    def make_wire(self, **kwargs):
        wire = Draft.make_wire(self.points, **kwargs)
        FreeCAD.ActiveDocument.recompute()
        return wire

    def add_segments(self, points):
        for p in points:
            self.add_segment(p)


def X(length):
    return Vector(length, 0, 0)


def Y(length):
    return Vector(0, length, 0)


def draw_outer_walls_explict_space(placement=None, **kwargs):
    """
    Used to draw the outer walls, based on the floor plan found in:


    import importlib; import freecad_utils; importlib.reload(freecad_utils) ; freecad_utils.draw_outer_walls(placement=FreeCAD.Placement(FreeCAD.Vector(-8000,-1500,0),FreeCAD.Rotation()))
    """
    if placement is None:
        placement = Placement()

    if "face" not in kwargs:
        kwargs["face"] = False

    s = Segments(placement.Base)
    relative_coordinates = [
        Y(200),
        Y(4000),
        Y(200),
        Y(4000),
        X(3100),
        Y(1400),
        X(1300),
        Y(-300),
        X(3000),
        Y(300),
        X(1200),
        Y(-900),
        X(2600),
        Y(-200),
        Y(-4000),
        Y(-200),
        Y(-900),
        Y(-100),
        Y(-1800),
        Y(-200),
        Y(-1300),
        X(2300),
        X(200),
        Y(-200),
        Y(-3400),
        Y(-200),
        X(-200),
        X(-6500),
        X(-200),
        Y(200),
        Y(3400),
        X(-1200),
        X(-200),
        X(-5200),
        X(-200),
    ]
    s.add_segments(relative_coordinates)
    wire1 = s.make_wire(**kwargs)
    walls = Arch.makeWall(wire1)
    FreeCAD.ActiveDocument.recompute()
    return walls


def draw_house(placement=None, **kwargs):
    # import importlib; import freecad_utils; importlib.reload(freecad_utils) ; freecad_utils.draw_house()

    draw_outer_walls(placement, **kwargs)
    draw_internal_walls(placement, **kwargs)


def draw_outer_walls(placement=None, **kwargs):
    """
    Used to draw the outer walls, based on the floor plan found in:


    import importlib; import freecad_utils; importlib.reload(freecad_utils) ; freecad_utils.draw_outer_walls(placement=FreeCAD.Placement(FreeCAD.Vector(-8000,-1500,0),FreeCAD.Rotation()))
    """
    if placement is None:
        placement = Placement()

    if "face" not in kwargs:
        kwargs["face"] = False

    s = Segments(placement.Base)
    relative_coordinates = [
        Y(4200),
        Y(4200),
        X(3050),
        Y(1400),
        X(1150),
        Y(-300),
        X(3200),
        Y(300),
        X(1000),
        Y(-900),
        X(2600),
        Y(-4150),
        Y(-1000),
        Y(-1950),
        # bathroom/hallway
        Y(-1800),
        X(2500),
        Y(-3600),
        # south-east corner
        X(-6700),
        Y(3600),
        # rear enterance
        X(-1400),
        X(-5400),
    ]
    s.add_segments(relative_coordinates)
    wire1 = s.make_wire(**kwargs)
    walls = Arch.makeWall(wire1)
    FreeCAD.ActiveDocument.recompute()

    return walls


def draw_internal_walls(placement=None, **kwargs):

    if placement is None:
        placement = Placement()

    if "face" not in kwargs:
        kwargs["face"] = False

    entrance_hallway_wall = Segments(placement.Base + Vector(3050, 8400, 0))
    entrance_hallway_wall.add_segment(X(1300))
    w1 = Arch.makeWall(entrance_hallway_wall.make_wire(**kwargs))

    # separation between living room and kids' room
    kids_room = Segments(placement.Base + Vector(0, 4200, 0))
    kids_room.add_segments(
        [
            X(4300),
            Y(500),
            X(1100),
            Y(-4700),
        ]
    )

    w2 = Arch.makeWall(kids_room.make_wire(**kwargs))

    # kitchen
    kitchen = Segments(placement.Base + Vector(7400, 9500, 0))
    kitchen.add_segment(Y(-4750))
    kitchen.add_segment(X(3600))
    w3 = Arch.makeWall(kitchen.make_wire(**kwargs))

    # TODO: add bathrooms

    # TODO: split master bedroom

    # TODO: add doors

    # TODO: add windows

    FreeCAD.ActiveDocument.recompute()


def draw_outer_walls_2_parts(placement=None, **kwargs):
    """
    Used to draw the outer walls, based on the floor plan found in:


    import importlib; import freecad_utils; importlib.reload(freecad_utils) ; freecad_utils.draw_outer_walls(placement=FreeCAD.Placement(FreeCAD.Vector(-8000,-1500,0),FreeCAD.Rotation()))
    """
    if placement is None:
        placement = Placement()

    if "face" not in kwargs:
        kwargs["face"] = False

    s = Segments(placement.Base)
    relative_coordinates = [
        Y(200),
        Y(4000),
        Y(200),
        Y(4000),
        X(3100),
        Y(1400),
        X(1300),
        Y(-300),
        X(3000),
        Y(300),
        X(1200),
        Y(-900),
        X(2600),
        Y(-200),
        Y(-4000),
        Y(-200),
        Y(-900),
        Y(-100),
        Y(-1800),
        Y(-200),
        X(-200),
        X(-2600),
        X(-100),
        X(-2700),
        Y(-1300),
        Y(-200),
        X(-200),
        X(-5200),
        X(-200),
    ]
    s.add_segments(relative_coordinates)
    wire1 = s.make_wire(**kwargs)

    # make the addition
    s2 = Segments(placement.Base + Vector(6800, 200, 0))
    s2_relative_coordinates = [
        X(200),
        X(6500),
        X(200),
        Y(-200),
        Y(-3400),
        Y(-200),
        X(-200),
        X(-6500),
        X(-200),
        Y(200),
        Y(3400),
        Y(200),
    ]
    s2.add_segments(s2_relative_coordinates)
    wire2 = s2.make_wire(**kwargs)

    # connect the two sections (door heading to backyard, door to service area)
    backyard_door = Segments(placement.Base + Vector(5600, 0, 0))
    backyard_door.add_segment(X(1200))
    backyard_wire = backyard_door.make_wire(**kwargs)

    service_door = Segments(placement.Base + Vector(11200, 200, 0))
    service_door.add_segment(Y(1300))
    service_wire = service_door.make_wire(**kwargs)

    return [wire1, wire2, backyard_wire, service_wire]
