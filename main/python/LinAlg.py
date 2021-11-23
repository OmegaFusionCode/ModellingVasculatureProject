from __future__ import annotations
import math

import numpy as np


class LineSegment:
    """The line segment bounded by the endpoints a and b."""

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.eqn = Line(a, (b - a))

    @property
    def length(self):
        """The length of the line segment."""
        a = self.a
        b = self.b
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    @property
    def vector(self):
        """The vector of the path from a to b."""
        a = self.a
        b = self.b
        return Vec2D(b.x - a.x, b.y - a.y)

    def distance_to(self, p: Vec2D):
        #A = p.x - self.a.x
        #B = p.y - self.a.y
        #C = self.b.x - self.a.x
        #D = self.b.y - self.a.y
        #dot = A*C + B*D

        ab = self.vector.arr
        ap = p.arr - self.a.arr

        dot = np.dot(ab, ap)
        len_sq = self.length ** 2
        param = dot/len_sq if len_sq != 0 else -1

        if param < 0:
            #xx = self.a.x
            #yy = self.a.y
            res = self.a.arr
        elif param > 1:
            #xx = self.b.x
            #yy = self.b.y
            res = self.a.arr
        else:
            #xx = self.a.x + param*
            res = self.a.arr + param*ap
        return np.linalg.norm(p.arr - res)

    @staticmethod
    def on_segment(p, q, r):
        """Test if q lies in the bounding box of the line segment pr"""
        # TODO: Make this a non-static method.
        if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
                (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True
        return False

    @staticmethod
    def orientation(p, q, r):
        """Determine the relationship between p, q and r.
        :returns 0 if p, q and r are collinear.
        :returns 1 if p, q and r are clockwise.
        :returns -1 if p, q and r are anticlockwise.
        """
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if val > 0:
            return 1
        elif val < 0:
            return -1
        else:
            return 0

    def intersects_with(self, other: LineSegment):
        """Test if this intersects with other."""
        p1 = self.a
        q1 = self.b
        p2 = other.a
        q2 = other.b

        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True
        elif o1 == 0 and self.on_segment(p1, p2, q1):
            return True
        elif o2 == 0 and self.on_segment(p1, q2, q1):
            return True
        elif o3 == 0 and self.on_segment(p2, p1, q2):
            return True
        elif o4 == 0 and self.on_segment(p2, q1, q2):
            return True
        else:
            return False


class Vec2D:
    """Wrapper for 2D Numpy arrays."""

    @staticmethod
    def from_array(array) -> Vec2D:
        """Alternative constructor to build from an existing Numpy array."""
        return Vec2D(array[0], array[1])

    def __init__(self, x, y) -> None:
        self.arr = np.array([x, y])

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return (self.arr == other.arr).all()

    def __abs__(self):
        return np.linalg.norm(self.arr)

    def __hash__(self):
        # Numpy arrays are mutable and therefore not hashable, so we hash the tuple of it instead.
        # This now means we must be careful not to mutate the array.
        # TODO: Fix this problem or figure out that hashing these values is not something we need to do.
        return hash(tuple(self.arr))

    @property
    def x(self):
        """The x value of this vector."""
        return self.arr[0]

    @property
    def y(self):
        """The y value of this vector."""
        return self.arr[1]

    def __add__(self, other):
        return Vec2D.from_array(self.arr + other.arr)

    def __sub__(self, other):
        return Vec2D.from_array(self.arr - other.arr)

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vec2D(x, y)



# TODO: Improve the tolerance.
def parallel(a, b, tolerance=3e-10) -> bool:
    """Test if a and b are parallel vectors.
    :returns True if a and b are parallel, False otherwise.
    """
    dot = abs(np.dot(a.arr, b.arr))
    lengths = abs(a) * abs(b)
    return dot - lengths < tolerance


class Line:
    """Lines expressed as a position vector and a direction vector."""

    def __init__(self, start, direction):
        self.p = start
        self.d = direction

    def is_point_on_line(self, p) -> bool:
        """Tests if p is on the line.
        :returns True if p is on the line, False otherwise.
        """
        new_p = p - self.p
        return parallel(new_p, self.d)

    def find_scalars_at_intersection(self, other):
        """Find the values that we have to multiply the direction vectors of this and other by to find the point of
        intersection in the line equation.
        :returns an array containing the two scalars, or None if the lines are parallel.
        """
        new_p = other.p - self.p
        m = np.array((self.d, -other.d)).transpose()
        # new_p = m*ans
        try:
            # TODO: Make this work for 3D.
            return np.linalg.solve(m, new_p)
            # Find the intersection point, then check that it
        except np.linalg.LinAlgError:  # The inverse of m does not exist.
            return None

    def find_point_of_intersection(self, line):
        """Find the point at which this and other intersect.
        :returns the point of intersection, or None if the lines are parallel.
        """
        s = self.find_scalars_at_intersection(line)
        if s is None:
            return None
        assert ((p := self.p + s[0] * self.d) == line.p + s[1] * line.d)
        return p


def main():
    p1 = Vec2D(1, 1)
    q1 = Vec2D(10, 1)
    s1 = LineSegment(p1, q1)
    p2 = Vec2D(1, 2)
    q2 = Vec2D(10, 2)
    s2 = LineSegment(p2, q2)

    if s1.intersects_with(s2):
        assert (s2.intersects_with(s1))
        print("Yes")
    else:
        assert (not s2.intersects_with(s1))
        print("No")

    p1 = Vec2D(10, 0)
    q1 = Vec2D(0, 10)
    s1 = LineSegment(p1, q1)
    p2 = Vec2D(0, 0)
    q2 = Vec2D(10, 10)
    s2 = LineSegment(p2, q2)

    if s1.intersects_with(s2):
        assert (s2.intersects_with(s1))
        print("Yes")
    else:
        assert (not s2.intersects_with(s1))
        print("No")

    p1 = Vec2D(-5, -5)
    q1 = Vec2D(0, 0)
    s1 = LineSegment(p1, q1)
    p2 = Vec2D(1, 1)
    q2 = Vec2D(10, 10)
    s2 = LineSegment(p2, q2)

    if s1.intersects_with(s2):
        assert (s2.intersects_with(s1))
        print("Yes")
    else:
        assert (not s2.intersects_with(s1))
        print("No")


if __name__ == '__main__':
    main()
