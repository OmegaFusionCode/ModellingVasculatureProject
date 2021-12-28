from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Any

from BloodVessel import BloodVessel, VesselGroup, test_for_length_zero
from LinAlg import Vec2D
from PointSampleHeuristic import PointSampleHeuristic
from VascularDomain import VascularDomain

INTERVALS = 5
RADIUS = 1


@dataclass(order=True)
class PrioritisedItem:
    priority: int
    item: Any = field(compare=False)


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

    def relative_cost(self, bifurcation):
        vj, group = bifurcation
        return group.cost - vj.cost

    def bifurcate(self, vj: BloodVessel, xp, xd) -> VesselGroup:
        """Given an existing blood vessel vj, bifurcation point xp and terminal point xd,
        :return a VesselGroup with the new vessels resulting from bifurcation.
        """
        # TODO: I think this should be refactored quite a bit.
        xpj = vj.proximal_point
        xdj = vj.distal_point
        return VesselGroup([BloodVessel(RADIUS, xp, xd),
                            BloodVessel(RADIUS, xp, xdj),
                            BloodVessel(RADIUS, xpj, xp)])

    def get_candidate_bifurcation_points(self, xdi, vj):
        """Find the set of points that we might use to bifurcate."""
        h = PointSampleHeuristic(xdi, vj.proximal_point, vj.distal_point, INTERVALS)
        return self.domain.sample_discretised_points(h)

    def generate_next_terminal(self):
        """Generate the position of the next terminal point in the tree. """
        def new_point():  # Get a random point in the domain.
            return self.domain.generate_point()

        def valid(point: Vec2D):  # Test if all vessels are sufficiently far away from the point.
            return all(v.line_seg.distance_to(point) > l_min for v in self.vessels)

        l_min = self.min_vessel_length
        i = 0
        while not valid(p := new_point()):
            if (i := i + 1) == 10:
                logging.debug(f"Rescaled {l_min=}")
                i = 0
                l_min *= 0.5
        return p

    @property
    def min_vessel_length(self) -> float:
        """The initial minimum permissible distance between new terminals and existing vascularisation. """
        return self.domain.characteristic_length * math.sqrt(1 / (len(self.vessels) + 1))

    def next_vascular_tree(self) -> VascularTree:
        """Make a vascular tree with an additional terminal. """
        # TODO: We could make this a bit tidier.
        best_bifurcation = None
        while best_bifurcation is None:
            xdi = self.generate_next_terminal()
            pq = PriorityQueue()
            for v in self.vessels:
                pq.put(PrioritisedItem(v.line_seg.distance_to(xdi), v))
            #num_vessels_to_try = max(round(math.sqrt(pq.qsize())), (pq.qsize()+1) // 2)
            num_vessels_to_try = round(2 * math.sqrt(pq.qsize()))
            #num_vessels_to_try = round(math.sqrt(pq.qsize()))
            # TODO: Ignore unreachable vessels early.
            for _ in range(num_vessels_to_try):
                if pq.empty():
                    break
                # Get the closest blood vessel in the priority queue
                vj = pq.get().item
                xjs = self.get_candidate_bifurcation_points(xdi, vj)
                for xj in xjs:
                    b = self.bifurcate(vj, xj, xdi)
                    if b.satisfies_geometrical_constraints:
                        this_bifurcation = vj, self.bifurcate(vj, xj, xdi)
                        if best_bifurcation is None or self.relative_cost(this_bifurcation) < self.relative_cost(
                                best_bifurcation):
                            best_bifurcation = this_bifurcation
        v_old, vessel_group = best_bifurcation
        if test_for_length_zero(vessel_group):
            logging.warning("Vessel of length 0 created!")
        return VascularTree([v for v in self.vessels if v is not v_old] + vessel_group.vessels, self.domain)
