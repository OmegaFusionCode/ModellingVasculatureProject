import random
import unittest

from LinAlg import Vec2D, LineSegment


def rn(): return random.uniform(0.0, 100.0)


DIMS = 2
TOL = 1e-13  # TODO: Better tolerance value?


class TestVec2D(unittest.TestCase):

    def test_abs(self):
        for v in (Vec2D(3.0, 4.0),
                  Vec2D(3.0, -4.0),
                  Vec2D(-3.0, 4.0),
                  Vec2D(-3.0, -4.0),
                  ):
            self.assertEqual(abs(v), 5.0)
        for v in (Vec2D(5.0, 12.0),
                  Vec2D(5.0, -12.0),
                  Vec2D(-5.0, 12.0),
                  Vec2D(-5.0, -12.0),
                  ):
            self.assertEqual(abs(v), 13.0)


class TestLineSegment(unittest.TestCase):

    def test_intersect(self):
        v1 = Vec2D(0.0, 0.0)
        v2 = Vec2D(1.0, 1.0)
        v3 = Vec2D(0.0, 1.0)
        v4 = Vec2D(1.0, 0.0)
        s1 = LineSegment(v1, v2)
        s2 = LineSegment(v3, v4)
        self.assertTrue(s1.intersects_with(s2))
        self.assertTrue(s2.intersects_with(s1))
        s3 = LineSegment(v1, v3)
        s4 = LineSegment(v2, v4)
        self.assertFalse(s3.intersects_with(s4))
        self.assertFalse(s4.intersects_with(s3))
        # Boundary case: The lines just touch.
        self.assertTrue(s2.intersects_with(s4))


if __name__ == '__main__':
    unittest.main()
