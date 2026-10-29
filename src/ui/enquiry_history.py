import streamlit as st

from src.database import get_all_enquiries


def render_enquiry_history():
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
