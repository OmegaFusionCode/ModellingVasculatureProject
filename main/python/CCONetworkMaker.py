import math
from collections import Generator

from BloodVessel import BaseBloodVessel, Origin, BloodVessel
from VascularDomain import VascularDomain
#from VascularTree import VascularTree


class CCONetworkMaker:

    def __init__(self, radius, initial_point, flow, domain: VascularDomain) -> None:
        self.radius = radius
        self.initial_point = initial_point
        self.flow = flow
        self.domain = domain

    def _make_first_vessel(self) -> BaseBloodVessel:
        """Make the first vessel of the tree to start. """
        origin = Origin(self.radius, self.initial_point)
        p = self.domain.generate_point()
        origin.create_child(self.radius, p)
        return origin

    def generate_trees(self, iterations: int) -> Generator[BaseBloodVessel]:
        """A generator to produce the trees at all stages. """
        origin = self._make_first_vessel()
        if iterations > 0:
            yield origin
        for _ in range(1, iterations):
            origin = origin.copy_subtree()
            # Rescaling happens here.
            xd = self.domain.generate_point()   # Randomly select a terminal point to be connected to the tree.
            #vj, xp = CCONetworkMaker.find_bifurcation(root, self.domain)
            # TODO: Find the best bifurcation point.
            # For now, just choose any vessel.
            vj = origin.root
            vj.bifurcate(xd)
            # TODO: Bifurcation
            assert(origin.root is not vj)
            yield origin
            # TODO: Geometric Optimisation

    def run(self, terminals: int) -> BaseBloodVessel:
        """Generate the trees, returning the final one. """
        assert(terminals > 0)
        *_, root = self.generate_trees(terminals)
        return root
