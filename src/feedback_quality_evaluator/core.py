# Calculation reading guide: ../CALCULATIONS.md (repository root).
# Kappa = (observed agreement - chance agreement)/(1 - chance agreement).
# Constant identical ratings make chance agreement one and kappa undefined, not perfect. Lexical cues do not prove semantic grounding. Reference correctness is supplied externally; dimensions are not collapsed into a total quality score.

import math
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations
from numbers import Real


ACTION_VERBS = {
    "add",
    "calculate",
    "check",
    "clarify",
    "compare",
    "define",
    "describe",
    "explain",
    "identify",
    "justify",
    "label",
    "remove",
    "replace",
    "revise",
    "show",
    "summarize",
    "test",
    "verify",
}

RATIONALE_MARKERS = {
    "because",
    "since",
    "therefore",
    "so",
    "which means",
    "this matters",
    "for example",
}

NEXT_STEP_MARKERS = {
    "next",
    "then",
    "after",
    "before submitting",
    "before you submit",
    "check whether",
    "verify",
    "test",
    "try",
}

AGENCY_MARKERS = {
    "consider",
    "you could",
    "you might",
    "one option",
    "try",
    "would you",
    "if useful",
}

COERCIVE_MARKERS = {
    "you must",
    "obviously",
    "clearly you",
    "just do",
    "simply do",
}

CERTAINTY_MARKERS = {
    "definitely",
    "obviously",
    "clearly",
    "always",
    "never",
    "certainly",
    "proves",
}

GENERIC_PRAISE = {
    "good job",
    "great job",
    "well done",
    "excellent work",
    "nice work",
    "good work",
}

PERSON_JUDGMENTS = {
    "lazy",
    "careless",
    "weak student",
    "bad student",
    "smart",
    "stupid",
    "confused person",
    "not trying",
}

NEGATIVE_JUDGMENT_MARKERS = {
    "wrong",
    "bad",
    "weak",
    "poor",
    "incorrect",
}

REFERENCE_VERDICTS = {
    "supports",
    "contradicts",
    "insufficient",
    "not_provided",
}

DIMENSIONS = (
    "goal_alignment",
    "grounding_specificity",
    "actionability",
    "explanatory_rationale",
    "feed_forward",
    "constructive_framing",
    "learner_agency",
    "reference_alignment",
)

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "because",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "were",
    "with",
    "you",
    "your",
}


def _text(value, name, *, optional=False):
    if value is None and optional:
        return None
    if not isinstance(value, str) or not value.strip():
        if optional:
            raise ValueError(
                f"{name} must be a non-empty string or None"
            )
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _tokenize(text):
    if not text:
        return []
    return re.findall(r"[^\W_]+(?:['’-][^\W_]+)?", text.lower(), re.UNICODE)


def _content_tokens(text):
    return {
        token
        for token in _tokenize(text)
        if token not in STOPWORDS and len(token) >= 3
    }


def _phrase_present(text, phrases):
    lowered = text.lower()
    return any(phrase in lowered for phrase in phrases)


def _overlap_count(text, reference):
    return len(_content_tokens(text) & _content_tokens(reference))


def _dimension(score, rationale, *, evidence=None):
    if score not in (0, 1, 2):
        raise ValueError("dimension score must be 0, 1, or 2")
    return {
        "status": "scored",
        "score": score,
        "rationale": rationale,
        "evidence": [] if evidence is None else list(evidence),
    }


def _not_evaluable(rationale):
    return {
        "status": "not_evaluable",
        "score": None,
        "rationale": rationale,
        "evidence": [],
    }


@dataclass(frozen=True)
class FeedbackContext:
    """Structured context for transparent formative-feedback review."""

    feedback_text: str
    task_goal: str | None = None
    rubric_criterion: str | None = None
    learner_work: str | None = None
    identified_issue: str | None = None
    supporting_evidence: str | None = None
    expected_standard: str | None = None
    reference_verdict: str = "not_provided"

    def __post_init__(self):
        object.__setattr__(
            self,
            "feedback_text",
            _text(self.feedback_text, "feedback_text"),
        )
        for name in (
            "task_goal",
            "rubric_criterion",
            "learner_work",
            "identified_issue",
            "supporting_evidence",
            "expected_standard",
        ):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(
                    self,
                    name,
                    _text(value, name, optional=True),
                )

        if self.reference_verdict not in REFERENCE_VERDICTS:
            raise ValueError(
                "reference_verdict must be one of "
                f"{sorted(REFERENCE_VERDICTS)}"
            )


