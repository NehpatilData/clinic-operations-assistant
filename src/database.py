
import pyodbc


def get_connection():
    """Connect to the local ClinicOperationsDB database."""
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=ClinicOperationsDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string, timeout=5)

import json



def save_enquiry(
    original_message,
    category,
    preferred_date=None,
    preferred_time=None,
    summary=None,
    missing_fields=None,
    status="new",
    safety_flag=False,
    needs_human_review=True,
    draft_reply=None,
    sender_phone=None,
    follow_up_status="not_required",
    follow_up_notes=None,
    reviewed_at=None,
):
    """Save an administrative enquiry and follow-up details."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO clinic_requests (
                original_message,
                category,
                preferred_date,
                preferred_time,
                summary,
                missing_fields_json,
                status,
                safety_flag,
                needs_human_review,
                draft_reply,
                sender_phone,
                follow_up_status,
                follow_up_notes,
                reviewed_at
            )
            OUTPUT INSERTED.request_id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            original_message,
            category,
            preferred_date,
            preferred_time,
            summary or "Enquiry submitted; summary pending review.",
            json.dumps(missing_fields or []),
            status,
            safety_flag,
            needs_human_review,
            draft_reply,
            sender_phone,
            follow_up_status,
            follow_up_notes,
            reviewed_at,
        )

        request_id = cursor.fetchone()[0]
        connection.commit()

        return request_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()



def get_all_enquiries():
    """Retrieve enquiries and staff follow-up details from SQL Server."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                request_id,
                original_message,
                category,
                status,
                safety_flag,
                needs_human_review,
                created_at,
                sender_phone,
                follow_up_status,
                follow_up_notes,
                reviewed_at
            FROM clinic_requests
            ORDER BY request_id DESC
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "request_id": row[0],
                "original_message": row[1],
                "category": row[2],
                "status": row[3],
                "safety_flag": bool(row[4]),
                "needs_human_review": bool(row[5]),
                "created_at": row[6],
                "sender_phone": row[7],
                "follow_up_status": row[8],
                "follow_up_notes": row[9],
                "reviewed_at": row[10],
            }
            for row in rows
        ]

    finally:
        connection.close()



def update_enquiry_status(request_id, new_status):
    """Update an enquiry's workflow status and review timestamp."""

    from datetime import datetime

    allowed_statuses = {
        "new",
        "awaiting_information",
        "in_progress",
        "completed",
    }

    if new_status not in allowed_statuses:
        raise ValueError("Invalid enquiry status.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM clinic_requests
            WHERE request_id = ?
            """,
            request_id,
        )

        if cursor.fetchone() is None:
            raise ValueError("Enquiry not found.")

        if new_status in {"in_progress", "completed"}:
            reviewed_at = datetime.now()

            cursor.execute(
                """
                UPDATE clinic_requests
                SET status = ?, reviewed_at = ?
                WHERE request_id = ?
                """,
                new_status,
                reviewed_at,
                request_id,
            )
        else:
            cursor.execute(
                """
                UPDATE clinic_requests
                SET status = ?
                WHERE request_id = ?
                """,
                new_status,
                request_id,
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def update_follow_up_details(request_id, follow_up_status, follow_up_notes=None):
    """Update follow-up status and notes for an existing enquiry."""

    allowed_follow_up_statuses = {
        "not_required",
        "pending",
        "contacted",
        "completed",
    }

    if follow_up_status not in allowed_follow_up_statuses:
        raise ValueError("Invalid follow-up status.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM clinic_requests
            WHERE request_id = ?
            """,
            request_id,
        )

        if cursor.fetchone() is None:
            raise ValueError("Enquiry not found.")

        cursor.execute(
            """
            UPDATE clinic_requests
            SET follow_up_status = ?,
                follow_up_notes = ?
            WHERE request_id = ?
            """,
            follow_up_status,
            follow_up_notes.strip() if follow_up_notes else None,
            request_id,
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def update_draft_reply(request_id, draft_reply):
    """Save a staff-reviewed administrative draft reply."""

    if not isinstance(draft_reply, str) or not draft_reply.strip():
        raise ValueError("Draft reply cannot be empty.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM clinic_requests
            WHERE request_id = ?
            """,
            request_id,
        )

        if cursor.fetchone() is None:
            raise ValueError("Enquiry not found.")

        cursor.execute(
            """
            UPDATE clinic_requests
            SET draft_reply = ?,
                needs_human_review = 1
            WHERE request_id = ?
            """,
            draft_reply.strip(),
            request_id,
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_enquiry_draft_context(request_id):
    """Retrieve enquiry details needed to prepare a draft reply."""

    import json

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                original_message,
                category,
                summary,
                missing_fields_json,
                draft_reply,
                safety_flag
            FROM clinic_requests
            WHERE request_id = ?
            """,
            request_id,
        )

        row = cursor.fetchone()

        if row is None:
            raise ValueError("Enquiry not found.")

        return {
            "original_message": row[0],
            "category": row[1],
            "summary": row[2],
            "missing_fields": json.loads(row[3] or "[]"),
            "draft_reply": row[4],
            "safety_flag": bool(row[5]),
        }

    finally:
        connection.close()
