import streamlit as st

from src.database import (
    get_all_enquiries,
    get_enquiry_draft_context,
    update_draft_reply,
)
from src.gemini_service import generate_draft_reply


def render_draft_reply_management():
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
