# Related work and theoretical context

Feedback Quality Evaluator is an original transparent implementation.

It does not reproduce the models or empirical results below.

## Hattie and Timperley: The Power of Feedback

Hattie and Timperley synthesize feedback research around questions concerning:

- the learning goal
- current progress/performance
- what should happen next

Reference:

- Hattie, J., & Timperley, H. (2007).
- *The Power of Feedback.*
- Review of Educational Research, 77(1), 81–112.
- https://doi.org/10.3102/003465430298487

This motivates the repository's explicit separation of goal alignment, current-work grounding, and feed-forward.

## Shute: Focus on Formative Feedback

Shute reviews formative feedback as information intended to change learner thinking or behavior in ways that improve learning, with attention to properties such as specificity, supportiveness, timing, and credibility.

Reference:

- Shute, V. J. (2008).
- *Focus on Formative Feedback.*
- Review of Educational Research, 78(1), 153–189.
- https://doi.org/10.3102/0034654307313795

This motivates the repository's rejection of generic praise and of length as a specificity proxy.

## Nicol and Macfarlane-Dick: feedback and self-regulation

Nicol and Macfarlane-Dick frame formative assessment and feedback as processes that can support self-regulated learning and learner control.

Reference:

- Nicol, D. J., & Macfarlane-Dick, D. (2006).
- *Formative assessment and self-regulated learning: a model and seven principles of good feedback practice.*
- Studies in Higher Education, 31(2), 199–218.
- https://doi.org/10.1080/03075070600572090

This is relevant to learner-agency and actionable next-step dimensions.

## Carless and Boud: feedback literacy

Carless and Boud emphasize that learners need capacities to appreciate feedback, make judgments, manage affective responses, and take action.

Reference:

- Carless, D., & Boud, D. (2018).
- *The development of student feedback literacy: enabling uptake of feedback.*
- Assessment & Evaluation in Higher Education, 43(8), 1315–1325.
- https://doi.org/10.1080/02602938.2018.1463354

This reinforces the distinction between feedback-text properties and actual learner uptake.

## Current scope

Implemented:

- structured feedback context
- goal/rubric alignment heuristic
- work/evidence grounding heuristic
- actionability
- explanatory-rationale check
- feed-forward check
- constructive-framing check
- learner-agency wording check
- externally supplied reference alignment
- not-evaluable states
- transparent error taxonomy
- revision suggestions
- unweighted Cohen kappa
- ordinal weighted Cohen kappa
- exact agreement
- mean absolute error
- dimension-level validation
- pairwise rater summaries

Not implemented:

- semantic embeddings
- LLM judging
- factual correctness inference
- disciplinary knowledge bases
- automated rubric extraction
- full tone or discourse modeling
- multilingual validation
- feedback-timing optimization
- learner uptake prediction
- causal effects of feedback
- multi-rater reliability coefficient such as Krippendorff alpha
- validated composite quality score

The current repository is best understood as an auditable formative-feedback rubric baseline for research and error analysis.
