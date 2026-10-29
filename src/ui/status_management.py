import streamlit as st

from src.database import get_all_enquiries, update_enquiry_status


def render_status_management():
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
