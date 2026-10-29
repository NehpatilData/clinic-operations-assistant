# AI-Powered Clinic Operations Assistant

## Project Overview

The AI-Powered Clinic Operations Assistant is a Python-based application designed to help clinic staff manage administrative enquiries more efficiently.

The application uses Streamlit for its user interface, Google Gemini for administrative enquiry analysis and draft replies, and Microsoft SQL Server for persistent data storage.

It includes keyword-based safety screening to identify potentially urgent language and route flagged enquiries for immediate human review.

**Important:** This is a fictional clinic workflow prototype. It is not a medical device, a diagnostic system, or a clinically validated triage solution.

## Key Features

- **Enquiry submission:** Capture administrative enquiries through a Streamlit interface.
- **AI-powered analysis:** Classify enquiries, summarize messages, identify missing information, and extract explicitly stated preferred dates or times.
- **Safety screening:** Check messages for configured potentially urgent phrases before routine AI processing.
- **Human-review workflow:** Flag enquiries that require human review and display appropriate warnings.
- **SQL Server integration:** Persist enquiry records and retrieve enquiry history.
- **Status management:** Update enquiry statuses as staff process requests.
- **Follow-up management:** Record follow-up statuses and notes.
- **Draft reply management:** Generate and save administrative reply drafts for staff review.
- **Automated testing:** Use pytest to validate core functionality and safety-related behavior.

## Technology Stack

- Python
- Streamlit
- Google Gemini API
- Microsoft SQL Server Express
- pyodbc
- pytest
- ODBC Driver 18 for SQL Server

## Project Structure

```text
clinic-operations-assistant/
├── app.py
├── .env.example
├── .gitignore
├── data/
│   └── sample_messages.csv
├── document/
│   ├── database_design.md
│   └── data_schema.md
└── src/
    ├── config.py
    ├── database.py
    ├── gemini_service.py
    ├── safety_check.py
    ├── test_db_connection.py
    ├── test_gemini.py
    ├── test_review_timestamp.py
    ├── test_safety_check.py
    ├── test_safety_integration.py
    ├── test_validation.py
    └── validation.py
```

## Prerequisites

Install or configure the following before running the application:

- Python compatible with the installed dependencies
- Microsoft SQL Server Express
- ODBC Driver 18 for SQL Server
- A Google Gemini API key
- Visual Studio Code or another Python development environment

## Setup and Installation

### 1. Clone or download the project

Open a terminal in the project directory.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

Install the packages required by the project. If a `requirements.txt` file is available, use:

```powershell
python -m pip install -r requirements.txt
```

If that file has not yet been created, prepare one from the project's actual dependencies before using this command.

### 5. Configure environment variables

Copy `.env.example` to `.env` and replace the placeholder with your own Gemini API key.

Example `.env` format:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit `.env` or expose your API key publicly.

### 6. Configure the database

The current local database connection is configured for:

- SQL Server instance: `localhost\SQLEXPRESS`
- Database: `ClinicOperationsDB`
- Authentication: Windows Trusted Connection
- ODBC driver: ODBC Driver 18 for SQL Server

Create the database and required tables using the project's database design and schema documentation before starting the application.

The connection settings may need to be adjusted for a different SQL Server instance.

### 7. Run the application

From the project root, activate the virtual environment and run:

```powershell
python -m streamlit run app.py
```

Open the local URL printed in the terminal, usually `http://localhost:8501`.

## Running Tests

Run the complete automated test suite from the project root:

```powershell
python -m pytest -q
```

During development, the suite completed with **17 passed tests** and one dependency deprecation warning.

Test results may vary after code or dependency changes.

## Safety and Human Review

The safety screening module checks for a configured list of potentially urgent phrases before routine AI processing.

When a configured phrase is detected, the application is designed to:

1. Flag the enquiry.
2. Skip routine AI analysis.
3. Save the enquiry for staff review.
4. Mark human review as required.
5. Display an immediate human-review warning.
6. Block routine draft generation for safety-flagged enquiries.

The current screening uses simple keyword matching. It may miss urgent messages expressed in different words and may flag phrases used in negations or hypothetical examples.

It is not clinically validated and must not replace professional judgment, established clinic safety procedures, or emergency protocols.

## Responsible AI Use

- Use fictional or appropriately authorized data during development and testing.
- Do not use AI-generated content as a diagnosis or treatment recommendation.
- Treat classifications, summaries, extracted information, and draft replies as suggestions requiring staff oversight.
- Review draft replies before sending them.
- Do not assume an appointment, refund, or other action has occurred unless staff have verified it.
- Protect API keys, patient information, and database credentials.

## Current Limitations

- Safety screening is keyword-based and is not clinically validated.
- AI-generated classifications and summaries may be inaccurate.
- Draft replies require staff review before use.
- The application is a prototype, not a production-ready clinical system.
- Production deployment would require additional security, privacy, access-control, monitoring, and reliability testing.

## Future Improvements

- Add authentication and role-based access control.
- Expand automated tests for database and interface workflows.
- Improve safety-screening coverage and validation.
- Add structured logging and error monitoring.
- Add deployment configuration and dependency management.
- Improve reporting and enquiry-volume analytics.

## Project Status

The core application workflows have been exercised during development, including enquiry analysis, database persistence, status updates, follow-up management, and safety-flagged enquiry handling.

The automated test suite previously completed with 17 passing tests. Further testing, documentation verification, and deployment hardening are needed before production use.

## Disclaimer

This project is intended for educational and administrative workflow demonstration purposes only. It does not provide medical advice, diagnose conditions, or replace qualified healthcare professionals.
