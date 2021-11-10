from __future__ import annotations

from typing import List

from BloodVessel import BloodVessel
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
        return sum(v.cost for v in self.vessels)

    def nearest_point_to(self, p):
        nearest = None
        for v in self.vessels:
            this_nearest = v.nearest_point_to(p)
            if nearest is None or this_nearest < nearest:
                nearest = this_nearest
        return nearest

    def bifurcate(self, vj: BloodVessel, xp, xd) -> VascularTree:
        xpj = vj.proximal_point
        xdj = vj.distal_point
        new_vessels = [v for v in self.vessels if v is not vj]
        new_vessels += [BloodVessel(RADIUS, xp, xd),
                        BloodVessel(RADIUS, xp, xdj),
                        BloodVessel(RADIUS, xpj, xp)]
        return VascularTree(new_vessels, self.domain)

    def get_candidate_bifurcation_points(self, xdi, vj):
        h = PointSampleHeuristic(xdi, vj.proximal_point, vj.distal_point, INTERVALS)
        return self.domain.sample_discretised_points(h)

    def next_vascular_tree(self) -> VascularTree:
        best_tree = None
        while best_tree is None:
            xdi = self.domain.generate_point()
            #xn = self.nearest_point_to(xdi)
            # TODO: Compute the nearest point to xdi.
            reachable = self.vessels  #self.vessels_reachable_from(xdi)
            # TODO: Ignore unreachable vessels early.
            for vj in reachable:
                xjs = self.get_candidate_bifurcation_points(xdi, vj)
                for xj in xjs:
                    new_tree = self.bifurcate(vj, xj, xdi)
                    if best_tree is None or new_tree.cost < best_tree.cost:
                        best_tree = new_tree
        return best_tree
