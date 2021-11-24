import math
import random
import unittest

import numpy as np

from LinAlg import Vec2D, parallel, LineSegment


def rn(): return random.uniform(0.0, 100.0)


DIMS = 2
TOL = 1e-13  # TODO: Better tolerance value?
random.seed(1637682142)

# Some values we can just grab during tests
points = [(rn(), rn()) for _ in range(1000)]
points2 = [(rn(), rn()) for _ in range(1000)]
vals = [random.uniform(0.0, 100.0) for _ in range(1000)]
vals0to1 = [random.uniform(0.0, 1.0) for _ in range(1000)]
vals1to2 = [random.uniform(1.0, 2.0) for _ in range(1000)]
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
            self.assertLess(abs(res), TOL)


class TestLineSegment(unittest.TestCase):

    def test_length_rand(self):
        for v1, v2 in zip(vecs, vecs2):
            seg = LineSegment(v1, v2)
            v3 = v2 - v1
            length = math.sqrt(v3.x ** 2 + v3.y ** 2)
            self.assertEqual(seg.length, length)

    def test_vector_rand(self):
        for v1, v2 in zip(vecs, vecs2):
            seg = LineSegment(v1, v2)
            v3 = v2 - v1
            self.assertIsNot(seg.vector, v3)
            self.assertEqual(seg.vector, v3)

    # TODO: Floating point inaccuracies. Investigate this later.
    def test_distance_to_rand(self):
        def generate_points(v1, v2, n1, n2):
            x1, y1 = v1.x, v1.y
            x2, y2 = v2.x, v2.y
            x_diff = x2 - x1
            y_diff = y2 - y1
            # Find a point on the line
            x3 = x1 + n1*x_diff
            y3 = y1 + n1*y_diff
            # Find a point whose closest point on the line is (x3, y3)
            x4 = x3 + n2*y_diff
            y4 = y3 - n2*x_diff
            v4 = Vec2D(x4, y4)
            dist = math.sqrt((x4-x3) ** 2 + (y4-y3) ** 2)
            return v4, dist
        # there are three cases:
        for v1, v2, n1, n2 in zip(vecs, vecs2, vals0to1, vals1to2):
            seg = LineSegment(v1, v2)
            #   between the two endpoints.
            v, d = generate_points(v1, v2, n1, n2)
            self.assertLess(abs(seg.distance_to(v) - d), TOL)
            #   or outside the leftmost one
            v, _ = generate_points(v1, v2, -n1, n2)
            d = math.sqrt((v.x - v1.x) ** 2 + (v.y - v1.y) ** 2)
            self.assertLess(abs(seg.distance_to(v) - d), TOL)
            #   or outside the rightmost one
            v, _ = generate_points(v1, v2, 1+n1, n2)
            d = math.sqrt((v.x - v2.x) ** 2 + (v.y - v2.y) ** 2)
            self.assertLess(abs(seg.distance_to(v) - d), TOL)


if __name__ == '__main__':
    unittest.main()
