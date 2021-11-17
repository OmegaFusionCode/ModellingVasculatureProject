from __future__ import annotations

import math
from typing import List

from BloodVessel import BloodVessel
from LinAlg import Vec2D
from PointSampleHeuristic import PointSampleHeuristic
from VascularDomain import VascularDomain


INTERVALS = 5
RADIUS = 1


class VascularTree:

    def __init__(self, vessels: List[BloodVessel], domain: VascularDomain):
        self.vessels = vessels
        self.domain = domain

    @property
    def cost(self) -> float:
        """The total cost of all vessels in the tree. """
        return sum(v.cost for v in self.vessels)

    def nearest_point_to(self, p):
        """Find the nearest point on the tree to p. """
        nearest = None
        for v in self.vessels:
            this_nearest = v.nearest_point_to(p)
            if nearest is None or this_nearest < nearest:
                nearest = this_nearest
        return nearest

    def bifurcate(self, vj: BloodVessel, xp, xd) -> VascularTree:
        """Given an existing blood vessel vj, bifurcation point xp and terminal point xd,
        :return a VascularTree with vj bifurcated at xp.
        """
        xpj = vj.proximal_point
        xdj = vj.distal_point
        new_vessels = [v for v in self.vessels if v is not vj]
        new_vessels += [BloodVessel(RADIUS, xp, xd),
                        BloodVessel(RADIUS, xp, xdj),
                        BloodVessel(RADIUS, xpj, xp)]
        return VascularTree(new_vessels, self.domain)

    def get_candidate_bifurcation_points(self, xdi, vj):
        """Find the set of points that we might use to bifurcate."""
        h = PointSampleHeuristic(xdi, vj.proximal_point, vj.distal_point, INTERVALS)
        return self.domain.sample_discretised_points(h)

    def generate_next_terminal(self):
        """Generate the position of the next terminal point in the tree. """
        def new_point():
            return self.domain.generate_point()

        def valid(point: Vec2D):
            return all(v.line_seg.distance_to(point) > l_min for v in self.vessels)

        l_min = self.min_vessel_length
        i = 0
        while not valid(p := new_point()):
            if (i := i + 1) == 10:
                print(l_min)
                i = 0
                l_min *= 0.5
        return p

    @property
    def min_vessel_length(self) -> float:
        """The initial minimum permissible distance between new terminals and existing vascularisation. """
        return self.domain.characteristic_length * math.sqrt(1 / (len(self.vessels) + 1))

    def next_vascular_tree(self) -> VascularTree:
        """Make a vascular tree with an additional terminal. """
        best_tree = None
        while best_tree is None:
            xdi = self.generate_next_terminal()
            reachable = self.vessels  #self.vessels_reachable_from(xdi)
            # TODO: Ignore unreachable vessels early.
            for vj in reachable:
                xjs = self.get_candidate_bifurcation_points(xdi, vj)
                for xj in xjs:
                    new_tree = self.bifurcate(vj, xj, xdi)
                    if best_tree is None or new_tree.cost < best_tree.cost:
                        best_tree = new_tree
        return best_tree
