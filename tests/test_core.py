import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from feedback_quality_evaluator import core


def context(**overrides):
    base = {
        "feedback_text": (
            "Replace 'causes' with 'is associated with' because the "
            "study reports correlation, then verify the claim against "
            "the rubric criterion."
        ),
        "task_goal": "Interpret statistical evidence accurately",
        "rubric_criterion": "Distinguish correlation from causation",
        "learner_work": (
            "The results prove that screen time causes lower sleep quality."
        ),
        "identified_issue": "causation claim from correlational evidence",
        "supporting_evidence": "the study reports correlation only",
        "expected_standard": (
            "Use association language when causal identification is absent"
        ),
        "reference_verdict": "supports",
    }
    base.update(overrides)
    return core.FeedbackContext(**base)


class CoreTests(unittest.TestCase):
    def test_context_requires_feedback(self):
        with self.assertRaises(ValueError):
            core.FeedbackContext(feedback_text="   ")

    def test_context_rejects_bad_reference_verdict(self):
        with self.assertRaises(ValueError):
            core.FeedbackContext(
                feedback_text="Revise this.",
                reference_verdict="probably",
            )

    def test_evaluate_returns_all_dimensions(self):
        result = core.evaluate_feedback(context())
        self.assertEqual(
            set(result["dimensions"]),
            set(core.DIMENSIONS),
        )

    def test_no_overall_score(self):
        result = core.evaluate_feedback(context())
        self.assertIsNone(result["overall_score"])

    def test_goal_alignment_not_evaluable_without_goal_context(self):
        value = context(
            task_goal=None,
            rubric_criterion=None,
            expected_standard=None,
        )
        result = core.evaluate_feedback(value)
        self.assertEqual(
            result["dimensions"]["goal_alignment"]["status"],
            "not_evaluable",
        )

    def test_goal_alignment_detects_overlap(self):
        value = context(
            feedback_text=(
                "Revise the causation claim to distinguish correlation "
                "from causation."
            )
        )
        score = core.evaluate_feedback(value)["dimensions"][
            "goal_alignment"
        ]["score"]
        self.assertGreaterEqual(score, 1)

    def test_grounding_not_evaluable_without_work_context(self):
        value = context(
            learner_work=None,
            identified_issue=None,
            supporting_evidence=None,
        )
        dimension = core.evaluate_feedback(value)["dimensions"][
            "grounding_specificity"
        ]
        self.assertEqual(dimension["status"], "not_evaluable")

    def test_short_precise_feedback_can_score_grounding(self):
        value = context(
            feedback_text=(
                "Replace 'causes' with 'is associated with'; "
                "the study reports correlation."
            )
        )
        dimension = core.evaluate_feedback(value)["dimensions"][
            "grounding_specificity"
        ]
        self.assertGreaterEqual(dimension["score"], 1)

    def test_verbose_vague_feedback_does_not_gain_specificity_from_length(self):
        value = context(
            feedback_text=(
                "This is a very long and detailed sounding response with "
                "many different words and several sentences that discuss "
                "important improvements without naming the actual issue."
            )
        )
        dimension = core.evaluate_feedback(value)["dimensions"][
            "grounding_specificity"
        ]
        self.assertEqual(dimension["score"], 0)

    def test_actionability_detects_action_verb(self):
        dimension = core.evaluate_feedback(context())["dimensions"][
            "actionability"
        ]
        self.assertEqual(dimension["score"], 2)

    def test_actionability_zero_without_action(self):
        value = context(feedback_text="The claim is weak.")
        dimension = core.evaluate_feedback(value)["dimensions"][
            "actionability"
        ]
        self.assertEqual(dimension["score"], 0)

    def test_rationale_marker_alone_is_not_full_score(self):
        value = context(
            feedback_text="Revise this because it is wrong.",
            learner_work="A completely unrelated learner response.",
            identified_issue="causation claim",
            supporting_evidence="correlation only",
        )
        dimension = core.evaluate_feedback(value)["dimensions"][
            "explanatory_rationale"
        ]
        self.assertEqual(dimension["score"], 1)

    def test_grounded_rationale_gets_full_score(self):
        dimension = core.evaluate_feedback(context())["dimensions"][
            "explanatory_rationale"
        ]
        self.assertEqual(dimension["score"], 2)

    def test_feed_forward_detects_action_and_check(self):
        dimension = core.evaluate_feedback(context())["dimensions"][
            "feed_forward"
        ]
        self.assertEqual(dimension["score"], 2)

    def test_feed_forward_action_only_is_partial(self):
        value = context(
            feedback_text="Replace the causation claim."
        )
        dimension = core.evaluate_feedback(value)["dimensions"][
            "feed_forward"
        ]
        self.assertEqual(dimension["score"], 1)

    def test_generic_praise_is_flagged(self):
        value = context(
            feedback_text="Good job.",
            task_goal=None,
            rubric_criterion=None,
            learner_work=None,
            identified_issue=None,
            supporting_evidence=None,
            expected_standard=None,
            reference_verdict="not_provided",
        )
        result = core.evaluate_feedback(value)
        self.assertIn("generic_praise", result["flags"])

    def test_person_focused_judgment_is_zero_constructive(self):
        value = context(feedback_text="You are lazy and careless.")
        dimension = core.evaluate_feedback(value)["dimensions"][
            "constructive_framing"
        ]
        self.assertEqual(dimension["score"], 0)

    def test_task_focused_correction_is_constructive(self):
        dimension = core.evaluate_feedback(context())["dimensions"][
            "constructive_framing"
        ]
        self.assertEqual(dimension["score"], 2)

    def test_agency_supportive_language_scores_two(self):
        value = context(
            feedback_text=(
                "You could compare the claim with the correlation "
                "criterion, then revise it."
            )
        )
        dimension = core.evaluate_feedback(value)["dimensions"][
            "learner_agency"
        ]
        self.assertEqual(dimension["score"], 2)

    def test_coercive_language_scores_zero(self):
        value = context(
            feedback_text="You must just do this correctly."
        )
        dimension = core.evaluate_feedback(value)["dimensions"][
            "learner_agency"
        ]
        self.assertEqual(dimension["score"], 0)

    def test_reference_alignment_supports(self):
        dimension = core.evaluate_feedback(context())["dimensions"][
            "reference_alignment"
        ]
        self.assertEqual(dimension["score"], 2)

    def test_reference_alignment_contradiction(self):
        value = context(reference_verdict="contradicts")
        result = core.evaluate_feedback(value)
        self.assertEqual(
            result["dimensions"]["reference_alignment"]["score"],
            0,
        )
        self.assertIn("reference_contradiction", result["flags"])

    def test_reference_alignment_not_evaluable(self):
        value = context(reference_verdict="not_provided")
        dimension = core.evaluate_feedback(value)["dimensions"][
            "reference_alignment"
        ]
        self.assertEqual(dimension["status"], "not_evaluable")

    def test_certainty_without_reference_is_flagged(self):
        value = context(
            feedback_text="This definitely proves causation.",
            reference_verdict="not_provided",
        )
        result = core.evaluate_feedback(value)
        self.assertIn(
            "certainty_without_reference",
            result["flags"],
        )

    def test_goal_mismatch_is_flagged(self):
        value = context(
            feedback_text=(
                "Add more colors to the slide and change the font."
            )
        )
        result = core.evaluate_feedback(value)
        self.assertIn(
            "goal_or_rubric_mismatch",
            result["flags"],
        )

    def test_missing_action_generates_revision_suggestion(self):
        value = context(feedback_text="The claim is weak.")
        result = core.evaluate_feedback(value)
        self.assertTrue(
            any(
                "feasible action" in suggestion
                for suggestion in result["revision_suggestions"]
            )
        )

    def test_reference_contradiction_generates_suggestion(self):
        value = context(reference_verdict="contradicts")
        result = core.evaluate_feedback(value)
        self.assertTrue(
            any(
                "reference evidence" in suggestion
                for suggestion in result["revision_suggestions"]
            )
        )

    def test_unicode_tokenization_handles_non_ascii_words(self):
        value = context(
            feedback_text=(
                "Revise análisis because correlación does not prove "
                "causación."
            ),
            identified_issue="correlación causación",
            supporting_evidence="correlación only",
        )
        dimension = core.evaluate_feedback(value)["dimensions"][
            "grounding_specificity"
        ]
        self.assertGreaterEqual(dimension["score"], 1)

    def test_cohen_kappa_known_example(self):
        self.assertAlmostEqual(
            core.cohen_kappa([1, 1, 0], [1, 0, 0]),
            0.4,
        )

    def test_cohen_kappa_rejects_empty(self):
        with self.assertRaises(ValueError):
            core.cohen_kappa([], [])

    def test_weighted_kappa_perfect(self):
        self.assertEqual(
            core.weighted_cohen_kappa(
                [0, 1, 2],
                [0, 1, 2],
            ),
            1.0,
        )

    def test_weighted_kappa_rejects_non_integer_ordinal(self):
        with self.assertRaises(ValueError):
            core.weighted_cohen_kappa(
                [0.0, 1.0],
                [0.0, 1.0],
            )

    def test_weighted_kappa_rejects_bad_weighting(self):
        with self.assertRaises(ValueError):
            core.weighted_cohen_kappa(
                [0, 1],
                [0, 1],
                weighting="mystery",
            )

    def test_exact_agreement(self):
        self.assertAlmostEqual(
            core.exact_agreement([0, 1, 2], [0, 1, 1]),
            2 / 3,
        )

    def test_mean_absolute_error(self):
        self.assertAlmostEqual(
            core.mean_absolute_error(
                [0, 1, 2],
                [0, 2, 2],
            ),
            1 / 3,
        )

    def test_mae_rejects_nan(self):
        with self.assertRaises(ValueError):
            core.mean_absolute_error(
                [0, math.nan],
                [0, 1],
            )

    def test_dimension_validation(self):
        result = core.dimension_validation(
            [0, 1, 2, 2],
            [0, 1, 1, 2],
        )
        self.assertEqual(result["n"], 4)
        self.assertIn(
            "weighted_kappa_quadratic",
            result,
        )

    def test_dimension_validation_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            core.dimension_validation(
                [0, 3],
                [0, 2],
            )

    def test_pairwise_rater_summary(self):
        result = core.pairwise_rater_summary(
            {
                "r1": [0, 1, 2],
                "r2": [0, 1, 1],
                "r3": [0, 2, 2],
            }
        )
        self.assertEqual(result["pair_count"], 3)

    def test_pairwise_summary_requires_two_raters(self):
        with self.assertRaises(ValueError):
            core.pairwise_rater_summary(
                {"r1": [0, 1]}
            )

    def test_legacy_wrapper_still_returns_old_shape(self):
        result = core.score_feedback(
            "Revise this because the evidence is weak.",
            True,
        )
        self.assertIn("total", result)
        self.assertTrue(result["legacy_heuristic"])


if __name__ == "__main__":
    unittest.main()
