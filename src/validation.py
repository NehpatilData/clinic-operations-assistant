ALLOWED_CATEGORIES = {
    "appointment_booking",
    "rescheduling",
    "cancellation",
    "clinic_information",
    "billing",
    "other",
}
def is_valid_category(category):
    """Return True if category is an approved string."""
    if not isinstance(category, str):
        return False

    return category in ALLOWED_CATEGORIES

ALLOWED_STATUSES = {
    "new",
    "awaiting_information",
    "in_progress",
    "completed",
}


def is_valid_status(status):
    """Return True if status is an approved string."""
    if not isinstance(status, str):
        return False

    return status in ALLOWED_STATUSES

REQUIRED_FIELDS = {
    "category",
    "preferred_date",
    "preferred_time",
    "summary",
    "missing_fields",
    "needs_human_review",
}


def has_required_fields(data):
    """Return True if all required fields are present."""
    if not isinstance(data, dict):
        return False

    return REQUIRED_FIELDS.issubset(data.keys())

def is_valid_review_flag(value):
    """Return True only if the value is a Boolean."""
    return isinstance(value, bool)

def is_valid_summary(summary):
    """Return True if the summary is a non-empty string."""
    if not isinstance(summary, str):
        return False

    return bool(summary.strip())

def is_valid_missing_fields(missing_fields):
    """Return True if missing_fields is a list of strings."""
    if not isinstance(missing_fields, list):
        return False

    return all(isinstance(field, str) for field in missing_fields)

from datetime import date


def is_valid_preferred_date(value):
    """Return True if the value is None or a real YYYY-MM-DD date."""
    if value is None:
        return True

    if not isinstance(value, str):
        return False

    try:
        parsed_date = date.fromisoformat(value)
        return parsed_date.isoformat() == value
    except ValueError:
        return False

def is_valid_preferred_time(value):
    """Return True if the value is None or a non-empty string."""
    if value is None:
        return True

    if not isinstance(value, str):
        return False

    return bool(value.strip())