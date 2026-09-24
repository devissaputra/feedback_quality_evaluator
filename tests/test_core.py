import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from feedback_quality_evaluator import core


class CoreTests(unittest.TestCase):
    def test_feedback_score_and_kappa(self):
        score = core.score_feedback("Revise this because the evidence is weak.", True)
        self.assertGreaterEqual(score["total"], 3)
        self.assertLessEqual(score["total"], 4)
        self.assertAlmostEqual(core.cohen_kappa([1, 1, 0], [1, 0, 0]), 0.4)

    def test_empty_feedback_is_rejected(self):
        with self.assertRaises(ValueError):
            core.score_feedback("   ")


if __name__ == "__main__":
    unittest.main()
