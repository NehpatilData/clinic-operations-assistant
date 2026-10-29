

# from src.gemini_service import test_gemini_connection

# print("Starting Gemini connection test...")

# if __name__ == "__main__":
#     try:
#         result = test_gemini_connection()
#         print("Gemini API request successful!")
#         print("Gemini response:", result)

#     except Exception as error:
#         print("Gemini connection test failed.")
#         print("Error type:", type(error).__name__)
#         print("Error details:", str(error))

# code 2--------------------------------------------------
# from src.gemini_service import analyze_clinic_enquiry

# if __name__ == "__main__":
#     message = "I would like to reschedule my appointment to Friday afternoon."

#     print("Testing AI clinic enquiry analysis...")
#     print("Original enquiry:", message)

#     try:
#         result = analyze_clinic_enquiry(message)

#         print("\nAI analysis result:")
#         for key, value in result.items():
#             print(f"{key}: {value}")

#     except Exception as error:
#         print("\nAI analysis failed.")
#         print("Error type:", type(error).__name__)
#         print("Error details:", str(error))

# code 3--------------------------------------------------


from src.gemini_service import process_clinic_enquiry


if __name__ == "__main__":
    test_messages = [
        "I am experiencing chest pain.",
        "What time does the clinic close?",
    ]

    for message in test_messages:
        print("\n" + "=" * 50)
        print("Original enquiry:", message)

        try:
            result = process_clinic_enquiry(message)

            print("Safety flag:", result["safety_flag"])
            print("Processing status:", result["processing_status"])
            print("Immediate human review:",
                  result["requires_immediate_human_review"])

            if result["ai_analysis"] is not None:
                print("AI analysis:", result["ai_analysis"])
            else:
                print("AI analysis skipped due to safety flag.")

        except Exception as error:
            print("Test failed.")
            print("Error type:", type(error).__name__)
            print("Error details:", str(error))
