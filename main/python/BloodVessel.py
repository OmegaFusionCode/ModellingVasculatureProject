from __future__ import annotations
from math import sqrt, pi, exp

from LinAlg import LineSegment, Vec2D


def test_for_length_zero(group):
    for v in group.vessels:
        if v.length < 1e-15:
            return True
    return False


class BloodVessel:
    GAMMA = 3
    DELTA = None

    def __init__(self, radius, proximal_point, distal_point) -> None:
        self.radius = radius
        self.proximal_point = proximal_point
        self.distal_point = distal_point

    def __eq__(self, other):
        return self.radius == other.radius and \
               self.proximal_point == other.proximal_point and \
               self.distal_point == other.distal_point

    @property
    def length(self):
        """The length of the blood vessel. """
        return abs(self.distal_point - self.proximal_point)

    @property
    def cost(self):
        """The cost of the blood vessel is its volume. """
        r = self.radius
        xp, yp = self.proximal_point
        xd, yd = self.distal_point
        length = sqrt((xp - xd) ** 2 + (yp - yd) ** 2)
        return pi * r**2 * length

    @property
    def line_seg(self):
        """The line segment that represents the position of the blood vessel. """
        return LineSegment(self.proximal_point, self.distal_point)

    @property
    def kappa(self):
        return (self.radius / (self.radius - 5.5e-4)) ** 2

    @property
    def viscosity(self):
        """Compute the fluid viscosity in the vessel accounting for the Fàhræus-Lindqvist effect. """
        k = self.kappa
        r = self.radius
        return 1.125 * (k + k**2 * (6 * exp(-170 * r) - 2.44 * exp(-8.09 * r**0.64) + 2.2))

    @property
    def resistance(self):
        n = self.viscosity
        L = self.length
        r = self.radius
        return (8 * n * L) / (pi * r**4)

    @property
    def satisfies_murray_law(self):
        # TODO: Implement
        return True

    @property
    def satisfies_radius_ratio(self, other):
        # TODO: Not used
        return min(self.radius, other.radius) / max(self.radius, other.radius) > BloodVessel.DELTA

    @property
    def satisfies_aspect_ratio(self):
        return self.line_seg.length / self.radius > 2

    def nearest_point_to(self, p: Vec2D) -> Vec2D:
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


class VesselGroup:
    """A wrapper for collections of blood vessels so that their total cost can be found easily."""

    def __init__(self, vessels) -> None:
        self.vessels = vessels

    @property
    def cost(self):
        return sum(v.cost for v in self.vessels)

    @property
    def satisfies_aspect_ratio(self):
        return all(v.satisfies_aspect_ratio for v in self.vessels)

    @property
    def satisfies_geometrical_constraints(self):
        return self.satisfies_aspect_ratio
