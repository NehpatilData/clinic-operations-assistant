from src.validation import is_valid_category, is_valid_status

print(is_valid_category("billing"))
print(is_valid_category("rescheduling"))
print(is_valid_category("appointment_change"))
print(is_valid_category(None))
print(is_valid_category(123))

 

print(is_valid_status("new"))
print(is_valid_status("in_progress"))
print(is_valid_status("completed"))
print(is_valid_status("pending"))
print(is_valid_status(None))

from src.validation import has_required_fields

complete_data = {
    "category": "rescheduling",
    "preferred_date": None,
    "preferred_time": "afternoon",
    "summary": "The person wants to reschedule an appointment.",
    "missing_fields": ["preferred_date"],
    "needs_human_review": True,
}

incomplete_data = {
    "category": "rescheduling",
    "summary": "The person wants to reschedule an appointment.",
}

print(has_required_fields(complete_data))
print(has_required_fields(incomplete_data))

from src.validation import is_valid_review_flag

print(is_valid_review_flag(True))
print(is_valid_review_flag(False))
print(is_valid_review_flag("yes"))
print(is_valid_review_flag(1))
print(is_valid_review_flag(None))

from src.validation import is_valid_summary

print(is_valid_summary("The person wants to reschedule an appointment."))
print(is_valid_summary(""))
print(is_valid_summary("   "))
print(is_valid_summary(123))
print(is_valid_summary(None))

from src.validation import is_valid_missing_fields

print(is_valid_missing_fields(["preferred_date"]))
print(is_valid_missing_fields([]))
print(is_valid_missing_fields("preferred_date"))
print(is_valid_missing_fields(["preferred_date", 123]))
print(is_valid_missing_fields(None))

from src.validation import is_valid_preferred_date

print(is_valid_preferred_date("2026-11-05"))
print(is_valid_preferred_date(None))
print(is_valid_preferred_date("05-11-2026"))
print(is_valid_preferred_date("2026-02-30"))
print(is_valid_preferred_date(123))

from src.validation import is_valid_preferred_time

print(is_valid_preferred_time("afternoon"))
print(is_valid_preferred_time("10:30 AM"))
print(is_valid_preferred_time(None))
print(is_valid_preferred_time(""))
print(is_valid_preferred_time("   "))
print(is_valid_preferred_time(123))

def test_is_valid_category():
    assert is_valid_category("billing") is True
    assert is_valid_category("rescheduling") is True
    assert is_valid_category("appointment_change") is False
    assert is_valid_category(None) is False

def test_is_valid_status():
    assert is_valid_status("new") is True
    assert is_valid_status("in_progress") is True
    assert is_valid_status("completed") is True
    assert is_valid_status("pending") is False
    assert is_valid_status(None) is False


def test_has_required_fields():
    complete_data = {
        "category": "rescheduling",
        "preferred_date": None,
        "preferred_time": "afternoon",
        "summary": "The person wants to reschedule an appointment.",
        "missing_fields": ["preferred_date"],
        "needs_human_review": True,
    }

    incomplete_data = {
        "category": "rescheduling",
        "summary": "The person wants to reschedule an appointment.",
    }

    assert has_required_fields(complete_data) is True
    assert has_required_fields(incomplete_data) is False

def test_is_valid_review_flag():
    assert is_valid_review_flag(True) is True
    assert is_valid_review_flag(False) is True
    assert is_valid_review_flag("yes") is False
    assert is_valid_review_flag(1) is False
    assert is_valid_review_flag(None) is False

def test_is_valid_summary():
    assert is_valid_summary("The person wants to reschedule an appointment.") is True
    assert is_valid_summary("") is False
    assert is_valid_summary("   ") is False
    assert is_valid_summary(123) is False
    assert is_valid_summary(None) is False


def test_is_valid_missing_fields():
    assert is_valid_missing_fields(["preferred_date"]) is True
    assert is_valid_missing_fields([]) is True
    assert is_valid_missing_fields("preferred_date") is False
    assert is_valid_missing_fields(["preferred_date", 123]) is False
    assert is_valid_missing_fields(None) is False

def test_is_valid_preferred_date():
    assert is_valid_preferred_date("2026-11-05") is True
    assert is_valid_preferred_date(None) is True
    assert is_valid_preferred_date("05-11-2026") is False
    assert is_valid_preferred_date("2026-02-30") is False
    assert is_valid_preferred_date(123) is False


def test_is_valid_preferred_time():
    assert is_valid_preferred_time("afternoon") is True
    assert is_valid_preferred_time("10:30 AM") is True
    assert is_valid_preferred_time(None) is True
    assert is_valid_preferred_time("") is False
    assert is_valid_preferred_time("   ") is False
    assert is_valid_preferred_time(123) is False

from src.validation import (
    is_valid_category,
    is_valid_review_flag,
    is_valid_summary,
    is_valid_missing_fields,
    is_valid_preferred_date,
    is_valid_preferred_time,
)


def test_gemini_result_fields_are_valid():
    result = {
        "category": "rescheduling",
        "preferred_date": None,
        "preferred_time": "afternoon",
        "summary": "Patient requests an appointment reschedule.",
        "missing_fields": ["specific_date"],
        "needs_human_review": True,
    }

    assert is_valid_category(result["category"])
    assert is_valid_review_flag(result["needs_human_review"])
    assert is_valid_summary(result["summary"])
    assert is_valid_missing_fields(result["missing_fields"])
    assert is_valid_preferred_date(result["preferred_date"])
    assert is_valid_preferred_time(result["preferred_time"])
