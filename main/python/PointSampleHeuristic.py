from typing import List

from LinAlg import Vec2D, LineSegment


class PointSampleHeuristic:

    def __init__(self, p, q, r, intervals):
        assert(intervals >= 2)
        self.p = p
        self.q = q
        self.r = r
        self.n = intervals

    @property
    def points(self) -> List[Vec2D]:
        """Get the list of points to sample. """
        p, q, r, n = self.p, self.q, self.r, self.n
        pq = LineSegment(p, q)
        unit_pq = pq.vector * (1/(n-1))
        pr = LineSegment(p, r)
        unit_pr = pr.vector * (1/(n-1))
        current_component_pq = Vec2D(0, 0)
        sampled_points = []
        for i in range(n):
            current_component_pr = Vec2D(0, 0)
            for j in range(n-i):
                sampled_points.append(p + current_component_pq + current_component_pr)
                current_component_pr += unit_pr
            current_component_pq += unit_pq
        return sampled_points
