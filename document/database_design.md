# SQL Server Database Design

## 1. Purpose

The database stores fictional clinic enquiries and their processing results so that requests can be retrieved and tracked after the application restarts.

## 2. Proposed Table

Table name: `clinic_requests`

Each row represents one administrative enquiry.

## 3. Proposed Columns

| Column | SQL Server Type | Purpose |
|---|---|---|
| request_id | INT IDENTITY PRIMARY KEY | Unique automatically generated request identifier |
| original_message | NVARCHAR(MAX) | Original enquiry text |
| category | VARCHAR(30) | One of the six approved categories |
| preferred_date | DATE NULL | Explicitly known calendar date, if available |
| preferred_time | NVARCHAR(50) NULL | Explicit time or time preference |
| summary | NVARCHAR(500) | Brief administrative summary |
| missing_fields_json | NVARCHAR(MAX) | JSON array containing missing field names |
| status | VARCHAR(30) | Current administrative workflow status |
| safety_flag | BIT | Indicates whether the safety pre-check triggered |
| needs_human_review | BIT | Indicates whether staff review is required |
| draft_reply | NVARCHAR(MAX) NULL | Proposed response for staff review, if permitted |
| created_at | DATETIME2 | Time the request was recorded |

## 4. Allowed Categories

- appointment_booking
- rescheduling
- cancellation
- clinic_information
- billing
- other

## 5. Allowed Statuses

- new
- awaiting_information
- in_progress
- completed

## 6. Design Decisions

1. SQL Server generates a unique numeric request ID.
2. The original enquiry is retained so staff can compare the AI output with the submitted message.
3. Date and time values remain empty when they are not explicitly known.
4. The missing fields are stored as a JSON array.
5. Safety flags are separate from the enquiry category.
6. The application validates categories and statuses before saving records.
7. SQL queries will use parameters rather than inserting user input directly into query strings.
8. Routine response drafts require human approval and are not sent automatically.
9. Only fictional enquiries and fictional clinic policies will be used.

## 7. Initial Scope

This design describes one table for the first prototype. Separate audit-history, user-account, and clinic-policy tables may be considered later if the working application requires them.

The table design must be reviewed and tested before implementation.