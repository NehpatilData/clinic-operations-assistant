
from src.safety_check import screen_for_potentially_urgent_language


def test_potentially_urgent_phrase_is_flagged():
    result = screen_for_potentially_urgent_language(
        "I am experiencing chest pain."
    )

    assert result["safety_flag"] is True
    assert result["requires_immediate_human_review"] is True


def test_non_matching_message_is_not_flagged():
    result = screen_for_potentially_urgent_language(
        "What time does the clinic close?"
    )

    assert result["safety_flag"] is False
    assert result["requires_immediate_human_review"] is False


def test_phrase_matching_is_case_insensitive():
    result = screen_for_potentially_urgent_language(
        "I HAVE CHEST PAIN."
    )

    assert result["safety_flag"] is True


def test_empty_message_is_handled():
    result = screen_for_potentially_urgent_language("")

    assert result["safety_flag"] is False
