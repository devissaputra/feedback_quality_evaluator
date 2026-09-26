import unittest
from feedback_quality_evaluator.core import cohen_kappa, weighted_cohen_kappa, exact_agreement

class KappaDegeneracyTests(unittest.TestCase):
    def test_constant_identical_ratings_have_undefined_kappa(self):
        a=[1,1,1]
        self.assertEqual(exact_agreement(a,a),1.0)
        self.assertIsNone(cohen_kappa(a,a))
        self.assertIsNone(weighted_cohen_kappa(a,a))

    def test_variable_identical_ratings_have_perfect_kappa(self):
        a=[0,1,2]
        self.assertEqual(cohen_kappa(a,a),1.0)
        self.assertEqual(weighted_cohen_kappa(a,a),1.0)
