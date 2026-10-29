# AI-Powered Clinic Operations Assistant

## Project Overview

The AI-Powered Clinic Operations Assistant is a Python application
designed to help clinic staff organize administrative enquiries.

It uses **Streamlit** for the user interface, **Google Gemini** for
administrative enquiry analysis and draft replies, and **Microsoft SQL
Server** for persistent data storage.

A keyword-based safety screen checks messages for configured potentially
urgent phrases before routine AI processing. Flagged enquiries are
routed to a human-review workflow.

> **Important:** This is a fictional clinic workflow prototype. It is
> not a medical device, diagnostic system, or clinically validated
> triage solution.

## Key Features

-   **Enquiry submission:** Capture administrative enquiries through a
    Streamlit interface.
-   **AI-powered analysis:** Classify enquiries, summarize messages,
    identify missing information, and extract explicitly stated
    preferred dates or times.
-   **Safety screening:** Check messages for configured potentially
    urgent phrases before routine AI processing.
-   **Human-review workflow:** Flag enquiries requiring human review and
    display warnings.
-   **SQL Server integration:** Persist enquiry records and retrieve
    enquiry history.
-   **Status management:** Update enquiry statuses as staff process
    requests.
-   **Follow-up management:** Record follow-up statuses and notes.
-   **Draft reply management:** Generate and save administrative reply
    drafts for staff review.
-   **Automated testing:** Use `pytest` to test core functionality and
    safety-related behavior.

## Technology Stack

-   Python
-   Streamlit
-   Google Gemini API (`google-genai`)
-   Microsoft SQL Server Express
-   `pyodbc`
-   `python-dotenv`
-   `pytest`
-   ODBC Driver 18 for SQL Server

## Project Structure

The structure below reflects the latest project layout shared during
development, including the new `src/ui/` modules and the separate
`tests/` directory. Check the exact filenames in VS Code and adjust any
name that differs locally.

``` text
clinic-operations-assistant/
├── app.py
├── README.md
├── requirements.txt              # Ensure this file exists and is current
├── .env.example
├── .gitignore
├── data/
│   └── sample_messages.csv
├── docs/
│   ├── data_schema.md
│   └── database_design.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── gemini_service.py
│   ├── safety_check.py
│   ├── validation.py
│   └── ui/
│       ├── __init__.py
│       ├── enquiry_form.py
│       ├── enquiry_history.py
│       ├── status_management.py
│       ├── follow_up_management.py
│       └── draft_reply_management.py
└── tests/
    ├── test_db_connection.py
    ├── test_gemini.py
    ├── test_review_timestamp.py
    ├── test_safety_check.py
    ├── test_safety_integration.py
    └── test_validation.py
```

**Notes about the structure:**

-   `app.py` is the Streamlit entry point that brings together the UI
    modules.
-   `src/ui/` contains functions for the individual interface sections,
    keeping `app.py` smaller and easier to maintain.
-   `src/database.py` contains SQL Server connection and data-access
    functions.
-   `src/gemini_service.py` contains Gemini-based enquiry analysis and
    draft-generation logic.
-   `src/safety_check.py` contains the keyword-based safety screen.
-   `src/validation.py` contains validation helpers.
-   `tests/` contains automated tests. Test modules should remain
    separate from production modules.
-   `docs/` contains the database schema and design documentation.
-   `.venv/`, `__pycache__/`, and `.pytest_cache/` are generated/local
    folders and should not be committed to Git.

## Prerequisites

Before running the application, install or configure:

-   Python compatible with the project's dependencies
-   Microsoft SQL Server Express
-   ODBC Driver 18 for SQL Server
-   A Google Gemini API key
-   Visual Studio Code or another Python development environment

## Setup and Installation

### 1. Open the project directory

Open a terminal in the project root, `clinic-operations-assistant/`.

### 2. Create a virtual environment

``` powershell
python -m venv .venv
```

