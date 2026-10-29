
# import pyodbc
# import json

# connection_string = (
#     "DRIVER={ODBC Driver 18 for SQL Server};"
#     "SERVER=localhost\\SQLEXPRESS;"
#     "DATABASE=ClinicOperationsDB;"
#     "Trusted_Connection=yes;"
#     "TrustServerCertificate=yes;"
# )

# connection = pyodbc.connect(connection_string, timeout=5)

# try:
#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         INSERT INTO clinic_requests (
#             original_message,
#             category,
#             preferred_date,
#             preferred_time,
#             summary,
#             missing_fields_json,
#             status,
#             safety_flag,
#             needs_human_review
#         )
#         OUTPUT INSERTED.request_id
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """,
#         "TEST ONLY: I would like to reschedule my appointment.",
#         "rescheduling",
#         None,
#         "afternoon",
#         "Test enquiry for database verification.",
#         json.dumps(["preferred_date"]),
#         "new",
#         False,
#         True,
#     )

#     request_id = cursor.fetchone()[0]
#     connection.commit()

#     print("Test enquiry saved successfully!")
#     print("Request ID:", request_id)

# except Exception:
#     connection.rollback()
#     raise

# finally:
#     connection.close()

# ************************
# 2 time
# ************************

# from database import get_connection


# def test_database_connection():
#     connection = get_connection()

#     try:
#         cursor = connection.cursor()
#         cursor.execute("SELECT DB_NAME()")
#         result = cursor.fetchone()

#         print("Connected database:", result[0])

#         assert result[0] == "ClinicOperationsDB"

#         cursor.close()
#     finally:
#         connection.close()


# if __name__ == "__main__":
#     test_database_connection()
#     print("Database connection test passed!")

# ************************
# 3 time
# ************************


# from database import save_enquiry


# def test_save_enquiry():
#     request_id = save_enquiry(
#         original_message="TEST ONLY: Please reschedule my appointment.",
#         category="rescheduling",
#         preferred_time="afternoon",
#         summary="Test enquiry to verify database saving.",
#         missing_fields=["preferred_date"],
#         status="new",
#         safety_flag=False,
#         needs_human_review=True,
#     )

#     print("Enquiry saved successfully!")
#     print("Generated request ID:", request_id)

#     assert isinstance(request_id, int)
#     assert request_id > 0


# if __name__ == "__main__":
#     test_save_enquiry()
#     print("Database save test passed!")

# ************************
# 4 time
# ************************


from src.database import get_all_enquiries


def test_get_all_enquiries():
    enquiries = get_all_enquiries()

    print("Total enquiries retrieved:", len(enquiries))

    for enquiry in enquiries:
        print(
            enquiry["request_id"],
            "|",
            enquiry["category"],
            "|",
            enquiry["status"],
            "|",
            enquiry["original_message"],
        )

    assert isinstance(enquiries, list)
    assert len(enquiries) > 0

    print("Enquiry retrieval test passed!")


if __name__ == "__main__":
    test_get_all_enquiries()
