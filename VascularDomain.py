import abc
import random
from abc import ABC
from math import pi

from LinAlg import LineSegment, Vec2D


class VascularDomain(ABC):

    @property
    @abc.abstractmethod
    def area(self):
        """:returns the total area of the vascular domain. """

    @abc.abstractmethod
    def point_grid(self, intervals):
        """Generate a uniform grid of points within the domain. """

    @abc.abstractmethod
    def generate_point(self) -> Vec2D:
        """Generate a random point in the domain. """

    @abc.abstractmethod
    def contains(self, p) -> bool:
        """Test that the domain contains p. """


class RectangularVascularDomain(VascularDomain):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def area(self):
        return self.x * self.y

    def point_grid(self, s=1000):
        for i in range(0, s):
            for j in range(0, s):
                x = self.x * (i / s)
                y = self.y * (j / s)
                yield Vec2D(x, y)

    def generate_point(self) -> Vec2D:
        i = random.uniform(0, self.x)
        j = random.uniform(0, self.y)
        return Vec2D(i, j)

    def contains(self, p) -> bool:
        return self.x >= p.x >= 0 and self.y >= p.y >= 0


class CircularVascularDomain(VascularDomain):

    def __init__(self, radius):
        self.radius = radius
        self.enclosure = RectangularVascularDomain(radius*2, radius*2)

    @property
    def area(self):
        return pi * self.radius**2

    def point_grid(self, intervals=1000):
        return (p for p in self.enclosure.point_grid(intervals) if self.contains(p))

    def generate_point(self) -> Vec2D:
        p = self.enclosure.generate_point()
        while not self.contains(p):
            p = self.enclosure.generate_point()
        return p

    def contains(self, p) -> bool:
        return abs(p - Vec2D(self.radius, self.radius)) < self.radius
