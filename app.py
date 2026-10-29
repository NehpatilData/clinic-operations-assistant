
import streamlit as st

from src.database import (
    save_enquiry,
    get_all_enquiries,
    update_enquiry_status,
    update_follow_up_details,
    update_draft_reply,
    get_enquiry_draft_context,
)
from src.gemini_service import (
    process_clinic_enquiry,
    generate_draft_reply,
)

st.title("AI-Powered Clinic Operations Assistant")

st.write(
    "Welcome! This application will help clinic staff "
    "organize administrative enquiries."
)

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




st.divider()
st.subheader("Enquiry History")

try:
    enquiries = get_all_enquiries()

    if enquiries:
        # Search enquiries by ID, message, or category.
        search_text = st.text_input(
            "Search enquiries",
            placeholder="Enter request ID, message, or category...",
        )

        # Filter enquiries by workflow status.
        status_options = [
            "All",
            "new",
            "awaiting_information",
            "in_progress",
            "completed",
        ]

        selected_status = st.selectbox(
            "Filter by status",
            status_options,
        )

        filtered_enquiries = enquiries

        if search_text.strip():
            query = search_text.strip().lower()

            filtered_enquiries = [
                enquiry
                for enquiry in filtered_enquiries
                if query in str(enquiry["request_id"]).lower()
                or query in str(enquiry["original_message"] or "").lower()
                or query in str(enquiry["category"] or "").lower()
            ]

        if selected_status != "All":
            filtered_enquiries = [
                enquiry
                for enquiry in filtered_enquiries
                if enquiry["status"] == selected_status
            ]

        st.caption(
            f"Showing {len(filtered_enquiries)} of {len(enquiries)} enquiries"
        )

        if filtered_enquiries:
            st.dataframe(
                filtered_enquiries,
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("No enquiries match your search and status filter.")

    else:
        st.info("No enquiries have been saved yet.")

except Exception:
    st.error(
        "Unable to load enquiry history. "
        "Please check the database connection."
    )


st.divider()
st.subheader("Update Enquiry Status")

try:
    all_enquiries = get_all_enquiries()

    if all_enquiries:
        enquiry_ids = [
            enquiry["request_id"]
            for enquiry in all_enquiries
        ]
        

        selected_id = st.selectbox(
            "Select request ID",
            enquiry_ids,
            key="status_request_id",
        )

        selected_enquiry = next(
            enquiry
            for enquiry in all_enquiries
            if enquiry["request_id"] == selected_id
        )

        st.write("Current status:", selected_enquiry["status"])

        status_options = [
            "new",
            "awaiting_information",
            "in_progress",
            "completed",
        ]

        new_status = st.selectbox(
            "Choose new status",
            status_options,
            index=status_options.index(selected_enquiry["status"]),
            key="new_enquiry_status",
        )

        if st.button("Save Status", key="save_enquiry_status"):
            st.info("Save Status button clicked.")

            try:
                update_enquiry_status(selected_id, new_status)

                st.success(
                    f"Request {selected_id} status updated to {new_status}."
                )
                st.write("Updated status:", new_status)

            except Exception as error:
                st.error("Unable to save the status.")
                st.exception(error)

    else:
        st.info("No enquiries are available to update.")

except Exception as error:
    st.error("Unable to update the enquiry status.")
    st.exception(error)


st.divider()
st.subheader("Follow-up Management")

try:
    follow_up_enquiries = get_all_enquiries()

    if follow_up_enquiries:
        follow_up_ids = [
            enquiry["request_id"]
            for enquiry in follow_up_enquiries
        ]

        selected_follow_up_id = st.selectbox(
            "Select request ID for follow-up",
            follow_up_ids,
            key="follow_up_request_id",
        )

        selected_follow_up = next(
            enquiry
            for enquiry in follow_up_enquiries
            if enquiry["request_id"] == selected_follow_up_id
        )

        st.write(
            "Current follow-up status:",
            selected_follow_up["follow_up_status"] or "not_required",
        )

        follow_up_status_options = [
            "not_required",
            "pending",
            "contacted",
            "completed",
        ]

        current_follow_up_status = (
            selected_follow_up["follow_up_status"] or "not_required"
        )

        follow_up_status_index = (
            follow_up_status_options.index(current_follow_up_status)
            if current_follow_up_status in follow_up_status_options
            else 0
        )

        new_follow_up_status = st.selectbox(
            "Choose follow-up status",
            follow_up_status_options,
            index=follow_up_status_index,
            key="new_follow_up_status",
        )

        follow_up_notes = st.text_area(
            "Follow-up notes",
            value=selected_follow_up["follow_up_notes"] or "",
            placeholder="Record the follow-up action or outcome...",
            key=f"follow_up_notes_{selected_follow_up_id}",
        )

        if st.button("Save Follow-up", key="save_follow_up"):
            try:
                update_follow_up_details(
                    request_id=selected_follow_up_id,
                    follow_up_status=new_follow_up_status,
                    follow_up_notes=follow_up_notes,
                )

                st.success(
                    f"Follow-up details saved for request "
                    f"{selected_follow_up_id}."
                )
                st.write("Updated follow-up status:", new_follow_up_status)
                st.write("Updated follow-up notes:", follow_up_notes)


            except Exception as error:
                st.error("Unable to save follow-up details.")
                st.exception(error)

    else:
        st.info("No enquiries are available for follow-up.")

except Exception as error:
    st.error("Unable to load follow-up management.")
    st.exception(error)



# --------------------------------------------------
# Draft Reply Management
# --------------------------------------------------

st.header("Draft Reply Management")

draft_enquiries = get_all_enquiries()

if not draft_enquiries:
    st.info("No enquiries are available for draft replies.")

else:
    draft_ids = [
        enquiry["request_id"]
        for enquiry in draft_enquiries
    ]

    selected_draft_id = st.selectbox(
        "Select an enquiry for a draft reply",
        draft_ids,
        key="draft_reply_request_id",
    )

    try:
        draft_context = get_enquiry_draft_context(
            selected_draft_id
        )

        if draft_context["safety_flag"]:
            st.warning(
                "This enquiry has a safety flag. "
                "Do not generate a routine reply. "
                "Immediate human review is required."
            )

        else:
            if st.button(
                "Generate Draft Reply",
                key="generate_draft_reply",
            ):
                try:
                    result = generate_draft_reply(
                        message=draft_context["original_message"],
                        category=draft_context["category"],
                        summary=draft_context["summary"],
                        missing_fields=draft_context[
                            "missing_fields"
                        ],
                    )

                    if result.get("draft_reply"):
                        st.session_state[
                            f"draft_reply_{selected_draft_id}"
                        ] = result["draft_reply"]

                        st.success(
                            "Draft generated. Review it before saving."
                        )

                    else:
                        st.warning(
                            "No draft was generated. "
                            "Human review is required."
                        )

                except Exception as error:
                    st.error(
                        "Draft generation failed. "
                        "Check the API quota, connection, "
                        "and application logs."
                    )
                    st.caption(str(error))

            current_draft = st.session_state.get(
                f"draft_reply_{selected_draft_id}",
                draft_context["draft_reply"] or "",
            )

            edited_draft = st.text_area(
                "Review and edit the draft reply",
                value=current_draft,
                height=180,
                key=f"draft_editor_{selected_draft_id}",
            )

            if st.button(
                "Save Draft Reply",
                key="save_draft_reply",
            ):
                try:
                    update_draft_reply(
                        selected_draft_id,
                        edited_draft,
                    )

                    st.session_state[
                        f"draft_reply_{selected_draft_id}"
                    ] = edited_draft.strip()

                    st.success(
                        f"Draft reply saved for enquiry "
                        f"{selected_draft_id}. "
                        "It still requires staff review before sending."
                    )

                except Exception as error:
                    st.error(f"Could not save draft: {error}")

    except Exception as error:
        st.error(f"Could not load enquiry details: {error}")
