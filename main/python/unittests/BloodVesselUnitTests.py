import unittest

from BloodVessel import Origin, BloodVessel
from LinAlg import Vec2D


class TestBloodVessel(unittest.TestCase):

    def test_something(self):
        r = Origin(0.5, Vec2D(1.0, 2.0))
        v1 = r.create_child(0.5, Vec2D(3.0, 4.0))
        v2 = v1.create_child(0.25, Vec2D(3.5, 3.6))
        v3 = v1.create_child(0.3, Vec2D(4.5, 3.9))
        self.assertIs(v1, v2.parent)
        self.assertIs(v1, v3.parent)
        self.assertTrue(v2 in v1.children)
        self.assertTrue(v3 in v1.children)
        self.assertEqual(v1.distal_point, v2.proximal_point)
        self.assertEqual(v1.distal_point, v3.proximal_point)

    def test_descendants(self):
        r = Origin(0.5, Vec2D(1.0, 2.0))
        v1 = r.create_child(0.5, Vec2D(3.0, 4.0))
        v2 = v1.create_child(0.25, Vec2D(3.5, 3.6))
        v3 = v1.create_child(0.3, Vec2D(4.5, 3.9))
        self.assertTrue(v2 in v1.descendants)
        self.assertTrue(v3 in v1.descendants)
        v4 = v3.create_child(0.2, Vec2D(9.9, 8.8))
        self.assertTrue(v4 in v3.descendants)
        self.assertTrue(v4 not in v2.descendants)
        self.assertTrue(v4 in v1.descendants)

    def test_bifurcation(self):
        r = Origin(1.0, Vec2D(5.0, 5.0))
        v1 = r.create_child(1.0, Vec2D(7.5, 7.5))
        self.assertEqual(r.root.proximal_point, Vec2D(5.0, 5.0))
        self.assertEqual(r.root.distal_point, Vec2D(7.5, 7.5))
        self.assertEqual(r.num_terminals, 1)
        v1.bifurcate(Vec2D(6.0, 7.0))
        self.assertIs(v1, v1.parent.children[0])
        self.assertIsNot(v1, v1.parent.children[1])
        self.assertEqual(len(list(v1.descendants)), 1)
        self.assertEqual(len(list(r.descendants)), 3)
        self.assertEqual(len(list(r.root.descendants)), 3)
        self.assertEqual(r.root.proximal_point, Vec2D(5.0, 5.0))
        self.assertEqual(r.root.distal_point, Vec2D(6.25, 6.25))
        self.assertEqual(r.root.children[0].proximal_point, Vec2D(6.25, 6.25))
        self.assertEqual(r.root.children[1].proximal_point, Vec2D(6.25, 6.25))
        self.assertEqual(r.root.children[0].distal_point, Vec2D(7.5, 7.5))
        self.assertEqual(r.root.children[1].distal_point, Vec2D(6.0, 7.0))
        self.assertEqual(r.num_terminals, 2)

    def test_copy_subtree(self):
        r = Origin(0.5, Vec2D(1.0, 2.0))
        v1 = r.create_child(0.5, Vec2D(3.0, 4.0))
        v1.create_child(0.25, Vec2D(3.5, 3.6))
        v3 = v1.create_child(0.3, Vec2D(4.5, 3.9))
        v3.create_child(0.2, Vec2D(9.9, 8.8))
        r_copy = r.copy_subtree()
        self.assertEqual(r, r_copy)
        self.assertIsNot(r, r_copy)
        descendants_old = list(r.descendants)
        descendants_new = list(r_copy.descendants)
        for d1, d2 in zip(descendants_old, descendants_new):
            self.assertEqual(d1, d2)
        for d1 in descendants_old:
            for d2 in descendants_new:
                self.assertIsNot(d1, d2)
        self.assertEqual(len(descendants_old), 4)
        self.assertEqual(len(descendants_new), 4)

    def test_remove_bifurcation(self):
        r = Origin(1.0, Vec2D(5.0, 5.0))
        r.create_child(1.0, Vec2D(7.5, 7.5))
        rc = r.copy_subtree()
        v = rc.children[0]
        v.bifurcate(Vec2D(6.0, 7.0))
        self.assertNotEqual(r, rc)
        v.remove_bifurcation()
        self.assertEqual(r, rc)

    def test_geometrically_optimise(self):
        r = Origin(1.0, Vec2D(0.0, 0.0))
        v = r.create_child(1.0, Vec2D(10.0, 0.0))
        v.bifurcate(Vec2D(5.0, 5.0))
        vp = v.parent
        va = vp.children[0]
        vb = vp.children[1]
        self.assertIs(v, va)
        self.assertIsNot(v, vb)
        xp = vp.proximal_point
        xa = va.distal_point
        xb = vb.distal_point
        xz = vp.distal_point
        self.assertEqual(xp, Vec2D(0.0, 0.0))
        self.assertEqual(xa, Vec2D(10.0, 0.0))
        self.assertEqual(xb, Vec2D(5.0, 5.0))
        self.assertEqual(xz, Vec2D(5.0, 0.0))
        v.geometrically_optimise()
        xp2 = vp.proximal_point
        xa2 = va.distal_point
        xb2 = vb.distal_point
        xz2 = vp.distal_point
        self.assertEqual(xp, xp2)
        self.assertEqual(xa, xa2)
        self.assertEqual(xb, xb2)
        self.assertNotEqual(xz, xz2)
        self.assertEqual(vp.distal_point, va.proximal_point)
        self.assertEqual(vp.distal_point, vb
                         .proximal_point)


if __name__ == '__main__':
    unittest.main()
