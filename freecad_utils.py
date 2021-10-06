import FreeCAD
import Draft
import Arch
from FreeCAD import Vector, Placement, Rotation


class Segments:
    def __init__(self, origin=None):
        self.origin = origin if origin else Vector(0, 0, 0)
        self.points = [self.origin]
        self.named_points = {}
        self.wire = None

    def add_segment(self, point):
        last_point = self.points[-1]

        name = None
        if not isinstance(point, Vector):
            name = point[1]
            point = point[0]

        # add segment relative to the last point
        new_point = last_point + point
        print("adding point", new_point)
        self.points.append(new_point)

        if name:
            self.named_points[name] = new_point

        return self

    def make_wire(self, **kwargs):
        self.wire = Draft.make_wire(self.points, **kwargs)
        FreeCAD.ActiveDocument.recompute()
        return self.wire

    def make_wall(self):
        return Arch.makeWall(self.wire)

    def add_segments(self, points):
        for p in points:
            self.add_segment(p)


def X(length):
    return Vector(length, 0, 0)


def Y(length):
    return Vector(0, length, 0)


def draw_house(placement=None, make_walls=True, **kwargs):
    # import importlib; import freecad_utils; importlib.reload(freecad_utils) ; freecad_utils.draw_house()

    # outer_segments = draw_outer_walls(placement, **kwargs)
    outer_segments = draw_outer_walls_raphela(placement, **kwargs)
    # inner_segments = draw_internal_walls(outer_segments, placement, **kwargs)
    inner_segments = draw_inner_walls_raphela(outer_segments, placement, **kwargs)

    if make_walls:
        outer_segments.make_wall()
        for s in inner_segments:
            s.make_wall()
    FreeCAD.ActiveDocument.recompute()


def draw_outer_walls_raphela(placement=None, **kwargs):
    if placement is None:
        placement = Placement()

    if "face" not in kwargs:
        kwargs["face"] = False

    s = Segments(placement.Base)
    relative_coordinates = [
        Y(1550),
        X(2650),
        (Y(4200), "diningroom/livingroom"),
        Y(4210),
        X(-5410),
        (X(-1400), "children/hallway"),
        Y(3950),
        (X(-3200), "children/parents"),
        X(-4000),
        Y(-3950),
        X(2900),
        # total length of eastern wall should be 8900 mm
        (Y(-1150), "balcony/parent-bath"),
        (Y(-1030), "bathroom/bathroom"),
        (Y(-2570), "bath/work"),
        Y(-4200),
        (X(3650), "study/kitchen"),
        Y(-580),
        (X(3350), "kitchen/hall"),
        # Y(-460),  # before shifting this down by a bit, just to close the wire
        Y(-430),  # after shifting this down by a bit, just to close the wire
        # X(1500),  # before shifting this left a bit, just to close the wire
        X(1460),  # after shifting this left a bit, just to close the wire
    ]

    s.add_segments(relative_coordinates)
    s.make_wire(**kwargs)

    return s


def draw_inner_walls_raphela(outer_walls, placement=None, **kwargs):
    if placement is None:
        placement = Placement()

    if "face" not in kwargs:
        kwargs["face"] = False

    # bathrooms
    bathrooms = Segments(outer_walls.named_points["balcony/parent-bath"])
    bathrooms.add_segments(
        [
            (X(2230), "bathroom/suite-door"),
            (X(1550), "bathroom/service-cabinet"),
            Y(-2000),
            (X(-1550), "bathroom/bathroom-door"),
            Y(-1600),
            X(-2230),
        ]
    )

    bathrooms.make_wire(**kwargs)

    bathrooms_inner = Segments(outer_walls.named_points["bathroom/bathroom"])
    # need to make an L shape between two known points
    midpoint = Vector(
        bathrooms.named_points["bathroom/bathroom-door"].x,
        outer_walls.named_points["bathroom/bathroom"].y,
        0,
    )

    bathrooms_inner.points.append(midpoint)
    print("appended ", midpoint)
    print("appended ", bathrooms.named_points["bathroom/bathroom-door"])
    bathrooms_inner.points.append(bathrooms.named_points["bathroom/bathroom-door"])
    bathrooms_inner.make_wire()

    study_wall = Segments(outer_walls.named_points["study/kitchen"])

    study_wall.add_segment(Y(4650))
    study_wall.add_segment(X(750))
    study_wall.make_wire()

    hall_wall = Segments(outer_walls.named_points["kitchen/hall"])
    hall_wall.add_segment(Y(1150))
    hall_wall.add_segment(X(400))
    hall_wall.make_wire()

    # fridge area start 1250 mm to the right, 700 mm below
    fridge = Segments(study_wall.points[-1] + Vector(1250, -700, 0))
    fridge.add_segment(Y(900))
    fridge.add_segment(X(1290))
    fridge.add_segment(Y(-900))
    fridge.make_wire()

    tv_wall = Segments(fridge.points[1] + Vector(0, 1250, 0))
    tv_wall.add_segment(Y(1350))
    tv_wall.make_wire()

    bedrooms = Segments(outer_walls.named_points["children/hallway"])
    bedrooms.add_segment((X(-3200), "bedroom/bedroom"))
    bedrooms.add_segment(Y(3950))
    bedrooms.make_wire()

    bedroom_door = Segments(bedrooms.named_points["bedroom/bedroom"])
    bedroom_door.add_segment(X(-1100))
    bedroom_door.make_wire()

    FreeCAD.ActiveDocument.recompute()
    return (
        bathrooms,
        bathrooms_inner,
        study_wall,
        hall_wall,
        fridge,
        tv_wall,
        bedrooms,
        bedroom_door,
    )


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
        (X(3200), "livingroom/kitchen"),
        Y(300),
        X(1000),
        Y(-900),
        X(2600),
        Y(-4150),
        Y(-1000),
        (Y(-1950), "bathroom/hallway"),
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
    s.make_wire(**kwargs)

    return s


def draw_internal_walls(outer_walls, placement=None, **kwargs):

    if placement is None:
        placement = Placement()

    if "face" not in kwargs:
        kwargs["face"] = False

    entrance_hallway_wall = Segments(placement.Base + Vector(3050, 8400, 0))
    entrance_hallway_wall.add_segment(X(1300))
    entrance_hallway_wall.make_wire(**kwargs)

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
    kids_room.make_wire(**kwargs)

    # kitchen
    kitchen = Segments(outer_walls.named_points["livingroom/kitchen"])
    kitchen.add_segments(
        [
            Y(-4750),
            X(100),  # 10cm buldge
            (X(900), "kitchen-door"),  # 90cm doorway
            X(2600),
        ]
    )

    kitchen.make_wire(**kwargs)

    # cabinet, 85cm below doorway
    cabinet_end_y = kitchen.named_points["kitchen-door"].y - 850

    # TODO: add bathrooms
    bathrooms = Segments(outer_walls.named_points["bathroom/hallway"])
    bathrooms.add_segments([X(-3200), Y(2700)])
    bathrooms.make_wire(**kwargs)

    # TODO: split master bedroom

    # TODO: add doors

    # TODO: add windows

    FreeCAD.ActiveDocument.recompute()
    return (entrance_hallway_wall, kids_room, kitchen, bathrooms)
