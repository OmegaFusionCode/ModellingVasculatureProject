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

    def make_first_tree(self) -> VascularTree:
        d = self.domain.generate_point()
        v = BloodVessel(self.radius, self.initial_point, d)
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