def _goal_alignment(context):
    references = [
        value
        for value in (
            context.task_goal,
            context.rubric_criterion,
            context.expected_standard,
        )
        if value
    ]
    if not references:
        return _not_evaluable(
            "No task goal, rubric criterion, or expected standard was supplied."
        )

    overlaps = [
        (reference, _overlap_count(context.feedback_text, reference))
        for reference in references
    ]
    positive = [item for item in overlaps if item[1] > 0]
    total_overlap = sum(count for _, count in overlaps)

    if total_overlap >= 2 or len(positive) >= 2:
        return _dimension(
            2,
            "Feedback contains multiple lexical links to the supplied goal/criterion context.",
            evidence=[f"overlap={count}" for _, count in positive],
        )
    if total_overlap == 1:
        return _dimension(
            1,
            "Feedback contains one lexical link to the supplied goal/criterion context.",
            evidence=["one contextual token overlap"],
        )
    return _dimension(
        0,
        "No lexical link to the supplied goal/criterion context was detected.",
    )


def _grounding_specificity(context):
    sources = [
        value
        for value in (
            context.learner_work,
            context.identified_issue,
            context.supporting_evidence,
        )
        if value
    ]
    if not sources:
        return _not_evaluable(
            "No learner work, identified issue, or supporting evidence was supplied."
        )

    issue_overlap = (
        _overlap_count(context.feedback_text, context.identified_issue)
        if context.identified_issue
        else 0
    )
    evidence_overlap = (
        _overlap_count(context.feedback_text, context.supporting_evidence)
        if context.supporting_evidence
        else 0
    )
    work_overlap = (
        _overlap_count(context.feedback_text, context.learner_work)
        if context.learner_work
        else 0
    )

    distinct_sources = sum(
        count > 0
        for count in (issue_overlap, evidence_overlap, work_overlap)
    )
    total = issue_overlap + evidence_overlap + work_overlap

    if distinct_sources >= 2 or total >= 3:
        return _dimension(
            2,
            "Feedback is anchored to multiple supplied details from the work or issue evidence.",
            evidence=[
                f"work_overlap={work_overlap}",
                f"issue_overlap={issue_overlap}",
                f"evidence_overlap={evidence_overlap}",
            ],
        )
    if total >= 1:
        return _dimension(
            1,
            "Feedback refers to at least one supplied detail, but grounding is limited.",
            evidence=[f"context_overlap={total}"],
        )
    return _dimension(
        0,
        "Feedback does not refer to the supplied work, issue, or evidence.",
    )


def _actionability(context):
    words = set(_tokenize(context.feedback_text))
    actions = sorted(words & ACTION_VERBS)
    if not actions:
        return _dimension(
            0,
            "No explicit next-action verb from the transparent action lexicon was detected.",
        )

    target_sources = [
        value
        for value in (
            context.identified_issue,
            context.rubric_criterion,
            context.expected_standard,
            context.learner_work,
        )
        if value
    ]
    targeted = any(
        _overlap_count(context.feedback_text, source) > 0
        for source in target_sources
    )

    if targeted:
        return _dimension(
            2,
            "Feedback contains an explicit action linked to supplied task/work context.",
            evidence=[f"action_verbs={','.join(actions)}"],
        )
    return _dimension(
        1,
        "Feedback contains an explicit action but the action is not clearly tied to supplied context.",
        evidence=[f"action_verbs={','.join(actions)}"],
    )


def _explanatory_rationale(context):
    marker = _phrase_present(context.feedback_text, RATIONALE_MARKERS)
    if not marker:
        return _dimension(
            0,
            "No explanatory connection marker was detected.",
        )

    grounding_sources = [
        value
        for value in (
            context.identified_issue,
            context.supporting_evidence,
            context.expected_standard,
            context.learner_work,
        )
        if value
    ]
    grounded = any(
        _overlap_count(context.feedback_text, source) > 0
        for source in grounding_sources
    )

    if grounded:
        return _dimension(
            2,
            "Feedback gives a reason and connects it to supplied work/evidence context.",
            evidence=["rationale marker + contextual overlap"],
        )
    return _dimension(
        1,
        "Feedback uses explanatory wording, but the rationale is not grounded in supplied evidence.",
        evidence=["rationale marker only"],
    )


def _feed_forward(context):
    has_action = bool(
        set(_tokenize(context.feedback_text)) & ACTION_VERBS
    )
    has_sequence = _phrase_present(
        context.feedback_text,
        NEXT_STEP_MARKERS,
    )

    if has_action and has_sequence:
        return _dimension(
            2,
            "Feedback contains both an action and an explicit next-step/verification cue.",
            evidence=["action + next-step cue"],
        )
    if has_action:
        return _dimension(
            1,
            "Feedback gives an action but little indication of how to verify or sequence the next step.",
            evidence=["action only"],
        )
    return _dimension(
        0,
        "No actionable feed-forward step was detected.",
    )


