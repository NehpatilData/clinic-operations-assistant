import streamlit as st

from src.database import save_enquiry
from src.gemini_service import process_clinic_enquiry


def render_enquiry_form():
    st.subheader("Submit a Clinic Enquiry")

    # status = st.selectbox(
    #     "Select the request status:",
    #     [
    #         "new",
    #         "awaiting_information",
    #         "in_progress",
    #         "completed",
    #     ],
    # )


    # category = st.selectbox(
    #     "Select the enquiry category:",
    #     [
    #         "appointment_booking",
    #         "rescheduling",
    #         "cancellation",
    #         "clinic_information",
    #         "billing",
    #         "other",
    #     ],
    # )


    message = st.text_area(
        "Enter the patient's enquiry:",
        placeholder="Example: I would like to reschedule my appointment.",
        height=150,
    )


    sender_phone = st.text_input(
        "Patient phone number (optional)",
        placeholder="Example: +919876543210",
        help="Enter the Indian mobile number with country code +91, if provided.",
    )



    if st.button("Submit Enquiry"):

        if not message.strip():
            st.warning("Please enter an enquiry before submitting.")

        else:
            try:
                # Run the safety check before routine AI processing.
                result = process_clinic_enquiry(message.strip())

            except Exception as ai_error:
                st.error(
                f"AI processing failed: "
                f"{type(ai_error).__name__}: {ai_error}"
            )
                # Gemini or another processing step failed.
                # Save the original message for later staff review.
                try:
                    request_id = save_enquiry(
                        original_message=message.strip(),
                        category="other",
                        sender_phone=sender_phone.strip() or None,
                        summary=(
                            "AI analysis pending because processing failed. "
                            "Staff review required."
                        ),
                        missing_fields=[],
                        status="new",
                        safety_flag=False,
                        needs_human_review=True,
                        draft_reply=None,
                    )

                    st.warning(
                        "AI analysis is unavailable. The enquiry was saved "
                        "for staff review without AI analysis."
                    )
                    st.write("Request ID:", request_id)

                except Exception as save_error:
                    st.error(
                        "AI processing failed, and the enquiry could not "
                        "be saved. Check the database connection."
                    )
                    st.exception(save_error)

            else:
                if result["processing_status"] == "safety_check_failed":
                    try:
                        request_id = save_enquiry(
                            original_message=message.strip(),
                            category="other",
                            sender_phone=sender_phone.strip() or None,
                            summary=(
                                "Safety screening failed. "
                                "Manual review required before further processing."
                            ),
                            missing_fields=[],
                            status="new",
                            safety_flag=True,
                            needs_human_review=True,
                            draft_reply=None,
                        )
                        st.error(
                            "Safety screening failed. The enquiry was saved "
                            "for human review. Follow the clinic's established "
                            "safety procedures."
                        )
                        st.write("Request ID:", request_id)
                    except Exception as save_error:
                        st.error(
                            "Safety screening failed, and the enquiry could "
                            "not be saved. Follow the clinic's established "
                            "procedures and notify the appropriate reviewer."
                        )
                        st.exception(save_error)

                elif result["safety_flag"]:
                    try:
                        request_id = save_enquiry(
                            original_message=message.strip(),
                            category="other",
                            sender_phone=sender_phone.strip() or None,
                            summary=(
                                "Potentially urgent language detected. "
                                "Immediate human review required."
                            ),
                            missing_fields=[],
                            status="new",
                            safety_flag=True,
                            needs_human_review=True,
                            draft_reply=None,
                        )

                        st.error(
                            "Potentially urgent language detected. "
                            "Routine AI processing was skipped. "
                            "Refer this message to the appropriate "
                            "human review process immediately."
                        )
                        st.write("Request ID:", request_id)

                    except Exception as save_error:
                        st.error(
                            "The potentially urgent enquiry could not be "
                            "saved. Follow the clinic's established "
                            "emergency procedure and notify the appropriate "
                            "human reviewer."
                        )
                        st.exception(save_error)

                else:
                    analysis = result["ai_analysis"]

                    try:
                        request_id = save_enquiry(
                            original_message=message.strip(),
                            category=analysis["category"],
                            preferred_date=analysis.get("preferred_date"),
                            preferred_time=analysis.get("preferred_time"),
                            sender_phone=sender_phone.strip() or None,
                            summary=analysis["summary"],
                            missing_fields=analysis.get("missing_fields", []),
                            status="new",
                            safety_flag=False,
                            needs_human_review=True,
                            draft_reply=None,
                        )

                        st.success("Enquiry analyzed and saved successfully!")
                        st.write("Request ID:", request_id)
                        st.write("AI-suggested category:", analysis["category"])
                        st.write("Summary:", analysis["summary"])
                        st.write(
                            "Preferred date:",
                            analysis.get("preferred_date") or "Not provided",
                        )
                        st.write(
                            "Preferred time:",
                            analysis.get("preferred_time") or "Not provided",
                        )
                        st.write(
                            "Missing information:",
                            ", ".join(analysis.get("missing_fields", []))
                            or "None identified",
                        )
                        st.info(
                            "A staff member must review the result "
                            "before taking action."
                        )

                    except Exception as save_error:
                        st.error(
                            "Gemini analyzed the enquiry, but the result "
                            "could not be saved. Please check the database."
                        )
                        st.exception(save_error)
