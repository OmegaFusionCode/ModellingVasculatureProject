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

    def run(self, iterations: int) -> VascularTree:
        assert(iterations >= 1)
        trees = [self.make_first_tree()]
        for i in range(0, iterations-1):
            prev_tree = trees[i]
            next_tree = prev_tree.next_vascular_tree()
            trees.append(next_tree)
        final_tree = trees[iterations-1]
        return final_tree