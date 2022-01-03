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


class BaseBloodVessel(ABC):
    """Parent class for the root and daughter blood vessels. """

    GAMMA = 3   # Required for Murray's Law

    def __init__(self, distal_point):
        self._d = distal_point
        self._c = []

    def __eq__(self, other):
        """Two subtrees are considered 'equal' if they correspond to the same points in space. """
        return self.radius == other.radius and \
            self.distal_point == other.distal_point and \
            all(c_self == c_other for c_self, c_other in zip(self.children, other.children))    \

    @property
    @abstractmethod
    def cost(self):
        """The cost of a subtree is the volume of blood that it needs to fill it. """

    @property
    @abstractmethod
    def radius(self):
        """The radius of the vasculature. """

    @property
    def distal_point(self):
        """The distal (outflow) point of the blood vessel. """
        return self._d

    @property
    def children(self):
        """A list of blood vessels that are fed by this one. """
        return self._c

    def create_child(self, radius, distal_point):
        """Create and :return a child of this vessel with a given radius and distal point. """
        child = BloodVessel(radius, self, distal_point)
        self.children.append(child)
        return child

    def add_child(self, child):
        """Add a direct descendant to this vessel. """
        # TODO: Enforce exactly two children.
        self._c.append(child)

    def remove_child(self, child):
        """Remove a child from the collection of children. """
        self._c.remove(child)

    @property
    @abstractmethod
    def num_terminals(self):
        """The number of terminals that can be reached from this vessel. """

    @property
    def resistance(self):
        """The resistance of the blood vessel according to ?????. """
        # TODO: Needs to be in BaseBloodVessel or BloodVessel?
        # TODO: Include actual calculation of resistance.
        return self._r ** -4

    @abstractmethod
    def rescale(self, scaling_factor):
        """Rescale this subtree according to a scaling factor. """

    @abstractmethod
    def copy_subtree(self):
        """:returns a new vessel that is a copy of this one, and whose descendants are all copies. """

    @property
    @abstractmethod
    def descendants(self):
        """:returns all descendants of this blood vessel. """

    #def update_children(self, new_parent):
    #    """Change the parent of this vessel's children. """
    #    # TODO: Move somewhere else?
    #    for c in self.children:
    #        c.parent = new_parent
    #        new_parent.add_child(c)

    #@distal_point.setter
    #def distal_point(self, new):
    #    self._d = new

    #@property
    #def kappa(self):
    #    # TODO: Old Version
    #    return (self.radius / (self.radius - 5.5e-4)) ** 2

    #@property
    #def resistance(self):
    #    # TODO: Old Version
    #    n = self.viscosity
    #    L = self.length
    #    r = self.radius
    #    return (8 * n * L) / (pi * r**4)

    #@property
    #def satisfies_murray_law(self):
    #    # TODO: Old Version
    #    # TODO: Implement
    #    return True

    #def satisfies_radius_ratio(self, other):
    #    # TODO: Old Version
    #    # TODO: Not used
    #    return min(self.radius, other.radius) / max(self.radius, other.radius) > BloodVessel.DELTA

    #@property
    #def satisfies_aspect_ratio(self):
    #    # TODO: Old Version
    #    return self.line_seg.length / self.radius > 2

    #def nearest_point_to(self, p: Vec2D) -> Vec2D:
    #    # TODO: Old Version
    #    """The closest point to p on the blood vessel. """
    #    # TODO: Remove, or move to LineSegment
    #    a = self.proximal_point
    #    b = self.distal_point
    #    a_to_p = Vec2D(p.x - a.x, p.y - a.y)
    #    a_to_b = Vec2D(b.x - a.x, b.y - a.y)
    #
    #    atb2 = a_to_b.x ** 2 + a_to_b.y ** 2
    #
    #    atp_dot_atb = a_to_p.x * a_to_b.x + a_to_p.y * a_to_b.y
    #
    #    t = atp_dot_atb / atb2
    #
    #    return Vec2D(a.x + a_to_b.x * t,
    #                 a.y + a_to_b.y * t)

    #@staticmethod
    #def perp(a):
    #    return a * np.array([[0, 1],
    #                         [-1, 0]])

    #def blocked_by(self, other: BloodVessel, p: Vec2D) -> bool:
    #    # TODO: Old Version
    #    """p is blocked by other if the paths from p to the proximal and distal points intersect other.
    #     or if the proximal and distal points """
    #
    #    # First check that the other line segment doesn't block the proximal and distal points.
    #    that_seg = LineSegment(other.proximal_point, other.distal_point)
    #    this_seg_proximal = LineSegment(p, self.proximal_point)
    #    this_seg_distal = LineSegment(p, self.distal_point)
    #
    #    if that_seg.intersects_with(this_seg_proximal):
    #        return True
    #    if that_seg.intersects_with(this_seg_distal):
    #        return True

    #    # For the endpoints of other, we need to check the entire line, not just the line segment.
    #    # But we also need to be sure that other is in front of this.
    #    # To do this, check that the scalars are greater than 1.


