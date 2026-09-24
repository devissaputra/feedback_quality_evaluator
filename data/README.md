# Data documentation

## Included synthetic data

This repository contains two synthetic CSV files.

- `sample.csv`: 20 feedback cases with task/rubric context, learner work, identified issue, supporting evidence, expected standard, an externally supplied reference verdict, and the feedback text.
- `ratings.csv`: two synthetic human-rater profiles for seven rubric dimensions.

No real learner, instructor, student submission, or institution is represented.

## Why context is required

Feedback cannot be evaluated responsibly from wording alone.

The main evaluator therefore accepts a structured `FeedbackContext` containing:

- feedback text
- task goal
- rubric criterion
- learner work
- identified issue
- supporting evidence
- expected standard
- external reference verdict

Not every field is mandatory, but missing context can make dimensions **not evaluable**.

## Reference verdict

`reference_verdict` is one of:

- `supports`
- `contradicts`
- `insufficient`
- `not_provided`

The evaluator does not infer disciplinary correctness from style or confidence.

A `supports` or `contradicts` verdict must come from an external reference process such as an answer key, validated calculation, rubric-grounded expert judgment, or other defensible evidence.

## Automated dimensions

The current transparent baseline evaluates:

- goal alignment
- grounding/specificity
- actionability
- explanatory rationale
- feed-forward quality
- constructive framing
- learner agency
- reference alignment

Scores are 0–2 where evaluable.

Dimensions are deliberately **not** collapsed into a single total.

## Synthetic stress cases

The corpus deliberately includes:

- short but precise corrective feedback
- long but vague feedback
- generic praise
- vague criticism
- person-focused judgment
- unsupported certainty
- rubric mismatch
- action without evidence
- rationale words without grounding
- reference contradiction
- agency-supportive wording
- missing context
- strong feed-forward
- correct but non-actionable information

These are test fixtures, not empirical findings.

## Human ratings

`ratings.csv` contains synthetic ordinal ratings from two fictional raters for seven dimensions.

The ratings exist only to exercise:

- exact agreement
- weighted Cohen kappa
- dimension-level heuristic-versus-human comparison

They must not be reported as real inter-rater reliability.

## Before real data are connected

Document:

- learning task and discipline
- feedback source
- target learner population
- rubric dimension definitions
- rater training
- rating scale
- adjudication rules
- reference-answer/evidence process
- de-identification procedure
- sampling strategy
- language(s)
- feedback timing
- learner uptake/outcome measurement
- missing-context rules
- permitted uses and retention

## Privacy

Feedback and learner work can contain identifiers and sensitive educational records.

Do not commit identifiable submissions, private instructor comments, grades, accommodations, health information, private LMS exports, licensed assessment items, or restricted institutional material.

Use de-identified research data in an approved environment and keep only permissible synthetic or derived examples in this repository.
