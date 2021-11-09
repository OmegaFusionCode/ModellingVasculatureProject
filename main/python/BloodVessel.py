from __future__ import annotations
from math import sqrt, pi

import numpy as np

from LinAlg import LineSegment, Vec2D


class BloodVessel:

    def __init__(self, radius, proximal_point, distal_point) -> None:
        self.radius = radius
        self.proximal_point = proximal_point
        self.distal_point = distal_point

    @property
    def cost(self):
        r = self.radius
        xp, yp = self.proximal_point
        xd, yd = self.distal_point
        length = sqrt((xp - xd) ** 2 + (yp - yd) ** 2)
        return pi * r**2 * length

    def nearest_point_to(self, p: Vec2D) -> Vec2D:
        a = self.proximal_point
        b = self.distal_point
        a_to_p = Vec2D(p.x - a.x, p.y - a.y)
        a_to_b = Vec2D(b.x - a.x, b.y - a.y)

        atb2 = a_to_b.x ** 2 + a_to_b.y ** 2

        atp_dot_atb = a_to_p.x * a_to_b.x + a_to_p.y * a_to_b.y

        t = atp_dot_atb / atb2

        return Vec2D(a.x + a_to_b.x * t,
                     a.y + a_to_b.y * t)

    @staticmethod
    def perp(a):
        return a * np.array([[0, 1],
                             [-1, 0]])

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