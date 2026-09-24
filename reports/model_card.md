# Analytic system card

## System

Feedback Quality Evaluator

## Purpose

Context-aware, multidimensional formative-feedback review with transparent heuristics, explicit not-evaluable states, reference-evidence boundaries, error flags, and human-rater validation tools.

## Current maturity

Working research prototype.

The bundled feedback cases, reference verdicts, and rater scores are synthetic.

The repository validates software behavior and exposes failure modes. It does not establish real-world feedback-quality validity.

## Inputs

The main API accepts a `FeedbackContext` containing:

- feedback text
- task goal
- rubric criterion
- learner work
- identified issue
- supporting evidence
- expected standard
- external reference verdict

Context fields may be absent.

Missing evidence can make a dimension not evaluable.

## Dimensions

The current baseline reports:

- goal alignment
- grounding/specificity
- actionability
- explanatory rationale
- feed-forward
- constructive framing
- learner agency
- reference alignment

Each dimension is reported separately.

## No default total

The main API intentionally returns no overall quality score.

A total could conceal serious failures, for example:

- highly actionable but wrong feedback
- correct but non-actionable feedback
- grounded but coercive feedback
- polite but generic feedback

Any future composite should require an explicit validated weighting model.

## Correctness boundary

The evaluator does not infer disciplinary correctness from feedback wording.

Reference alignment is:

- 2 when external reference evidence supports the feedback
- 0 when external reference evidence contradicts it
- not evaluable when reference evidence is missing or insufficient

The external verdict must come from a separate defensible reference process.

## Error flags

The baseline can identify transparent surface/context conditions such as:

- generic praise
- person-focused judgment
- vague criticism
- missing action
- missing next step
- weak grounding
- goal/rubric mismatch
- rationale without grounding
- certainty without reference evidence
- reference contradiction
- limited context

These are review prompts rather than definitive classifications.

## Human validation tools

Implemented:

- unweighted Cohen kappa
- linear weighted Cohen kappa
- quadratic weighted Cohen kappa
- exact agreement
- mean absolute error
- dimension-level comparison
- pairwise summaries for multiple rater sequences

The pairwise summary should not be described as a formal multi-rater reliability coefficient.

## Main limitations

The current baseline:

- relies on lexical overlap rather than semantic entailment
- has English-oriented cue lexicons
- uses hand-authored action/rationale/agency markers
- cannot verify domain facts
- cannot judge timing from text alone
- cannot measure learner uptake
- cannot establish instructional effectiveness
- does not estimate uncertainty statistically
- does not use learned models
- does not implement a validated multi-rater reliability coefficient
- does not produce a validated composite score

## Evidence needed before real use

A real study should include:

- precise rubric definitions
- trained raters
- double-rated or multi-rated corpus
- adjudicated reference examples
- discipline and task diversity
- multilingual validation where relevant
- adversarial heuristic testing
- per-dimension error analysis
- human review of high-risk contradictions
- learner uptake or revision outcomes if effectiveness is claimed

## Human oversight

Every output should remain inspectable.

A reviewer should be able to see:

- the supplied context
- the dimension score
- why the heuristic produced it
- the evidence trace
- flags
- whether reference alignment was actually evaluable

No score should be treated as a diagnosis of learner, instructor, or system quality.
