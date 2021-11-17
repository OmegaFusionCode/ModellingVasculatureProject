import math
from collections import Generator

from BloodVessel import BloodVessel
from VascularDomain import VascularDomain
from VascularTree import VascularTree


class CCONetworkBuilder:

    def __init__(self, radius, initial_point, flow, domain: VascularDomain) -> None:
        self.radius = radius
        self.initial_point = initial_point
        self.flow = flow
        self.domain = domain

    def make_first_vessel(self) -> BloodVessel:
        def make(): return BloodVessel(1, self.initial_point, self.domain.generate_point())
        i = 0
        l_min = self.min_vessel_length(0)
        while (v := make()).length < l_min:
            if (i := i + 1) == 10:
                i = 0
                l_min *= 0.5
        return v

    def min_vessel_length(self, num_vessels: int) -> float:
        return self.domain.characteristic_length * math.sqrt(1 / (num_vessels + 1))

    def make_first_tree(self) -> VascularTree:
        v = self.make_first_vessel()
        return VascularTree([v], self.domain)

    def generate_trees(self, iterations: int) -> Generator[VascularTree]:
        tree = self.make_first_tree()
        if iterations > 0:
            yield tree
        for _ in range(1, iterations):
            tree = tree.next_vascular_tree()
            yield tree

    def run(self, iterations: int) -> VascularTree:
        *_, tree = self.generate_trees(iterations)
        return tree
