import abc
import random
from abc import ABC

from LinAlg import LineSegment, Vec2D


class VascularDomain(ABC):

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

    def generate_point(self) -> Vec2D:
        p = self.enclosure.generate_point()
        while not self.contains(p):
            p = self.enclosure.generate_point()
        return p

    def contains(self, p) -> bool:
        return abs(p - Vec2D(self.radius, self.radius)) < self.radius