def _constructive_framing(context):
    lowered = context.feedback_text.lower()
    if _phrase_present(lowered, PERSON_JUDGMENTS):
        return _dimension(
            0,
            "Feedback includes person-focused judgment rather than task-focused information.",
            evidence=["person-focused judgment cue"],
        )

    generic_praise = any(
        phrase == lowered.rstrip(".!")
        or lowered.startswith(phrase + ".")
        for phrase in GENERIC_PRAISE
    )
    has_task_context = any(
        _overlap_count(context.feedback_text, value) > 0
        for value in (
            context.learner_work,
            context.identified_issue,
            context.rubric_criterion,
        )
        if value
    )
    negative = bool(
        set(_tokenize(context.feedback_text))
        & NEGATIVE_JUDGMENT_MARKERS
    )

    if generic_praise and not has_task_context:
        return _dimension(
            1,
            "Feedback is positive but generic and provides little task-focused information.",
            evidence=["generic praise"],
        )
    if negative and not has_task_context:
        return _dimension(
            1,
            "Feedback contains negative evaluation without clear task-grounded detail.",
            evidence=["ungrounded negative evaluation"],
        )
    return _dimension(
        2,
        "No person-focused judgment was detected and framing is task-oriented or neutral.",
    )


def _learner_agency(context):
    if _phrase_present(context.feedback_text, COERCIVE_MARKERS):
        return _dimension(
            0,
            "Feedback uses coercive or dismissive wording.",
            evidence=["coercive cue"],
        )
    if _phrase_present(context.feedback_text, AGENCY_MARKERS):
        return _dimension(
            2,
            "Feedback includes language that leaves room for learner choice or exploration.",
            evidence=["agency-supportive cue"],
        )
    return _dimension(
        1,
        "Feedback is directive or neutral without explicit coercion or learner choice.",
    )


def _reference_alignment(context):
    if context.reference_verdict == "supports":
        return _dimension(
            2,
            "External reference evidence was supplied as supporting the feedback claim.",
            evidence=["reference_verdict=supports"],
        )
    if context.reference_verdict == "contradicts":
        return _dimension(
            0,
            "External reference evidence was supplied as contradicting the feedback claim.",
            evidence=["reference_verdict=contradicts"],
        )
    return _not_evaluable(
        "Reference evidence is insufficient or was not supplied; disciplinary correctness is not inferred from wording."
    )


def evaluate_feedback(context: FeedbackContext):
    """Evaluate feedback by separate transparent dimensions; no total score."""
    if not isinstance(context, FeedbackContext):
        raise ValueError("context must be a FeedbackContext")

    dimensions = {
        "goal_alignment": _goal_alignment(context),
        "grounding_specificity": _grounding_specificity(context),
        "actionability": _actionability(context),
        "explanatory_rationale": _explanatory_rationale(context),
        "feed_forward": _feed_forward(context),
        "constructive_framing": _constructive_framing(context),
        "learner_agency": _learner_agency(context),
        "reference_alignment": _reference_alignment(context),
    }

    flags = feedback_flags(context, dimensions=dimensions)
    suggestions = revision_suggestions(
        context,
        dimensions=dimensions,
        flags=flags,
    )
    return {
        "dimensions": dimensions,
        "flags": flags,
        "revision_suggestions": suggestions,
        "overall_score": None,
        "overall_score_reason": (
            "Dimensions are intentionally not collapsed into a single quality score."
        ),
    }


