import abc
import random
from abc import ABC
from typing import List

from LinAlg import LineSegment, Vec2D
from PointSampleHeuristic import PointSampleHeuristic


class VascularDomain(ABC):

    @property
    @abc.abstractmethod
    def characteristic_length(self):
        """The characteristic length of the region. """

    @abc.abstractmethod
    def generate_point(self) -> Vec2D:
        """Generate a random point in the domain. """

    @abc.abstractmethod
    def contains(self, p) -> bool:
        """Test that the domain contains p. """

    @abc.abstractmethod
    def sample_discretised_points(self, heuristic: PointSampleHeuristic) -> List[Vec2D]:
        """Get some points according to some method. """


class RectangularVascularDomain(VascularDomain):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def characteristic_length(self):
        raise NotImplementedError("Rectangular vascular domains currently do not have a characteristic length.")

    def generate_point(self) -> Vec2D:
        i = random.uniform(0, self.x)
        j = random.uniform(0, self.y)
        return Vec2D(i, j)

    def contains(self, p) -> bool:
        return self.x >= p.x >= 0 and self.y >= p.y >= 0

    def sample_discretised_points(self, heuristic: PointSampleHeuristic):
        """Select points in the domain according to the given point sampling heuristic. """

        return [p for p in heuristic.points if self.contains(p)]


class CircularVascularDomain(VascularDomain):

    def __init__(self, radius):
        self.radius = radius
        self.enclosure = RectangularVascularDomain(radius*2, radius*2)

    @property
    def characteristic_length(self):
        return self.radius

    def generate_point(self) -> Vec2D:
        p = self.enclosure.generate_point()
        while not self.contains(p):
            p = self.enclosure.generate_point()
        return p

    def contains(self, p) -> bool:
        return abs(p - Vec2D(self.radius, self.radius)) < self.radius

    def sample_discretised_points(self, heuristic: PointSampleHeuristic) -> List[Vec2D]:
        return [p for p in self.enclosure.sample_discretised_points(heuristic) if self.contains(p)]


def main():
    v = RectangularVascularDomain(10, 10)
    h = PointSampleHeuristic(Vec2D(1, 1), Vec2D(5, 4), Vec2D(7, 2), 3)
    ps = v.sample_discretised_points(h)
    print(ps)


if __name__ == '__main__':
    main()
