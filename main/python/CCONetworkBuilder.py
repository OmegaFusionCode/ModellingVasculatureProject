import math
from collections import Generator

from BloodVessel import BloodVessel, RootBloodVessel
from VascularDomain import VascularDomain
from VascularTree import VascularTree


class CCONetworkBuilder:

    def __init__(self, radius, initial_point, flow, domain: VascularDomain) -> None:
        self.radius = radius
        self.initial_point = initial_point
        self.flow = flow
        self.domain = domain

    def make_first_vessel(self) -> BloodVessel:
        """Make the first vessel to be added to the empty tree. """
        def make(): return RootBloodVessel(1, self.initial_point, self.domain.generate_point())
        i = 0
        l_min = self.min_vessel_length(0)
        while (v := make()).length < l_min:
            if (i := i + 1) == 10:
                i = 0
                l_min *= 0.5
        return v

    def min_vessel_length(self, num_vessels: int) -> float:
        """The initial minimum permissible distance between new terminals and existing vascularisation. """
        return self.domain.characteristic_length * math.sqrt(1 / (num_vessels + 1))

    def make_first_tree(self) -> VascularTree:
        """Make the first tree of the network. """
        # TODO: Eliminate the special case for the first tree.
        v = self.make_first_vessel()
        return VascularTree([v], self.domain)

    def generate_trees(self, iterations: int) -> Generator[VascularTree]:
        """A generator to produce the trees at all stages. """
        tree = self.make_first_tree()
        if iterations > 0:
            yield tree
        for _ in range(1, iterations):
            tree = tree.next_vascular_tree()
            yield tree

    def run(self, iterations: int) -> VascularTree:
        """Generate the trees, returning the final one. """
        *_, tree = self.generate_trees(iterations)
        return tree
