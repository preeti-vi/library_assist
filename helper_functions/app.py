from streamlit import logger
import logging
from dotenv import load_dotenv
import os
import helper_functions.utility_functions as util_functions


# Initialize loggers
def initialize_loggers():
    app_logger = logger.get_logger("SMI_APP")

    logging.basicConfig(filename="app.log", level=logging.INFO)

    # Disable httpx logging
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return app_logger


def authenticate_user(placeholder, st):
    if "authenticated" not in st.session_state:
        load_dotenv()

        AUTH_CODE = os.environ.get("AUTH_CODE")

        user_auth_code = placeholder.text_input("Enter auth code : ")

        if user_auth_code == AUTH_CODE:
            st.session_state["authenticated"] = True
            placeholder.write("")
        else:
            if user_auth_code:
                st.error("Invalid auth code. Please try again.")


def get_user_status(app_logger: logger):
    # Get user ip address
    user_ip = util_functions.get_user_ip()

    # Get the access count for the user: How many queries the user has submitted
    access_cnt = util_functions.get_access_count_for_user(user_ip)

    # Get maximum access count
    max_access_cnt = os.environ.get("MAX_ACCESS_CNT")

    app_logger.info(f"app:get_user_status: User Access cnt: {access_cnt}, Max access cnt: {max_access_cnt}")

    # Compare the access count with maximum limit
    if access_cnt > int(max_access_cnt):        # Maximum limit exceeded
        app_logger.info("app:get_user_status: maximum limit exceeded")
        return False
    else:                                       # Maximum limit not exceeded
        app_logger.info("app:get_user_status: access allowed")
        # increase the access count
        util_functions.increase_access_cnt(user_ip)
        return True

