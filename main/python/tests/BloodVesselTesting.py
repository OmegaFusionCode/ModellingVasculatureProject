import unittest

from BloodVessel import RootBloodVessel, ChildBloodVessel
from LinAlg import Vec2D


class BloodVesselTesting(unittest.TestCase):

    def test_something(self):
        v1 = RootBloodVessel(0.5, Vec2D(1.0, 2.0), Vec2D(3.0, 4.0))
        v2 = ChildBloodVessel(0.25, v1, Vec2D(3.5, 3.6))
        v3 = ChildBloodVessel(0.3, v1, Vec2D(4.5, 3.9))
        self.assertIs(v1, v2.parent)
        self.assertIs(v1, v3.parent)
        self.assertTrue(v2 in v1.children)
        self.assertTrue(v3 in v1.children)
        self.assertEqual(v1.distal_point, v2.proximal_point)
        self.assertEqual(v1.distal_point, v3.proximal_point)
        v4 = RootBloodVessel(0.5, Vec2D(1.5, 2.5), Vec2D(3.0, 4.0))
        v1.update_children(v4)
        self.assertIs(v4, v2.parent)
        self.assertIs(v4, v3.parent)
        self.assertTrue(v2 in v4.children)
        self.assertTrue(v3 in v4.children)
        self.assertEqual(v4.distal_point, v2.proximal_point)
        self.assertEqual(v4.distal_point, v3.proximal_point)


if __name__ == '__main__':
    unittest.main()
