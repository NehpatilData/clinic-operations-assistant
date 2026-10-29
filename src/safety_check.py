
"""Basic keyword-based safety screening for a fictional clinic workflow."""

# Illustrative phrases for testing only, not a clinically validated list.
POTENTIALLY_URGENT_PHRASES = [
    "chest pain",
    "difficulty breathing",
    "can't breathe",
    "cannot breathe",
    "severe bleeding",
    "unconscious",
    "suicidal",
    "want to kill myself",
]


def screen_for_potentially_urgent_language(message):
    """Flag configured phrases for immediate human review."""
    if not isinstance(message, str) or not message.strip():
        return {
            "safety_flag": False,
            "requires_immediate_human_review": False,
            "matched_phrase": None,
        }

    normalized_message = message.casefold()

    for phrase in POTENTIALLY_URGENT_PHRASES:
        if phrase in normalized_message:
            return {
                "safety_flag": True,
                "requires_immediate_human_review": True,
                "matched_phrase": phrase,
            }

    return {
        "safety_flag": False,
        "requires_immediate_human_review": False,
        "matched_phrase": None,
    }