def feedback_flags(context, *, dimensions=None):
    if not isinstance(context, FeedbackContext):
        raise ValueError("context must be a FeedbackContext")
    if dimensions is None:
        dimensions = {
            "goal_alignment": _goal_alignment(context),
            "grounding_specificity": _grounding_specificity(context),
            "actionability": _actionability(context),
            "explanatory_rationale": _explanatory_rationale(context),
            "feed_forward": _feed_forward(context),
            "constructive_framing": _constructive_framing(context),
            "learner_agency": _learner_agency(context),
            "reference_alignment": _reference_alignment(context),
        }

    flags = []
    lowered = context.feedback_text.lower()

    generic_only = any(
        lowered.rstrip(".!") == phrase
        for phrase in GENERIC_PRAISE
    )
    if generic_only:
        flags.append("generic_praise")

    if _phrase_present(lowered, PERSON_JUDGMENTS):
        flags.append("person_focused_judgment")

    if (
        set(_tokenize(lowered)) & NEGATIVE_JUDGMENT_MARKERS
        and dimensions["grounding_specificity"]["status"] == "scored"
        and dimensions["grounding_specificity"]["score"] == 0
    ):
        flags.append("vague_criticism")

    if dimensions["actionability"]["score"] == 0:
        flags.append("missing_action")

    if dimensions["feed_forward"]["score"] == 0:
        flags.append("missing_next_step")

    if (
        dimensions["grounding_specificity"]["status"] == "scored"
        and dimensions["grounding_specificity"]["score"] == 0
    ):
        flags.append("weak_grounding")

    if (
        dimensions["goal_alignment"]["status"] == "scored"
        and dimensions["goal_alignment"]["score"] == 0
    ):
        flags.append("goal_or_rubric_mismatch")

    if (
        dimensions["explanatory_rationale"]["score"] == 1
        and dimensions["grounding_specificity"]["status"] == "scored"
        and dimensions["grounding_specificity"]["score"] == 0
    ):
        flags.append("rationale_without_grounding")

    if (
        context.reference_verdict in {"not_provided", "insufficient"}
        and _phrase_present(lowered, CERTAINTY_MARKERS)
    ):
        flags.append("certainty_without_reference")

    if context.reference_verdict == "contradicts":
        flags.append("reference_contradiction")

    if (
        dimensions["goal_alignment"]["status"] == "not_evaluable"
        or dimensions["grounding_specificity"]["status"] == "not_evaluable"
    ):
        flags.append("limited_context")

    return sorted(set(flags))


def revision_suggestions(context, *, dimensions=None, flags=None):
    if not isinstance(context, FeedbackContext):
        raise ValueError("context must be a FeedbackContext")
    if dimensions is None:
        dimensions = evaluate_feedback(context)["dimensions"]
    if flags is None:
        flags = feedback_flags(context, dimensions=dimensions)

    suggestions = []
    if "generic_praise" in flags:
        suggestions.append(
            "Replace generic praise with a concrete observation about the learner's work."
        )
    if "person_focused_judgment" in flags:
        suggestions.append(
            "Rewrite person-focused judgment as task- or process-focused information."
        )
    if "weak_grounding" in flags:
        suggestions.append(
            "Point to the specific claim, step, evidence, or criterion that needs attention."
        )
    if "goal_or_rubric_mismatch" in flags:
        suggestions.append(
            "Connect the feedback explicitly to the stated goal, criterion, or expected standard."
        )
    if "missing_action" in flags:
        suggestions.append(
            "Add a feasible action the learner can take next."
        )
    if "missing_next_step" in flags:
        suggestions.append(
            "Explain how the learner can check, verify, or sequence the next step."
        )
    if "rationale_without_grounding" in flags:
        suggestions.append(
            "Ground the explanation in supplied evidence rather than relying on a reason marker alone."
        )
    if "certainty_without_reference" in flags:
        suggestions.append(
            "Reduce certainty or provide reference evidence before making a definitive correctness claim."
        )
    if "reference_contradiction" in flags:
        suggestions.append(
            "Recheck the feedback claim against the supplied reference evidence before presenting it to a learner."
        )
    return suggestions


def _validate_labels(labels_a, labels_b):
    if (
        not isinstance(labels_a, Sequence)
        or isinstance(labels_a, (str, bytes))
        or not isinstance(labels_b, Sequence)
        or isinstance(labels_b, (str, bytes))
    ):
        raise ValueError("ratings must be sequences")
    if len(labels_a) != len(labels_b) or not labels_a:
        raise ValueError(
            "ratings must be non-empty and have equal length"
        )


def cohen_kappa(labels_a, labels_b) -> float | None:
    """Return unweighted kappa, or None when chance agreement is one."""
    _validate_labels(labels_a, labels_b)
    categories = sorted(set(labels_a) | set(labels_b), key=str)
    observed = (
        sum(a == b for a, b in zip(labels_a, labels_b))
        / len(labels_a)
    )
    share_a = {
        category: labels_a.count(category) / len(labels_a)
        for category in categories
    }
    share_b = {
        category: labels_b.count(category) / len(labels_b)
        for category in categories
    }
    expected = sum(
        share_a[category] * share_b[category]
        for category in categories
    )
    return None if expected == 1.0 else (
        observed - expected
    ) / (1 - expected)


