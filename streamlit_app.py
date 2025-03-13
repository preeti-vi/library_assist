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

    app_logger.info("streamlit_app: before calling get_user_status")
    # Check the access count for the user
    access_allowed = app.get_user_status(app_logger)

    app_logger.info(f"streamlit_app: after calling get_user_status")
    if not access_allowed:
        app_logger.info(f"streamlit_app: access not allowed")
        msg = ("Sorry, you have exhausted the maximum number of queries limit and are now blocked. "
               "To extend your access limit, please write to \"preeti.virkar@gmail.com\"")
        st.error(msg)
    else:
        app_logger.info(f"streamlit_app: access allowed")
        app_ui.show_query_ui(st, app_logger)
