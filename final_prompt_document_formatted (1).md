## Phase 1: Planning and requirements

Act as my AI automation project mentor and technical planner.

PROJECT:
AI-Powered Clinic Operations Assistant

CONTEXT:
I am building this as a practical project for an AI Growth & Automation Associate assessment. I am an intermediate Python learner. I use Windows, VS Code, Python, and have created a project folder named clinic-operations-assistant. I have created and activated a .venv virtual environment and installed Streamlit. I want to understand the purpose of every step and every piece of code.

PROJECT GOAL:
Build a working prototype for administrative staff at a fictional Australian GP clinic. The application will help process fictional clinic enquiries by classifying messages, extracting explicitly stated details, identifying missing information, storing requests, tracking status, and preparing draft replies for human review.

ALLOWED CATEGORIES:
1. appointment_booking
2. rescheduling
3. cancellation
4. clinic_information
5. billing
6. other

REQUIREMENTS:
- Use Python for workflow logic and validation.
- Use the Gemini API for AI-powered classification and information extraction.
- Use Streamlit for the user interface.
- Use SQL management server to store requests.
- Use fictional data and fictional clinic policies only.
- Never invent clinic policies or assume an appointment has been booked.
- Never automatically send replies.
- Do not provide medical advice or make clinical triage decisions.
- Potentially urgent language must trigger a cautious safety procedure and immediate human review; do not generate a routine reply in that case. Explain that keyword checks are only a limited safety net.
- Validate AI output in Python rather than trusting model output blindly.
- Keep the first version small and achievable, then suggest optional enhancements.
- Never expose API keys or commit them to GitHub.
- Include a sample/demo mode so the project can be demonstrated without a live API key if feasible.

YOUR TASK:
1. Explain the problem and target users.
2. Define the minimum viable product (MVP).
3. Separate essential features from optional features.
4. Describe the workflow from input to human review.
5. Recommend a simple architecture and explain each component.
6. Define measurable success criteria without inventing results.
7. List the project risks, limitations, and safety boundaries.
8. Propose a phased development plan.
9. Identify the deliverables needed for a project assessment, including prompt documentation, testing evidence, GitHub README, and demonstration video.
10. Create a concise problem-definition document that I can save in docs/problem_statement.md.

IMPORTANT INSTRUCTIONS:
- Do not build the application or generate all the code yet.
- Do not skip the reasoning behind technical choices.
- Explain technical terms in beginner-friendly English.
- Clearly distinguish recommendations from confirmed requirements.
- Work on Phase 1 only. Finish with a checklist of what I should review before moving to Phase 2.


---

## Phase 2: Data design

Act as my Python data design mentor. Continue the AI-Powered Clinic Operations Assistant project using the agreed Phase 1 specification. Design a simple JSON schema and SQLite record structure for the six categories: appointment_booking, rescheduling, cancellation, clinic_information, billing, and other. Include request ID, original message, category, explicitly stated preferred date/time, summary, missing fields, status, safety flag, human-review flag, draft reply, and timestamp where appropriate. Explain each field, which fields may be null, and how to validate allowed values. Create 15 fictional Australian GP clinic enquiries with manually assigned expected categories, including ambiguous and incomplete examples. Keep potentially urgent examples separate for safety testing. Never use real patient data or invent clinic policy facts. Do not write the application yet. Explain the result and give me one task at a time.



---

## Phase 3: Python foundation

Act as my beginner-friendly Python mentor. Continue the AI-Powered Clinic Operations Assistant from the approved schema and sample data. Help me build the Python foundation in small steps. First explain the folder structure and create only the first necessary file. Implement category validation, required-field checks, missing-information handling, and clear error messages. Explain every import, function, parameter, return value, and important line. Give me only one coding task at a time. After each task, wait for me to run it and share the result before continuing. Do not integrate Gemini or build the full Streamlit app yet.


---

## Phase 4: Gemini integration

Act as my AI integration and prompt-engineering mentor. Continue my AI-Powered Clinic Operations Assistant. Help me determine whether I have access to a Gemini API key and explain safe setup using environment variables or VS Code environment configuration. Never ask me to paste the key into chat or source code. Integrate the current supported Google Gemini Python SDK using its official documentation and a compatible model available to my account. Create a prompt that returns structured JSON using only the six agreed categories, extracts only explicitly stated facts, marks missing information, and never invents clinic policies or gives medical advice. Validate the returned data in Python. Then design prompt versions V1, V2, and V3 and a fair test plan using the same labelled messages. Record each prompt and revision. Teach one step at a time and wait for test results.



