
import json

from google import genai

from src.config import GEMINI_API_KEY

from src.safety_check import screen_for_potentially_urgent_language



def get_gemini_client():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "Gemini API key is not configured. Check your local .env file."
        )

    from google.genai import types

    return genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=1,
            )
        ),
    )



def test_gemini_connection():
    """Send a minimal test request to Gemini."""
    client = get_gemini_client()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Reply with exactly: Gemini connection successful",
    )

    return response.text

def analyze_clinic_enquiry(message):
    """Analyze a clinic enquiry and return structured information."""
    client = get_gemini_client()

    prompt = f"""
You are an administrative assistant for a fictional GP clinic in Australia.

Analyze the following patient enquiry for administrative purposes only.

Safety rules:
- Do not diagnose medical conditions or provide medical advice.
- Do not decide whether a patient needs urgent medical care.
- This function is not the clinic's safety screening system.
- Always require a human to review the result before any action.
- Never invent dates, times, or other patient details.
- Extract a date only when an unambiguous calendar date is provided.
- If a detail is missing or unclear, use null where appropriate.

Choose exactly one category from:
appointment_booking
rescheduling
cancellation
clinic_information
billing
other

Return a JSON object with these fields:
- category: one permitted category
- preferred_date: date in YYYY-MM-DD format or null
- preferred_time: time as a string or null
- summary: short summary of the enquiry
- missing_fields: array of missing information relevant to the request
- needs_human_review: always true

Patient enquiry:
{message}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        },
    )

    return json.loads(response.text)




def process_clinic_enquiry(message):
    """Screen an enquiry before deciding whether to call Gemini."""

    try:
        safety_result = screen_for_potentially_urgent_language(message)
    except Exception:
        return {
            "safety_flag": True,
            "requires_immediate_human_review": True,
            "matched_phrase": None,
            "ai_analysis": None,
            "processing_status": "safety_check_failed",
        }

    if safety_result["safety_flag"]:
        return {
            "safety_flag": True,
            "requires_immediate_human_review": True,
            "matched_phrase": safety_result["matched_phrase"],
            "ai_analysis": None,
            "processing_status": "immediate_human_review",
        }

    analysis = analyze_clinic_enquiry(message)

    return {
        "safety_flag": False,
        "requires_immediate_human_review": False,
        "matched_phrase": None,
        "ai_analysis": analysis,
        "processing_status": "pending_human_review",
    }


def generate_draft_reply(message, category, summary, missing_fields=None):
    """Generate a draft administrative reply for staff review."""

    safety_result = screen_for_potentially_urgent_language(message)

    if safety_result["safety_flag"]:
        return {
            "draft_reply": None,
            "needs_human_review": True,
            "processing_status": "immediate_human_review",
        }

    client = get_gemini_client()

    prompt = f"""
You are drafting an administrative reply for a fictional GP clinic
in Australia.

Write a brief, polite, professional response to the patient's enquiry.

Rules:
- This is an administrative draft only.
- Do not diagnose or provide medical advice.
- Do not promise an appointment, booking, cancellation, or refund.
- Do not invent clinic policies, fees, dates, times, or availability.
- If information is missing, ask the patient to provide it or say
  that clinic staff will confirm it.
- Do not claim that any action has already been completed.
- The reply must be reviewed by clinic staff before sending.
- Return only the draft reply text, not JSON or commentary.

Enquiry category: {category}
Enquiry summary: {summary}
Missing information: {json.dumps(missing_fields or [])}
Original patient enquiry:
{message}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return {
        "draft_reply": (response.text or "").strip() or None,
        "needs_human_review": True,
        "processing_status": "pending_human_review",
    }
