import os
# from helpers import *    # do not pollute yon namespace, sir
from helpers import int2bool, bool2int, int2choice, choice2int, \
     appendage2choice, choice2appendage
import unittest

class HelpersTestCase(unittest.TestCase):

    def test_int2bool(self):
        assert 'True'  == int2bool(1)
        assert 'False' == int2bool(0)
        assert 'False' == int2bool(-1)

    def test_bool2int(self):
        assert 1 == bool2int('True')
        assert 0 == bool2int('False')
        assert 0 == bool2int('')

    def test_int2choice(self):
        assert 'True'   == int2choice(2)
        assert 'False'  == int2choice(0)
        assert 'Unsure' == int2choice(1)
        assert 'Unsure' == int2choice(-1)

    def test_choice2int(self):
        assert 2 == choice2int('True')
        assert 0 == choice2int('False')
        assert 1 == choice2int('Unsure')
        assert 1 == choice2int('')

    def test_appendage2choice(self):
        assert 'Concave or Flat' == appendage2choice(0)
        assert 'Convex' == appendage2choice(2)
        assert 'Unsure' == appendage2choice(1)
        assert 'Unsure' == appendage2choice(-1)

    def test_choice2appendage(self):
        assert 0 == choice2appendage('Concave')
        assert 0 == choice2appendage('Flat')
        assert 2 == choice2appendage('Convex')
        assert 1 == choice2appendage('Unsure')
        assert 1 == choice2appendage('')

if __name__ == '__main__':
    unittest.main()


