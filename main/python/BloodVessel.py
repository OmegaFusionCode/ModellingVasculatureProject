from __future__ import annotations

from abc import ABC, abstractmethod
from math import sqrt, pi, exp

from LinAlg import LineSegment, Vec2D


def test_for_length_zero(group):
        # TODO: Old Version
    for v in group.vessels:
        if v.length < 1e-15:
            return True
    return False


class BloodVessel(ABC):

    """Parent class for the root and daughter blood vessels. """

    GAMMA = 3   # Required for Murray's Law

    def __init__(self, radius, distal_point):
        self.__r = radius
        self.__d = distal_point
        self.__children = []

    def __eq__(self, other):
        # TODO: Old Version. This may not be good to keep.
        return self.radius == other.radius and \
               self.proximal_point == other.proximal_point and \
               self.distal_point == other.distal_point

    @property
    def radius(self):
        """The radius of the vasculature. """
        return self.__r

    @property
    def kappa(self):
        # TODO: Old Version
        return (self.radius / (self.radius - 5.5e-4)) ** 2

    @property
    def resistance(self):
        # TODO: Old Version
        n = self.viscosity
        L = self.length
        r = self.radius
        return (8 * n * L) / (pi * r**4)

    @property
    def satisfies_murray_law(self):
        # TODO: Old Version
        # TODO: Implement
        return True

    def satisfies_radius_ratio(self, other):
        # TODO: Old Version
        # TODO: Not used
        return min(self.radius, other.radius) / max(self.radius, other.radius) > BloodVessel.DELTA

    @property
    def satisfies_aspect_ratio(self):
        # TODO: Old Version
        return self.line_seg.length / self.radius > 2

    def nearest_point_to(self, p: Vec2D) -> Vec2D:
        # TODO: Old Version
        """The closest point to p on the blood vessel. """
        # TODO: Remove, or move to LineSegment
        a = self.proximal_point
        b = self.distal_point
        a_to_p = Vec2D(p.x - a.x, p.y - a.y)
        a_to_b = Vec2D(b.x - a.x, b.y - a.y)

        atb2 = a_to_b.x ** 2 + a_to_b.y ** 2

        atp_dot_atb = a_to_p.x * a_to_b.x + a_to_p.y * a_to_b.y

        t = atp_dot_atb / atb2

        return Vec2D(a.x + a_to_b.x * t,
                     a.y + a_to_b.y * t)

    #@staticmethod
    #def perp(a):
    #    return a * np.array([[0, 1],
    #                         [-1, 0]])

    def blocked_by(self, other: BloodVessel, p: Vec2D) -> bool:
        # TODO: Old Version
        """p is blocked by other if the paths from p to the proximal and distal points intersect other.
         or if the proximal and distal points """

        # First check that the other line segment doesn't block the proximal and distal points.
        that_seg = LineSegment(other.proximal_point, other.distal_point)
        this_seg_proximal = LineSegment(p, self.proximal_point)
        this_seg_distal = LineSegment(p, self.distal_point)

        if that_seg.intersects_with(this_seg_proximal):
            return True
        if that_seg.intersects_with(this_seg_distal):
            return True

        # For the endpoints of other, we need to check the entire line, not just the line segment.
        # But we also need to be sure that other is in front of this.
        # To do this, check that the scalars are greater than 1.

    @property
    def length(self):
        # TODO: Remove references to this.
        return self.line_seg.length

    @property
    @abstractmethod
    def proximal_point(self):
        """The proximal (inflow) point of the blood vessel. """
        pass

    @property
    def distal_point(self):
        """The distal (outflow) point of the blood vessel. """
        return self.__d

    def add_child(self, child):
        """Add a direct descendant to this vessel. """
        # TODO: Enforce exactly two children.
        self.__children.append(child)

    @property
    def num_terminals(self):
        """The number of terminals that can be reached from this vessel. """
        return sum(v.num_terminals for v in self.__children) if len(self.__children) > 0 else 1

    @property
    def line_seg(self):
        """:returns a line segment that represents this blood vessel in 2D space. """
        return LineSegment(self.proximal_point, self.distal_point)

    @property
    def cost(self):
        """The cost of a blood vessel is the volume of blood that it can hold. """
        r = self.__r
        xp, yp = self.proximal_point
        xd, yd = self.distal_point
        L = sqrt((xp - xd) ** 2 + (yp - yd) ** 2)
        return pi * r**2 * L

    @property
    @abstractmethod
    def parent(self):
        pass

    @property
    def children(self):
        return self.__children

    def update_children(self, new_parent):
        for c in self.children:
            c.parent = new_parent
            new_parent.add_child(c)


class RootBloodVessel(BloodVessel):

    def __init__(self, radius, proximal_point, distal_point) -> None:
        super().__init__(radius, distal_point)
        self.__p = proximal_point

    @property
    def proximal_point(self):
        return self.__p

    @property
    def parent(self):
        return None


class ChildBloodVessel(BloodVessel):

    def __init__(self, radius, parent, distal_point):
        super().__init__(radius, distal_point)
        self.__parent = parent
        parent.add_child(self)

    @property
    def proximal_point(self):
        return self.__parent.distal_point

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, p):
        self.__parent = p


class VesselGroup:
        # TODO: Old Version
    """A wrapper for collections of blood vessels so that their total cost can be found easily."""

    def __init__(self, vessels) -> None:
        # TODO: Old Version
        self.vessels = vessels

    @property
    def cost(self):
        # TODO: Old Version
        return sum(v.cost for v in self.vessels)

    @property
    def satisfies_aspect_ratio(self):
        # TODO: Old Version
        return all(v.satisfies_aspect_ratio for v in self.vessels)

    @property
    def satisfies_geometrical_constraints(self):
        # TODO: Old Version
        return self.satisfies_aspect_ratio