### 3. Activate the virtual environment

``` powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

Ensure `requirements.txt` lists the project's direct dependencies, then
run:

``` powershell
python -m pip install -r requirements.txt
```

If `requirements.txt` has not yet been created, create and verify it
before using this command.

### 5. Configure environment variables

Copy `.env.example` to `.env`, then replace the placeholder with your
own Gemini API key.

Example `.env` format:

``` text
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit `.env` or expose your API key publicly. Keep `.env.example`
limited to placeholder values.

### 6. Configure the database

The current local connection configuration targets:

-   **SQL Server instance:** `localhost\SQLEXPRESS`
-   **Database:** `ClinicOperationsDB`
-   **Authentication:** Windows Trusted Connection
-   **ODBC driver:** ODBC Driver 18 for SQL Server

Create the database and required table using the project's database
schema documentation before starting the application. Adjust the
connection configuration if your SQL Server instance differs.

The current local configuration includes `TrustServerCertificate=yes`;
review certificate validation and connection security before using any
non-local environment.

### 7. Run the application

From the project root, with the virtual environment activated:

``` powershell
python -m streamlit run app.py
```

Open the local URL printed in the terminal, usually
`http://localhost:8501`.

## Running Tests

Run the automated test suite from the project root:

``` powershell
python -m pytest -q
```

During development, the suite completed with **17 passed tests** and one
dependency deprecation warning. Results may change after code,
environment, or dependency updates.

Some tests may require local SQL Server configuration or external API
credentials. Review individual test files before running tests in a new
environment.

## Safety and Human Review

The safety-screening module checks for configured potentially urgent
phrases before routine AI processing.

When a configured phrase is detected, the application is designed to:

1.  Flag the enquiry.
2.  Skip routine AI analysis.
3.  Save the enquiry for staff review, when database persistence
    succeeds.
4.  Mark human review as required.
5.  Display a human-review warning.
6.  Block routine draft generation for safety-flagged enquiries.

The screening uses simple keyword matching. It may miss urgent messages
expressed in different words and may flag benign text, including
negations or hypothetical examples. It is not clinically validated and
must not replace professional judgment, the clinic's established safety
procedures, or emergency protocols.

## Responsible AI Use

-   Use fictional or appropriately authorized data during development
    and testing.
-   Do not use AI-generated content as a diagnosis or treatment
    recommendation.
-   Treat classifications, summaries, extracted information, and draft
    replies as suggestions requiring staff oversight.
-   Review draft replies before sending them.
-   Do not assume an appointment, refund, or other action has occurred
    unless authorized staff have verified it.
-   Protect API keys, personal information, and database credentials.

## Current Limitations

-   Safety screening is keyword-based and is not clinically validated.
-   AI-generated classifications, summaries, and drafts may be
    inaccurate.
-   Draft replies require staff review before use.
-   The application is a prototype, not a production-ready clinical
    system.
-   Production deployment would require additional security, privacy,
    access-control, monitoring, reliability, and operational testing.
-   The local SQL Server Express connection is not directly usable from
    a cloud host without a reachable, securely configured database.

## Future Improvements

-   Add authentication and role-based access control.
-   Expand automated tests for database and interface workflows.
-   Improve safety-screening coverage and validation with appropriate
    expert review.
-   Add structured logging and error monitoring.
-   Verify dependency management and deployment configuration.
-   Improve reporting and enquiry-volume analytics.
-   Define data-retention, backup, and recovery procedures.

## Project Status

The core workflows have been exercised during development, including
enquiry analysis, database persistence, status updates, follow-up
management, and handling of safety-flagged enquiries.

The automated test suite previously completed with 17 passing tests.
Further testing, documentation verification, and deployment hardening
are needed before production use.

## Disclaimer

This project is intended for educational and administrative workflow
demonstration purposes only. It does not provide medical advice,
diagnose conditions, or replace qualified healthcare professionals.
