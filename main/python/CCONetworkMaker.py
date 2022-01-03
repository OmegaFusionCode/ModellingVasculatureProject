import math
from collections import Generator

from BloodVessel import BaseBloodVessel, Origin, BloodVessel
from VascularDomain import VascularDomain


class CCONetworkMaker:

    def __init__(self, radius, initial_point, flow, domain: VascularDomain) -> None:
        self.radius = radius
        self.initial_point = initial_point
        self.flow = flow
        self.domain = domain
        self._origin = None

    def _make_first_vessel(self) -> BaseBloodVessel:
        """Make the first vessel of the tree to start. """
        self._origin = Origin(self.radius, self.initial_point)
        p = self.domain.generate_point()
        self._origin.create_child(1.0, p)

    def generate_trees(self, iterations: int) -> Generator[BaseBloodVessel]:
        """A generator to produce the trees at all stages. """
        self._make_first_vessel()
        if iterations > 0:
            yield self._origin
        for _ in range(1, iterations):
            # Rescaling happens here.
            xd = self.domain.generate_point()  # Randomly select a terminal point to be connected to the tree.
            # TODO: Find the best bifurcation point.
            self._origin = self._origin.copy_subtree()
            min_c = None
            best_vj = None
            for vj in list(self._origin.descendants):
                vj.bifurcate(xd)
                bifurcated_vessels = vj.parent.children + [vj.parent]
                vt = vj.parent.children[1]
                assert len(bifurcated_vessels) == 3 and vj is bifurcated_vessels[0] and vt is bifurcated_vessels[1]
                intersection_found = False
                for w in self._origin.descendants:
                    if w not in bifurcated_vessels and vt.line_seg.intersects_with(w.line_seg):
                        # Don't consider this bifurcation further if it intersects with other vessels
                        intersection_found = True
                if intersection_found:
                    vj.remove_bifurcation()
                    continue
                c = self._origin.root.cost
                if min_c is None or c < min_c:
                    min_c = c
                    best_vj = vj
                assert self._origin.root is not vj
                vj.remove_bifurcation()
            assert best_vj is not None
            best_vj.bifurcate(xd)
            # TODO: Bifurcation
            yield self._origin
            # TODO: Geometric Optimisation

    def run(self, terminals: int) -> BaseBloodVessel:
        """Generate the trees, returning the final one. """
        assert terminals > 0
        *_, root = self.generate_trees(terminals)
        return root
