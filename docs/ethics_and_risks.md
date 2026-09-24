# Ethics, safety, and misuse risks

## Intended use

Feedback Quality Evaluator is a research and instructional-design prototype for inspecting feedback properties.

It should not be used as an autonomous judge of teachers, learners, employees, or AI systems.

## Feedback quality is contextual

A message that looks polished can still be wrong, irrelevant, mistimed, or unusable.

Likewise, a short message can be highly useful when it points precisely to an error and a next step.

The system therefore must not equate:

- length with specificity
- confidence with correctness
- politeness with pedagogical usefulness
- presence of "because" with a valid explanation
- action verbs with appropriate action
- rubric keywords with genuine alignment

## Disciplinary correctness

The current implementation does not infer factual correctness.

Reference alignment is only scored when an external reference verdict is supplied.

That verdict should come from defensible evidence such as:

- validated answer key
- verified calculation
- expert adjudication
- task/rubric reference
- authoritative source

If evidence is missing or insufficient, correctness-related evaluation should remain **not evaluable**.

## Risk of confidently wrong feedback

Incorrect feedback can actively harm learning.

A system that produces fluent but unsupported advice should not receive a high overall "quality" score merely because its wording is specific and actionable.

This is one reason the current implementation does not compute a default composite score.

## Person-focused judgment

Feedback should focus on work, strategy, evidence, or process rather than labeling the learner.

The baseline flags a small lexical set of person-focused judgments.

A real study needs broader language and cultural validation.

## Learner agency

Overly directive feedback can reduce opportunities for judgment and self-regulation.

The current agency dimension looks for limited lexical indicators of choice or coercion.

It is not a complete measure of autonomy support.

## Feedback uptake

Text quality is not the same as feedback effectiveness.

A learner may:

- ignore feedback
- misunderstand it
- disagree with it
- lack time to act
- lack prerequisite knowledge
- revise successfully
- revise in an unintended way

A real intervention study should measure uptake and revision separately.

## Privacy

Feedback text and learner work can contain identifiable educational records.

Do not publish or commit:

- named submissions
- private instructor comments
- grades
- accommodations
- health/disability information
- private messages
- licensed assessment items
- restricted institutional feedback
- proprietary learner data

Use de-identification and approved storage for real studies.

## Evaluating instructors or AI systems

Do not use the heuristic as a hidden performance-management score.

If used to study instructors, tutors, or AI feedback systems:

- disclose the evaluation dimensions
- retain the original feedback examples
- allow human review
- report uncertainty and disagreement
- avoid ranking people or systems from one aggregate score

## Linguistic and cultural bias

The current lexical rules are English-oriented even though tokenization supports Unicode.

Action, agency, tone, and explanation cues may differ across languages and cultures.

Do not generalize scores to other languages without separate validation.

## Excluded uses

Do not use this prototype alone for:

- grading learners
- instructor performance decisions
- employment decisions
- admissions
- disciplinary decisions
- automated teacher ranking
- deciding whether an AI system is "safe"
- psychological or personality assessment
- covert monitoring

## Before real deployment or research use

Document:

- rubric definitions
- reference-evidence process
- rater training
- adjudication
- language and discipline
- human review
- privacy controls
- known heuristic failure modes
- feedback timing
- learner uptake measures
- appeal/correction procedure

The evaluator should support careful review, not replace educational judgment.
