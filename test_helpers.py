import os
# from helpers import *    # do not pollute yon namespace, sir
from helpers import int2bool, bool2int, int2choice, choice2int, \
     appendage2choice, choice2appendage
import unittest

class HelpersTestCase(unittest.TestCase):

    def test_int2bool(self):
        self.assertEqual('True', int2bool(1))
        self.assertEqual('False', int2bool(0))
        self.assertEqual('False', int2bool(-1))

    def test_bool2int(self):
        self.assertEqual(1, bool2int('True'))
        self.assertEqual(0, bool2int('False'))
        self.assertEqual(0, bool2int(''))

    def test_int2choice(self):
        self.assertEqual('True', int2choice(2))
        self.assertEqual('False', int2choice(0))
        self.assertEqual('Unsure', int2choice(1))
        self.assertEqual('Unsure', int2choice(-1))

    def test_choice2int(self):
        self.assertEqual(2, choice2int('True'))
        self.assertEqual(0, choice2int('False'))
        self.assertEqual(1, choice2int('Unsure'))
        self.assertEqual(1, choice2int(''))

    def test_appendage2choice(self):
        self.assertEqual('Concave or Flat', appendage2choice(0))
        self.assertEqual('Convex', appendage2choice(2))
        self.assertEqual('Unsure', appendage2choice(1))
        self.assertEqual('Unsure', appendage2choice(-1))

    def test_choice2appendage(self):
        self.assertEqual(0, choice2appendage('Concave'))
        self.assertEqual(0, choice2appendage('Flat'))
        self.assertEqual(2, choice2appendage('Convex'))
        self.assertEqual(1, choice2appendage('Unsure'))
        self.assertEqual(1, choice2appendage(''))

if __name__ == '__main__':
    unittest.main()


