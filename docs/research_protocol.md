# Research protocol

## Project

Feedback Quality Evaluator

## Research questions

1. Can transparent text-and-context heuristics distinguish grounded, actionable formative feedback from generic or unsupported comments?
2. Which dimensions can be evaluated from text alone, and which require task, rubric, learner-work, or reference evidence?
3. How closely do automated dimension scores agree with trained human raters?
4. Which feedback patterns systematically fool surface heuristics?
5. How should feedback quality be evaluated without collapsing distinct strengths and failures into one opaque total?

## Theoretical framing

The repository is informed by established formative-feedback research.

Hattie and Timperley describe feedback as information that helps answer questions about the learning goal, current performance, and what comes next.

- Hattie, J., & Timperley, H. (2007).
- The Power of Feedback.
- Review of Educational Research, 77(1), 81–112.
- https://doi.org/10.3102/003465430298487

Shute's review emphasizes formative feedback that is supportive, specific, credible, and oriented toward improving learning.

- Shute, V. J. (2008).
- Focus on Formative Feedback.
- Review of Educational Research, 78(1), 153–189.
- https://doi.org/10.3102/0034654307313795

Nicol and Macfarlane-Dick frame good feedback as supporting learner self-regulation rather than simply transmitting judgments.

- Nicol, D. J., & Macfarlane-Dick, D. (2006).
- Formative assessment and self-regulated learning: a model and seven principles of good feedback practice.
- Studies in Higher Education, 31(2), 199–218.
- https://doi.org/10.1080/03075070600572090

Carless and Boud emphasize feedback literacy and learner uptake: feedback matters only when learners can make sense of it and act on it.

- Carless, D., & Boud, D. (2018).
- The development of student feedback literacy: enabling uptake of feedback.
- Assessment & Evaluation in Higher Education, 43(8), 1315–1325.
- https://doi.org/10.1080/02602938.2018.1463354

The current implementation does not claim to operationalize these theories completely. It uses them to define transparent research dimensions and boundaries.

## Structured feedback context

The primary API accepts a `FeedbackContext` with:

- feedback text
- task goal
- rubric criterion
- learner work
- identified issue
- supporting evidence
- expected standard
- external reference verdict

This structure prevents the evaluator from pretending that feedback quality can be judged from wording alone.

## Current dimensions

The evaluator reports each dimension separately on a 0–2 ordinal scale when it is evaluable.

### Goal alignment

Does the feedback visibly connect to the supplied goal, rubric criterion, or expected standard?

The current baseline uses transparent lexical overlap.

This is not semantic entailment.

### Grounding and specificity

Does the feedback point to concrete information in the supplied learner work, identified issue, or supporting evidence?

The baseline does **not** use word count as specificity.

### Actionability

Does the feedback contain an explicit action, and is that action linked to the task/work context?

### Explanatory rationale

Does the feedback give a reason, and is that reason grounded in supplied evidence rather than merely containing words such as "because"?

### Feed-forward

Does the feedback indicate a next action and, ideally, how to check, verify, or sequence it?

### Constructive framing

Does the feedback remain task/process focused rather than judging the learner as a person?

This is a limited lexical diagnostic, not a full tone model.

### Learner agency

Does the wording leave room for learner choice rather than using coercive or dismissive language?

Again, this is a surface-language baseline.

### Reference alignment

When an external reference verdict is supplied, does it support or contradict the feedback claim?

If external evidence is absent or insufficient, reference alignment is **not evaluable**.

The system does not infer disciplinary correctness from fluent wording.

## No overall score

The main evaluator intentionally sets:

`overall_score = None`

A feedback message can be:

- specific but wrong
- correct but non-actionable
- actionable but coercive
- constructive but ungrounded

A single total can hide those differences.

Any future composite should require an explicit, validated weighting rationale.

## Error taxonomy

The current baseline can flag:

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

These are review flags, not diagnoses of feedback quality.

## Revision suggestions

The system can generate targeted revision suggestions from the detected flags.

For example:

- point to the specific claim or step
- connect feedback to the criterion
- add a feasible action
- explain how the learner can verify the next step
- reduce certainty when reference evidence is missing

The tool does not automatically rewrite learner-facing feedback in the current baseline.

## Human validation

Human validation should occur by dimension.

For ordinal 0–2 ratings, the repository implements:

- exact agreement
- mean absolute error
- linear weighted Cohen kappa
- quadratic weighted Cohen kappa

It also provides pairwise summaries when more than two rater sequences are supplied.

The pairwise summary is **not** a multi-rater reliability coefficient and should not be described as one.

## Empirical study design

A real study should:

1. define each rubric dimension operationally
2. train raters using anchor examples
3. double-rate a sufficiently diverse sample
4. report agreement before adjudication
5. adjudicate disagreements for a reference set
6. evaluate each automated dimension separately
7. inspect false-positive and false-negative heuristic cases
8. test across disciplines, task types, languages, and feedback sources
9. evaluate feedback uptake or revision quality separately from text quality
10. pre-register any composite score before examining study results

## Adversarial evaluation

The current synthetic corpus deliberately tests cases that fool shallow heuristics:

- verbose but vague comments
- short but precise corrections
- "because" without evidence
- generic praise
- person-focused criticism
- confident but unsupported claims
- correct information with no next step
- actionable advice contradicted by reference evidence
- stylistic advice unrelated to the learning criterion

This kind of stress testing should remain part of future development.

## Threats to validity

Major threats include:

- lexical overlap being mistaken for semantic alignment
- action verbs appearing in irrelevant advice
- discipline-specific terminology
- indirect but useful feedback receiving low heuristic scores
- concise feedback being undervalued
- tone differing across cultures/languages
- reference answers being incomplete or wrong
- raters interpreting rubric anchors differently
- learner uptake depending on timing and prior knowledge
- feedback quality differing from feedback effectiveness
- AI-generated feedback optimizing for rubric keywords

The evaluator should therefore remain an inspectable research baseline rather than an autonomous judge.
