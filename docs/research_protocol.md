# Research protocol

## Project

Feedback Quality Evaluator

## Questions

1. Which measurable properties distinguish useful formative feedback from generic comments?
2. How reliable are automated rubric scores against human ratings?
3. Where do AI feedback systems overstate correctness or actionability?

## Baseline methods

- action verb detection
- specificity heuristic
- evidence cue detection
- transparent composite score
- Cohen kappa

## Evidence to collect

Start from the current transparent baseline and record every transformation needed to produce dimension scores for actionability, specificity, explanatory evidence, and a total from 0 to 4. Keep a clear boundary between synthetic demonstration data and any future empirical dataset.

## Validation

Create a human rated reference set, report agreement and rubric reliability, then compare automated scores against each dimension separately. Inspect examples where a high automated score still produces poor instructional feedback.

## What counts as a useful result

A proper study needs a rubric, multiple trained raters, a diverse feedback set, and analysis of where the heuristic agrees or disagrees with human judgments. A learned model should only be added after that reference set exists.

## Threats to validity

Surface wording can look specific without being useful, raters may interpret rubric language differently, and feedback quality depends on task context and learner needs.
