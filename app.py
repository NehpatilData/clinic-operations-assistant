
import streamlit as st

from src.ui.enquiry_form import render_enquiry_form
from src.ui.enquiry_history import render_enquiry_history
from src.ui.status_management import render_status_management
from src.ui.follow_up_management import render_follow_up_management
from src.ui.draft_reply_management import render_draft_reply_management

st.set_page_config(
    page_title="Clinic Operations Assistant",
    layout="wide",
)

st.title("AI-Powered Clinic Operations Assistant")
st.write(
    "Welcome! This application will help clinic staff "
    "organize administrative enquiries."
)

render_enquiry_form()
st.divider()
render_enquiry_history()
st.divider()
render_status_management()
st.divider()
render_follow_up_management()
st.divider()
render_draft_reply_management()

