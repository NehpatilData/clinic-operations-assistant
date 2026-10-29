# JSON Data Schema — Clinic Operations Assistant

## 1. Purpose

This document defines the structure of the data returned by the AI when processing a fictional clinic enquiry.

The schema helps Gemini, Python validation, and the database use consistent field names and data types.

## 2. Allowed Categories

The AI must select exactly one category from this list:

- `appointment_booking`
- `rescheduling`
- `cancellation`
- `clinic_information`
- `billing`
- `other`

The AI must not create additional categories.

## 3. AI Output Fields

| Field | Data type | Description |
|---|---|---|
| `category` | String | One of the six allowed categories |
| `preferred_date` | String or null | Explicitly stated calendar date in YYYY-MM-DD format, if known |
| `preferred_time` | String or null | Explicitly stated time or time preference |
| `summary` | String | Brief administrative summary of the enquiry |
| `missing_fields` | Array of strings | Names of required details that are missing |
| `needs_human_review` | Boolean | Indicates whether the result needs additional staff review |

## 4. Data Rules

1. Extract only information explicitly stated in the enquiry.
2. Never guess a date, time, appointment status, or other missing detail.
3. Use JSON `null` when a date or time is unknown.
4. Use `true` or `false` for Boolean values, not quoted strings.
5. Return exactly one approved category.
6. Use an empty array (`[]`) when no required fields are missing.
7. Keep the summary concise and administrative.
8. Do not provide medical advice or make clinical decisions.
9. The AI must not claim that an appointment has been booked, changed, or cancelled unless an authorized system confirms that action. This prototype does not perform those actions.
10. Python must validate the AI output before the application stores or uses it.

## 5. Example Input

"Hi, I would like to reschedule my appointment to Friday afternoon."

## 6. Example AI Output

{
  "category": "rescheduling",
  "preferred_date": null,
  "preferred_time": "afternoon",
  "summary": "The person wants to reschedule an appointment to Friday afternoon.",
  "missing_fields": ["preferred_date"],
  "needs_human_review": true
}

The calendar date is unknown because the message says Friday without specifying a date. The application must not invent one.

The human-review flag is true because staff must review the result before taking action.

## 7. Safety Handling

Safety flags are managed separately from the six categories.

A conservative safety pre-check runs before routine AI processing. If a configured safety rule triggers, routine processing and response drafting stop, and the request is directed to immediate human review under the fictional clinic procedure.

Keyword checks are only a limited safety measure. They may miss urgent messages or flag non-urgent ones and must not be treated as clinical triage.

## 8. Application Metadata

The application, rather than the AI, manages the following fields:

- `request_id`: unique identifier for the request.
- `original_message`: the submitted enquiry.
- `status`: current workflow state.
- `created_at`: time the request was recorded.
- `safety_flag`: result of the separate safety pre-check.
- `draft_reply`: proposed administrative response, if permitted and available.

These fields will be designed in more detail as part of the SQL Server table structure.

## 9. Validation Plan

Python will check:

- Required fields are present.
- The category belongs to the approved list.
- Dates follow the required format when supplied.
- Fields have the expected data types.
- Missing fields are represented as a list of strings.
- Boolean values are valid.
- Unexpected or invalid AI output is rejected safely.

## 10. Scope

This schema is for a fictional administrative prototype. It does not authorize real appointment changes, automatic message sending, medical advice, or clinical decisions.