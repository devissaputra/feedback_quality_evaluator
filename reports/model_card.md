# Analytic system card

## System

Feedback Quality Evaluator

## Purpose

Heuristic evaluator for formative feedback specificity, actionability, explanatory evidence, and rater agreement.

## Current maturity

Working research prototype. The bundled example checks the software path with synthetic inputs. It does not establish validity for real learners, instructors, courses, or workplaces.

## Inputs

See `../data/README.md` for the current synthetic schema and the documentation expected before real data are connected.

## Outputs

The current code produces dimension scores for actionability, specificity, explanatory evidence, and a total from 0 to 4. These outputs are research signals and should be interpreted with the educational context that produced them.

## Evidence needed before real use

Create a human rated reference set, report agreement and rubric reliability, then compare automated scores against each dimension separately. Inspect examples where a high automated score still produces poor instructional feedback.

## Main limitation

The score is a transparent heuristic, not a validated measure of feedback quality. It cannot judge disciplinary accuracy, tone, timing, or whether a learner actually uses the feedback.

## Human oversight

A person must review any output before it can affect a learner, instructor, applicant, or employee.
