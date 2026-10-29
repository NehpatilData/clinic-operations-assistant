import streamlit as st

from src.database import get_all_enquiries, update_follow_up_details


def render_follow_up_management():
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
