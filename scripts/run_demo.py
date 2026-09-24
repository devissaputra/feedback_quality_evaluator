import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from feedback_quality_evaluator.core import (
    FeedbackContext,
    DIMENSIONS,
    dimension_validation,
    evaluate_feedback,
    pairwise_rater_summary,
)


def optional(value):
    value = value.strip()
    return value or None


examples = []
with (ROOT / "data" / "sample.csv").open(
    encoding="utf-8",
    newline="",
) as handle:
    for row in csv.DictReader(handle):
        context = FeedbackContext(
            feedback_text=row["feedback_text"],
            task_goal=optional(row["task_goal"]),
            rubric_criterion=optional(row["rubric_criterion"]),
            learner_work=optional(row["learner_work"]),
            identified_issue=optional(row["identified_issue"]),
            supporting_evidence=optional(row["supporting_evidence"]),
            expected_standard=optional(row["expected_standard"]),
            reference_verdict=row["reference_verdict"],
        )
        examples.append(
            {
                "feedback_id": row["feedback_id"],
                "context": context,
                "result": evaluate_feedback(context),
            }
        )

ratings = defaultdict(dict)
with (ROOT / "data" / "ratings.csv").open(
    encoding="utf-8",
    newline="",
) as handle:
    for row in csv.DictReader(handle):
        ratings[row["rater"]][row["feedback_id"]] = {
            dimension: int(row[dimension])
            for dimension in DIMENSIONS
            if dimension != "reference_alignment"
        }

print("Feedback Quality Evaluator synthetic demo")
print()

for item in examples:
    result = item["result"]
    print(item["feedback_id"], item["context"].feedback_text)
    printable = {}
    for dimension, record in result["dimensions"].items():
        printable[dimension] = (
            record["score"]
            if record["status"] == "scored"
            else "not_evaluable"
        )
    print(" dimensions:", printable)
    print(" flags:", result["flags"])
    if result["revision_suggestions"]:
        print(" suggestions:", result["revision_suggestions"])

print("\nSynthetic rater agreement by dimension:")
for dimension in (
    "goal_alignment",
    "grounding_specificity",
    "actionability",
    "explanatory_rationale",
    "feed_forward",
    "constructive_framing",
    "learner_agency",
):
    r1 = [ratings["r1"][item["feedback_id"]][dimension] for item in examples]
    r2 = [ratings["r2"][item["feedback_id"]][dimension] for item in examples]
    summary = pairwise_rater_summary({"r1": r1, "r2": r2})
    pair = summary["pairs"][0]
    print(
        dimension,
        {
            "exact_agreement": round(pair["exact_agreement"], 3),
            "weighted_kappa_quadratic": round(
                pair["weighted_kappa_quadratic"], 3
            ),
        },
    )

print("\nHeuristic versus synthetic rater-1 where dimension is evaluable:")
for dimension in (
    "goal_alignment",
    "grounding_specificity",
    "actionability",
    "explanatory_rationale",
    "feed_forward",
    "constructive_framing",
    "learner_agency",
):
    auto = []
    human = []
    for item in examples:
        record = item["result"]["dimensions"][dimension]
        if record["status"] != "scored":
            continue
        auto.append(record["score"])
        human.append(
            ratings["r1"][item["feedback_id"]][dimension]
        )
    metrics = dimension_validation(auto, human)
    print(
        dimension,
        {
            "n": metrics["n"],
            "exact_agreement": round(
                metrics["exact_agreement"], 3
            ),
            "mae": round(
                metrics["mean_absolute_error"], 3
            ),
            "weighted_kappa_quadratic": round(
                metrics["weighted_kappa_quadratic"], 3
            ),
        },
    )

print(
    "\nNote: the corpus, reference verdicts, and human ratings are "
    "synthetic. The demo validates software behavior and exposes error "
    "patterns; it does not establish feedback-quality validity."
)
