import unittest

from app import extract_pairs, interpret, is_correct


class DemoTests(unittest.TestCase):
    def test_foundation_factor(self):
        self.assertTrue(is_correct("factor", "(x + 3)(y + 2) = 13")[0])

    def test_informal_divisibility(self):
        self.assertTrue(is_correct("divides", "3x-1 chc x^2-x+1")[0])

    def test_official_divisibility(self):
        self.assertTrue(is_correct("divides", "x²-x+1 | 3x-1")[0])

    def test_pairs(self):
        self.assertEqual(extract_pairs("(1; 1), (1; -2), (-2; 1)"), {(1, 1), (1, -2), (-2, 1)})

    def test_intent(self):
        self.assertIn("gợi ý", interpret("gợi ý"))


if __name__ == "__main__":
    unittest.main()
