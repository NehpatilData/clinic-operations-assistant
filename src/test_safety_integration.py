
from unittest.mock import patch

from src.gemini_service import (
    process_clinic_enquiry,
    generate_draft_reply,
)


def test_urgent_enquiry_bypasses_gemini():
    with patch(
        "src.gemini_service.screen_for_potentially_urgent_language",
        return_value={
            "safety_flag": True,
            "matched_phrase": "test urgent phrase",
        },
    ), patch(
        "src.gemini_service.analyze_clinic_enquiry"
    ) as mock_analysis:
        result = process_clinic_enquiry(
            "This is a test urgent enquiry."
        )

    assert result["safety_flag"] is True
    assert result["processing_status"] == "immediate_human_review"
    assert result["ai_analysis"] is None
    mock_analysis.assert_not_called()


def test_safety_screening_error_fails_safely():
    with patch(
        "src.gemini_service.screen_for_potentially_urgent_language",
        side_effect=RuntimeError("Simulated screening failure"),
    ), patch(
        "src.gemini_service.analyze_clinic_enquiry"
    ) as mock_analysis:
        result = process_clinic_enquiry(
            "This is a test enquiry."
        )

    assert result["safety_flag"] is True
    assert result["processing_status"] == "safety_check_failed"
    assert result["ai_analysis"] is None
    assert result["requires_immediate_human_review"] is True
    mock_analysis.assert_not_called()


def test_urgent_enquiry_cannot_generate_routine_draft():
    with patch(
        "src.gemini_service.screen_for_potentially_urgent_language",
        return_value={
            "safety_flag": True,
            "matched_phrase": "test urgent phrase",
        },
    ), patch(
        "src.gemini_service.get_gemini_client"
    ) as mock_client:
        result = generate_draft_reply(
            message="This is a test urgent enquiry.",
            category="other",
            summary="Test enquiry",
        )

    assert result["draft_reply"] is None
    assert result["needs_human_review"] is True
    assert result["processing_status"] == "immediate_human_review"
    mock_client.assert_not_called()
