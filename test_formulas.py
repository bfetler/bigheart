import os
from formulas import getXrayOutcome, getXrayOutcomePercent
import unittest

class FormulasTestCase(unittest.TestCase):

    def test_xrayOutcome_normal(self):
        self.assertEqual('Normal', getXrayOutcome('female', 0, 5.5, 0))
        self.assertEqual('Normal', getXrayOutcome('male',   0, 9.5, 0))
        self.assertEqual('Normal', getXrayOutcome('female', 0, 5.5, 1))
        self.assertEqual('Normal', getXrayOutcome('male',   0, 5.5, 2))

    def test_xrayOutcome_moderate(self):
        self.assertEqual('Moderate', getXrayOutcome('female', 2, 5.5, 0))
        self.assertEqual('Moderate', getXrayOutcome('male',   2, 7.0, 0))

    def test_xrayOutcome_severe(self):
        self.assertEqual('Severe', getXrayOutcome('female', 2, 5.5, 1))
        self.assertEqual('Severe', getXrayOutcome('female', 2, 7.1, 0))
        self.assertEqual('Severe', getXrayOutcome('male',   2, 8.1, 1))
        self.assertEqual('Severe', getXrayOutcome('male',   2, 8.1, 2))
        self.assertEqual('Severe', getXrayOutcome('female', 2, 5.5, 2))

    def test_xrayOutcomePercent_normal(self):
        self.assertGreaterEqual(0.5, getXrayOutcomePercent('female', 0, 5.5, 0))  # Normal
        self.assertGreaterEqual(0.5, getXrayOutcomePercent('female', 0, 7.5, 0))  # Normal
        self.assertGreaterEqual(0.5, getXrayOutcomePercent('male',   0, 9.5, 0))  # Normal
        self.assertGreaterEqual(0.5, getXrayOutcomePercent('female', 0, 7.0, 1))  # Normal
        self.assertGreaterEqual(0.5, getXrayOutcomePercent('female', 0, 7.0, 2))  # Normal
        self.assertGreaterEqual(0.5, getXrayOutcomePercent('male',   1, 7.0, 0))  # Normal
        self.assertGreaterEqual(0.5, getXrayOutcomePercent('male',   1, 8.0, 0))  # Normal
        self.assertGreaterEqual(0.5, getXrayOutcomePercent('male',   1, 9.0, 0))  # Normal

    def test_xrayOutcomePercent_moderate(self):
        self.assertGreaterEqual(0.69, getXrayOutcomePercent('male',   2, 5.0, 0))  # Moderate
        self.assertGreaterEqual(0.69, getXrayOutcomePercent('male',   2, 7.0, 0))  # Moderate

    def test_xrayOutcomePercent_severe(self):
        self.assertLess(0.69, getXrayOutcomePercent('male',   2, 7.2, 0))  # Severe
        self.assertLess(0.69, getXrayOutcomePercent('male',   2, 8.0, 0))  # Severe
        self.assertLess(0.69, getXrayOutcomePercent('male',   2, 9.0, 0))  # Severe
        self.assertLess(0.69, getXrayOutcomePercent('male',   2, 7.0, 2))  # Severe
        self.assertLess(0.69, getXrayOutcomePercent('male',   2, 8.1, 1))  # Severe
        self.assertLess(0.69, getXrayOutcomePercent('female', 2, 5.5, 2))  # Severe

if __name__ == '__main__':
    unittest.main()


