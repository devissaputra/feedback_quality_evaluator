# Calculation guide

## Question and evidence

Is feedback grounded and actionable in its supplied context?

Feedback text, goal, learner work, evidence and an optional external reference verdict.

**Status:** SYNTHETIC / RULE-BASED PROTOTYPE | no educational validity claim.

## Design

Score separate lexical rubric dimensions; preserve not-evaluable fields; report flags and compare ratings.

## Calculation and interpretation

`Kappa = (observed agreement - chance agreement)/(1 - chance agreement).`

Constant identical ratings make chance agreement one and kappa undefined, not perfect. Lexical cues do not prove semantic grounding. Reference correctness is supplied externally; dimensions are not collapsed into a total quality score.

## Evidence table

Worked example — illustrative, not a measured research result. Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| Cohen kappa: [1,1,0] vs [1,0,0] | 0.39999999999999997 | unitless | `outputs.Cohen kappa: [1,1,0] vs [1,0,0]` |
| constant-label kappa | undefined | unitless | `outputs.constant-label kappa` |
| exact agreement of constant labels | 1.0 | unitless | `outputs.exact agreement of constant labels` |

Source: [results/review_examples.json](results/review_examples.json). Values resolve directly from this file when figures are regenerated.

This evaluator examines feedback against supplied task context using separate, transparent rubric dimensions. It preserves missing evidence as unevaluable, exposes lexical triggers, and provides rater-agreement tools whose degenerate cases are handled explicitly. The project is a baseline for validation and error analysis, not an automated authority on disciplinary correctness or feedback quality.

## Verification performed in this review

41 existing unittest checks passed. The bundled demonstration executed successfully in this review.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

For the explicitly illustrative example:

```bash
python scripts/review_examples.py
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`optional`](scripts/run_demo.py#L18) | Inspect the explicit implementation and its callers. |
| [`evaluate_feedback`](src/feedback_quality_evaluator/core.py#L551) | Evaluate feedback by separate transparent dimensions; no total score. |
| [`feedback_flags`](src/feedback_quality_evaluator/core.py#L584) | Inspect the explicit implementation and its callers. |
| [`revision_suggestions`](src/feedback_quality_evaluator/core.py#L662) | Inspect the explicit implementation and its callers. |
| [`cohen_kappa`](src/feedback_quality_evaluator/core.py#L724) | Return unweighted kappa, or None when chance agreement is one. |
| [`weighted_cohen_kappa`](src/feedback_quality_evaluator/core.py#L749) | Return weighted kappa; None means expected disagreement is zero. |
| [`exact_agreement`](src/feedback_quality_evaluator/core.py#L811) | Inspect the explicit implementation and its callers. |
| [`mean_absolute_error`](src/feedback_quality_evaluator/core.py#L819) | Inspect the explicit implementation and its callers. |
| [`dimension_validation`](src/feedback_quality_evaluator/core.py#L835) | Compare 0-2 automated and human ordinal ratings for one dimension. |
| [`pairwise_rater_summary`](src/feedback_quality_evaluator/core.py#L872) | Return pairwise ordinal agreement; not a multi-rater reliability coefficient. |
| [`score_feedback`](src/feedback_quality_evaluator/core.py#L912) | Legacy 0-4 view. Prefer evaluate_feedback() for research use. |
| [`disagreement`](src/feedback_quality_evaluator/core.py#L781) | Inspect the explicit implementation and its callers. |

## What remains before a stronger research claim

Constant identical ratings make chance agreement one and kappa undefined, not perfect. Lexical cues do not prove semantic grounding. Reference correctness is supplied externally; dimensions are not collapsed into a total quality score. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
