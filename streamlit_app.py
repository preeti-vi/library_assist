import streamlit as st
from helper_functions import app, app_ui

# Initialize loggers
app_logger = app.initialize_loggers()

app_ui.show_top_ui(st)
placeholder_auth = st.empty()

# Authenticate user
app.authenticate_user(placeholder_auth, st)

# If user validated:
if "authenticated" in st.session_state:

    # Check the access count for the user
    access_allowed = app.get_user_status(app_logger)

    if not access_allowed:
        app_logger.info(f"streamlit_app: access not allowed")
        msg = ("Sorry, you have exhausted the maximum number of queries limit and are now blocked.")
        st.error(msg)
    else:
        app_logger.info(f"streamlit_app: access allowed")
        app_ui.show_query_ui(st, app_logger)