class Origin(BaseBloodVessel):

    def __init__(self, radius, distal_point) -> None:
        self._r = radius
        super().__init__(distal_point)

    @property
    def radius(self):
        return self._r

    @property
    def root(self):
        return self._c[0]

    def copy_subtree(self):
        v = Origin(self.radius, self.distal_point)
        for c in self.children:
            new_c = c.copy_subtree()
            new_c.parent = v
            v.add_child(new_c)
        return v

    @property
    def num_terminals(self):
        return self.root.num_terminals

    @property
    def descendants(self):
        # Don't include the origin itself in the list of descendants.
        return self.root.descendants

    def rescale(self, scaling_factor):
        self._r *= scaling_factor

    @property
    def cost(self):
        return self.root._cost_from_radius(self.radius)


class BloodVessel(BaseBloodVessel):

    def __init__(self, scale, parent, distal_point):
        super().__init__(distal_point)
        self._p = parent
        self._s = scale

    @property
    def radius(self):
        return self.parent.radius * self._s

    @property
    def proximal_point(self):
        return self._p.distal_point

    @property
    def parent(self):
        return self._p

    @parent.setter
    def parent(self, p):
        self._p = p

    @property
    def descendants(self):
        yield self
        for c in self.children:
            for d in c.descendants:
                yield d

    @property
    def length(self):
        """The length of the blood vessel. """
        # TODO: Remove references to this.
        return self.line_seg.length

    def copy_subtree(self):
        v = BloodVessel(self._s, self.parent, self.distal_point)
        for c in self.children:
            new_c = c.copy_subtree()
            new_c.parent = v
            v.add_child(new_c)
        return v

    @property
    def num_terminals(self):
        # TODO: Make this a variable that can be looked up.
        return sum(v.num_terminals for v in self._c) if len(self._c) > 0 else 1

    def bifurcate(self, terminal_point, bifurcation_point=None):
        """Attach a new terminal to the tree by creating a bifurcation point on this blood vessel. """
        # Get local copies of the variables that we need. (Improves readability in equations)
        xp = self.proximal_point
        xd = self.distal_point
        g = BloodVessel.GAMMA
        nt = self.num_terminals
        s = self._s
        if bifurcation_point is None:
            bifurcation_point = (xp + xd) * 0.5
        # Calculate the radii of the new and existing vessels. TODO: Better estimate for resistance
        s_branch = (1 + nt ** (-g / 4)) ** (-1 / g)
        s_terminal = (1 + nt ** (g / 4)) ** (-1 / g)
        assert abs(1.0 - s_branch ** g - s_terminal ** g) < 1e-12  # I.e. satisfies Murray's Law
        assert abs(s_terminal ** -4 - s_branch ** -4 * nt) < 1e-12  # I.e. satisfies resistances
        # Finally, connect all the vessels together and re-scale.
        self.parent.remove_child(self)
        new_parent = self.parent.create_child(s, bifurcation_point)
        # This vessel is always the 0th child.
        self.parent = new_parent
        new_parent.add_child(self)
        new_parent.create_child(s_terminal, terminal_point)
        # The new vessel is always the 1st child.
        self.rescale(s_branch)

    def remove_bifurcation(self):
        """Remove the bifurcation point that is at the root of this vessel. """
        parent = self.parent
        new_s = parent._s
        assert isinstance(parent, BloodVessel)
        new_parent = parent.parent
        new_parent.remove_child(parent)
        new_parent.add_child(self)
        self.parent = new_parent
        self.rescale(new_s)

    def rescale(self, scaling_factor):
        self._s = scaling_factor

    @property
    def line_seg(self):
        return LineSegment(self.proximal_point, self.distal_point)

    @property
    def cost(self):
        return self._cost_from_radius(self.radius)

    def _cost_from_radius(self, radius):
        # For if we already know the radius (to avoid recomputing)
        r = radius * self._s
        xp, yp = self.proximal_point
        xd, yd = self.distal_point
        length = sqrt((xp - xd) ** 2 + (yp - yd) ** 2)
        return pi * r**2 * length + sum(c._cost_from_radius(r) for c in self._c)

#class VesselGroup:
#        # TODO: Old Version
#    """A wrapper for collections of blood vessels so that their total cost can be found easily."""
#
#    def __init__(self, vessels) -> None:
#        # TODO: Old Version
#        self.vessels = vessels
#
#    @property
#    def cost(self):
#        # TODO: Old Version
#        return sum(v.cost for v in self.vessels)
#
#    @property
#    def satisfies_aspect_ratio(self):
#        # TODO: Old Version
#        return all(v.satisfies_aspect_ratio for v in self.vessels)
#
#    @property
#    def satisfies_geometrical_constraints(self):
#        # TODO: Old Version
#        return self.satisfies_aspect_ratio
