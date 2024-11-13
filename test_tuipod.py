#
# test_tuipod.py
#
# 2024-11-12: Matthew Hickson
#

import unittest

import tuipod


class TestSmokeTest(unittest.TestCase):

    def test_sanity_check(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
