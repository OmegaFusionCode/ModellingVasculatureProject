import math
import random
import unittest

import numpy as np

from LinAlg import Vec2D, parallel, LineSegment


def rn(): return random.uniform(0.0, 100.0)


DIMS = 2
random.seed(1637682142)

# Some values we can just grab during tests
points = [(rn(), rn()) for _ in range(1000)]
points2 = [(rn(), rn()) for _ in range(1000)]
vals = [random.uniform(0.0, 100.0) for _ in range(1000)]
vals0to1 = [random.uniform(0.0, 1.0) for _ in range(1000)]
vecs = [Vec2D(rn(), rn()) for _ in range(500)]
vecs2 = [Vec2D(rn(), rn()) for _ in range(500)]


class TestVec2D(unittest.TestCase):

    def test_constructor_rand(self):
        for x, y in points:
            v = Vec2D(x, y)
            self.assertEqual(v.x, x)
            self.assertEqual(v.y, y)

    def test_from_array_rand(self):
        for x, y in points:
            a = np.array((x, y))
            v = Vec2D.from_array(a)
            self.assertEqual(v.x, a[0])
            self.assertEqual(v.y, a[1])

    def test_eq_rand(self):
        for p1, p2 in zip(points, points2):
            x1, y1 = p1
            x2, y2 = p2
            if x1 != x2 or y1 != y2:
                v1 = Vec2D(x1, y1)
                v2 = Vec2D(x2, y2)
                self.assertIsNot(v1, v2)
                self.assertNotEqual(v1, v2)
        for x, y in points:
            v1 = Vec2D(x, y)
            v2 = Vec2D(x, y)
            self.assertIsNot(v1, v2)
            self.assertEqual(v1, v2)

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

    def test_add_rand(self):
        for p1, p2 in zip(points, points2):
            x1, y1 = p1
            x2, y2 = p2
            x3 = x1 + x2
            y3 = y1 + y2
            v1 = Vec2D(x1, y1)
            v2 = Vec2D(x2, y2)
            v3a = v1 + v2
            v3b = Vec2D(x3, y3)
            self.assertIsNot(v3a, v3b)
            self.assertEqual(v3a, v3b)

    def test_sub_rand(self):
        for p1, p2 in zip(points, points2):
            x1, y1 = p1
            x2, y2 = p2
            x3 = x1 - x2
            y3 = y1 - y2
            v1 = Vec2D(x1, y1)
            v2 = Vec2D(x2, y2)
            v3a = v1 - v2
            v3b = Vec2D(x3, y3)
            self.assertIsNot(v3a, v3b)
            self.assertEqual(v3a, v3b)

    def test_mul_rand(self):
        for p, n in zip(points, vals):
            x1, y1 = p
            x2 = x1 * n
            y2 = y1 * n
            v1 = Vec2D(x1, y1)
            v2a = v1 * n
            v2b = Vec2D(x2, y2)
            self.assertIsNot(v2a, v2b)
            self.assertEqual(v2a, v2b)

    def test_parallel_rand(self):
        for p, n in zip(points, vals):
            x, y = p
            v1 = Vec2D(x, y)
            v2 = v1 * n
            self.assertTrue(parallel(v1, v2))

    def test_abs_rand(self):
        for x, y in points:
            ans = math.sqrt(x ** 2 + y ** 2)
            v = Vec2D(x, y)
            res = abs(v) - ans
            self.assertIsInstance(res, float)
            # TODO: Better tolerance value
            self.assertLess(abs(res), 1e-13)


if __name__ == '__main__':
    unittest.main()
