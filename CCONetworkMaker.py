import logging
import math
from collections import Generator
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any

from BloodVessel import BaseBloodVessel, Origin, BloodVessel
from VascularDomain import VascularDomain


def _has_misformed_vessels(vessels):
    for v in vessels:
        if v.radius > v.length:
            # Don't consider bifurcations that create a zero-length vessel.
            return True


@dataclass(order=True)
class PrioritisedItem:
    priority: float
    item: Any = field(compare=False)


class CCONetworkMaker:

    def __init__(self, radius, initial_point, flow, domain: VascularDomain) -> None:
        self.radius = radius
        self.initial_point = initial_point
        self.flow = flow
        self.domain = domain
        self._origin = None
        # Prepare some lists for logging purposes
        self.iter_num_with_depth = []
        self.iter_num_with_dist = []

    @property
    def perfusion_area(self):
        return self.domain.area

    def _generate_terminal_point(self, k_term):
        found = False
        d_thresh = math.sqrt(self.perfusion_area / k_term)
        logging.debug(f"{d_thresh=}")
        i = 0
        while not found:
            if i == 50:
                i = 0
                d_thresh *= 0.9
                logging.debug(f"Rescaled. {d_thresh=}")
            p = self.domain.generate_point()
            d_crit = min((v.line_seg.distance_to(p) for v in self._origin.descendants))
            if d_crit > d_thresh:
                found = True
            i += 1
        return p

    def _make_first_vessel(self) -> None:
        """Make the first vessel of the tree to start. """
        self._origin = Origin(self.radius, self.initial_point)
        p = self.domain.generate_point()
        self._origin.create_child(1.0, p)

    def generate_trees(self, iterations: int) -> Generator[BaseBloodVessel]:
        """A generator to produce the trees at all stages. """
        self._make_first_vessel()
        if iterations > 0:
            yield self._origin
        for i in range(1, iterations):
            # Rescaling happens here.
            xd = self._generate_terminal_point(i)  # Randomly select a terminal point to be connected to the tree.
            self._origin = self._origin.copy_subtree()
            min_c = None
            best_vj = None
            best_distance = None
            best_index = None
            line_distances = [PrioritisedItem(v.line_seg.distance_to(xd), v) for v in self._origin.descendants]
            num_vessels_to_try = len(line_distances)
            pq = PriorityQueue()
            for pair in line_distances:
                pq.put(pair)
            for j in range(num_vessels_to_try):
                assert pq.not_empty
                pair = pq.get()
                vj = pair.item
                this_distance = pair.priority
                # TODO: Here, we should copy the subtree with this vessel.
                vj.bifurcate(xd)
                vj.geometrically_optimise()
                # The bifurcation point has been added and moved to the optimal location
                bifurcated_vessels = vj.parent.children + [vj.parent]
                # Don't consider the vessel further if it is mis-formed.
                if _has_misformed_vessels(bifurcated_vessels):
                    vj.remove_bifurcation()
                    continue
                vt = vj.parent.children[1]
                assert len(bifurcated_vessels) == 3 and vj is bifurcated_vessels[0] and vt is bifurcated_vessels[1]
                # Next, we check ALL THREE of the vessels involved in bifurcation for intersections with other vessels
                intersection_found = False
                for v in bifurcated_vessels:
                    # Only these vessels are allowed to intersect with v. (self, parent, siblings and children)
                    incident_vessels = [v.parent] + v.parent.children + v.children
                    for w in self._origin.descendants:
                        if w not in incident_vessels and v.line_seg.intersects_with(w.line_seg):
                            # Don't consider this bifurcation further as it intersects with other vessels
                            intersection_found = True
                if intersection_found:
                    vj.remove_bifurcation()
                    continue
                c = self._origin.root.cost
                if min_c is None or c < min_c:
                    min_c = c
                    best_vj = vj
                    best_distance = this_distance
                    best_index = j
                assert self._origin.root is not vj
                vj.remove_bifurcation()
            assert best_vj is not None
            best_vj.bifurcate(xd)
            best_vj.geometrically_optimise()
            self.iter_num_with_depth.append((i, best_index))
            self.iter_num_with_dist.append((i, best_distance))
            yield self._origin

    def run(self, terminals: int) -> BaseBloodVessel:
        """Generate the trees, returning the final one. """
        assert terminals > 0
        *_, root = self.generate_trees(terminals)
        return root