def weighted_cohen_kappa(
    labels_a,
    labels_b,
    *,
    weighting="quadratic",
):
    """Return weighted kappa; None means expected disagreement is zero."""
    _validate_labels(labels_a, labels_b)
    if weighting not in {"linear", "quadratic"}:
        raise ValueError(
            "weighting must be 'linear' or 'quadratic'"
        )

    all_labels = list(labels_a) + list(labels_b)
    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for value in all_labels
    ):
        raise ValueError(
            "weighted kappa requires integer ordinal ratings"
        )

    categories = sorted(set(all_labels))
    if len(categories) == 1:
        return None

    index = {
        category: position
        for position, category in enumerate(categories)
    }
    maximum_distance = len(categories) - 1

    def disagreement(a, b):
        distance = abs(index[a] - index[b]) / maximum_distance
        return (
            distance
            if weighting == "linear"
            else distance ** 2
        )

    observed = sum(
        disagreement(a, b)
        for a, b in zip(labels_a, labels_b)
    ) / len(labels_a)

    share_a = Counter(labels_a)
    share_b = Counter(labels_b)
    n = len(labels_a)
    expected = 0.0
    for category_a in categories:
        for category_b in categories:
            expected += (
                share_a[category_a] / n
                * share_b[category_b] / n
                * disagreement(category_a, category_b)
            )

    if expected == 0:
        return None
    return 1.0 - observed / expected


def exact_agreement(labels_a, labels_b):
    _validate_labels(labels_a, labels_b)
    return (
        sum(a == b for a, b in zip(labels_a, labels_b))
        / len(labels_a)
    )


def mean_absolute_error(values_a, values_b):
    _validate_labels(values_a, values_b)
    cleaned_a = [
        _finite_number(value, "rating")
        for value in values_a
    ]
    cleaned_b = [
        _finite_number(value, "rating")
        for value in values_b
    ]
    return sum(
        abs(a - b)
        for a, b in zip(cleaned_a, cleaned_b)
    ) / len(cleaned_a)


def dimension_validation(auto_scores, human_scores):
    """Compare 0-2 automated and human ordinal ratings for one dimension."""
    _validate_labels(auto_scores, human_scores)
    for sequence in (auto_scores, human_scores):
        for value in sequence:
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or value not in (0, 1, 2)
            ):
                raise ValueError(
                    "dimension ratings must be integers 0, 1, or 2"
                )

    return {
        "n": len(auto_scores),
        "exact_agreement": exact_agreement(
            auto_scores,
            human_scores,
        ),
        "mean_absolute_error": mean_absolute_error(
            auto_scores,
            human_scores,
        ),
        "weighted_kappa_linear": weighted_cohen_kappa(
            auto_scores,
            human_scores,
            weighting="linear",
        ),
        "weighted_kappa_quadratic": weighted_cohen_kappa(
            auto_scores,
            human_scores,
            weighting="quadratic",
        ),
    }


def pairwise_rater_summary(rater_scores):
    """Return pairwise ordinal agreement; not a multi-rater reliability coefficient."""
    if not isinstance(rater_scores, Mapping) or len(rater_scores) < 2:
        raise ValueError(
            "rater_scores must contain at least two raters"
        )
    names = sorted(rater_scores)
    lengths = {len(rater_scores[name]) for name in names}
    if len(lengths) != 1 or not lengths or next(iter(lengths)) == 0:
        raise ValueError(
            "all raters must provide equal non-empty rating sequences"
        )

    pairs = []
    for first, second in combinations(names, 2):
        ratings_a = rater_scores[first]
        ratings_b = rater_scores[second]
        pairs.append(
            {
                "rater_a": first,
                "rater_b": second,
                "exact_agreement": exact_agreement(
                    ratings_a,
                    ratings_b,
                ),
                "weighted_kappa_quadratic": weighted_cohen_kappa(
                    ratings_a,
                    ratings_b,
                    weighting="quadratic",
                ),
            }
        )
    return {
        "raters": names,
        "pair_count": len(pairs),
        "pairs": pairs,
    }


# Backward-compatible wrapper from the original prototype.
def score_feedback(text: str, references_error: bool = False):
    """Legacy 0-4 view. Prefer evaluate_feedback() for research use."""
    issue = "identified error" if references_error else None
    context = FeedbackContext(
        feedback_text=text,
        identified_issue=issue,
    )
    result = evaluate_feedback(context)
    dimensions = result["dimensions"]

    actionability = min(
        1,
        dimensions["actionability"]["score"],
    )
    specificity_score = dimensions["grounding_specificity"]["score"]
    if specificity_score is None:
        specificity = 0
    else:
        specificity = specificity_score
    evidence = min(
        1,
        dimensions["explanatory_rationale"]["score"],
    )

    return {
        "actionability": actionability,
        "specificity": specificity,
        "explanatory_evidence": evidence,
        "total": actionability + specificity + evidence,
        "legacy_heuristic": True,
    }
