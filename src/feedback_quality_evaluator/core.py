import re

ACTION_VERBS = {
    "revise",
    "compare",
    "explain",
    "justify",
    "calculate",
    "identify",
    "add",
    "remove",
    "test",
    "check",
    "clarify",
}


def score_feedback(text: str, references_error: bool = False) -> dict[str, int]:
    """Score a short feedback message on transparent heuristic dimensions."""
    if not text.strip():
        raise ValueError("text must not be empty")
    words = re.findall(r"[a-z]+", text.lower())
    actionability = int(any(word in ACTION_VERBS for word in words))
    specificity = min(2, int(len(set(words)) >= 12) + int(references_error))
    evidence = int(
        any(marker in text.lower() for marker in ("because", "for example", "specifically", "evidence"))
    )
    return {
        "actionability": actionability,
        "specificity": specificity,
        "explanatory_evidence": evidence,
        "total": actionability + specificity + evidence,
    }


def cohen_kappa(labels_a, labels_b) -> float:
    """Return Cohen kappa for two equal length rating sequences."""
    if len(labels_a) != len(labels_b) or not labels_a:
        raise ValueError("ratings must be non-empty and have equal length")
    categories = sorted(set(labels_a) | set(labels_b), key=str)
    observed = sum(a == b for a, b in zip(labels_a, labels_b)) / len(labels_a)
    share_a = {category: labels_a.count(category) / len(labels_a) for category in categories}
    share_b = {category: labels_b.count(category) / len(labels_b) for category in categories}
    expected = sum(share_a[category] * share_b[category] for category in categories)
    return 1.0 if expected == 1.0 else (observed - expected) / (1 - expected)