---

## Phase 5: Safety and error handling

Act as my Python testing and safety mentor. Review the current AI-Powered Clinic Operations Assistant code. Help me add conservative pre-checks for potentially urgent language before routine AI processing and prevent routine reply drafting when the safety rule triggers. Flag the request for immediate human review according to the fictional clinic procedure. Explain that keyword detection can miss urgent messages and is not clinical triage. Add handling for invalid JSON, missing fields, API errors, and unexpected categories. Create focused tests. Do not make clinical decisions or automatically send replies. Review existing code before proposing changes, explain each change, and work one task at a time.



---

## Phase 6: Database and interface

Act as my Streamlit and SQLite mentor. Continue my existing AI-Powered Clinic Operations Assistant and inspect the files and code already created before changing anything. Help me build a simple Streamlit form for entering fictional enquiries, displaying classification and extracted fields, showing missing information and safety alerts, preparing drafts for staff review, and saving requests to SQLite. Add a dashboard for request counts by category and status. Keep human approval mandatory; do not send messages or book real appointments. Preserve a sample/demo mode if live Gemini access is unavailable. Explain the code and give only one task at a time. Test each stage before proceeding.


---

## Phase 7: Testing and evaluation

Act as my software testing and evaluation mentor. Help me evaluate the completed AI-Powered Clinic Operations Assistant using a labelled fictional dataset. Test classification accuracy, field extraction accuracy, missing-information handling, safety-rule behavior, invalid model output, and API failures. Compare prompt versions using the same examples and report actual counts, percentages, and limitations. Do not fabricate test results or claim the development dataset proves real-world clinical safety. Help me write docs/evaluation_results.md and add relevant automated tests. Work through one test or task at a time and wait for my output.


---

## Phase 8: Release and submission

Act as my project release and assessment mentor. Review my completed AI-Powered Clinic Operations Assistant and help me prepare it for submission. Check the README, installation instructions, requirements.txt, .gitignore, .env.example, sample data, tests, prompt log, and measured evaluation results. Verify that no API key, real patient data, or sensitive credentials are committed. Explain how to publish the project to GitHub and, if suitable, deploy it with secure secrets. Help me prepare a video script of at least two minutes covering the problem, chosen AI tools, prompt revisions, architecture, challenges, working demo, results, and limitations. Do not claim features work unless tested. Give one task at a time.


---

## Adjusted Prompts Reflecting Implementation Changes


### Phase 2 (adjusted):

Act as my Python data design mentor. Continue the AI-Powered Clinic Operations Assistant project using the agreed Phase 1 specification. Design a simple JSON schema and SQL Server record structure for the six categories: appointment_booking, rescheduling, cancellation, clinic_information, billing, and other. Include request ID, original message, category, explicitly stated preferred date/time, summary, missing fields, status, safety flag, human-review flag, draft reply, and timestamp where appropriate. Explain each field, which fields may be null, and how to validate allowed values. Use the existing fictional sample dataset and verify its record count before documenting it. Do not invent a record count or claim that additional examples were created. Keep potentially urgent examples separate for safety testing. Never use real patient data or invent clinic policy facts. Do not write the application yet. Explain the result and give me one task at a time.


### Phase 6 (adjusted):

Act as my Streamlit and SQL Server mentor. Continue my existing AI-Powered Clinic Operations Assistant and inspect the files and code already created before changing anything. Help me build a simple Streamlit form for entering fictional enquiries, displaying classification and extracted fields, showing missing information and safety alerts, preparing drafts for staff review, and saving requests to SQL Server. Add an enquiry history view with status filter and search, plus status and follow-up management. Keep human approval mandatory; do not send messages or book real appointments. Explain the code and give only one task at a time. Test each stage before proceeding.


### Phase 7 (adjusted):

Act as my software testing and evaluation mentor. Help me test the completed AI-Powered Clinic Operations Assistant. Test safety-rule behavior, validation, invalid model output, and error handling with automated pytest tests. Report actual results and limitations. Do not fabricate test results or claim the development dataset proves real-world clinical safety. Work through one test or task at a time and wait for my output.
