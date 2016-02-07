import os
from formulas import getXrayOutcome
import unittest

class FormulasTestCase(unittest.TestCase):

    def test_xrayOutcome_normal(self):
        assert 'Normal' == getXrayOutcome('female', 0, 5.5, 0)
        assert 'Normal' == getXrayOutcome('male',   0, 9.5, 0)
        assert 'Normal' == getXrayOutcome('female', 0, 5.5, 1)
        assert 'Normal' == getXrayOutcome('male',   0, 5.5, 2)

    def test_xrayOutcome_moderate(self):
        assert 'Moderate to Severe' == getXrayOutcome('female', 2, 5.5, 0)
        assert 'Moderate to Severe' == getXrayOutcome('male',   2, 7.0, 0)
        assert 'Moderate to Severe' == getXrayOutcome('female', 2, 5.5, 1)

    def test_xrayOutcome_severe(self):
        assert 'Severe'  == getXrayOutcome('female', 2, 7.1, 0)
        assert 'Severe'  == getXrayOutcome('male',   2, 8.1, 1)
        assert 'Severe2' == getXrayOutcome('male',   2, 8.1, 2)
        assert 'Severe2' == getXrayOutcome('female', 2, 5.5, 2)

if __name__ == '__main__':
    unittest.main()


