import library_agent
import logging


def show_top_ui(st):
    st.title("AI-Powered Library Assistant")
    st.text("This is a library assistant app where user can enquire about the library, books etc.")


def show_query_ui(st, app_logger):
    agent_executor = config = None
    try:
        agent_executor, config = library_agent.initialize_agent(st)
    except Exception as e:
        app_logger.error(f"Error occurred in agent initialization : {e}")
        logging.error(f"Error occurred in agent initialization : {e}")

    user_query = st.text_input("Ask question: ", max_chars=60)

    btn = st.button("Find Answer")

    if btn or user_query:
        logging.info(f"\nUser query : {user_query}")

        placeholder = st.empty()
        placeholder.write("I am getting the answer...")

        try:
            response = library_agent.get_answer(agent_executor, config, user_query, app_logger)
            if len(response["messages"]) == 4:
                response = response["messages"][3].content
            else:
                response = response["messages"][1].content
            placeholder.write(response)
            logging.info(response)
        except Exception as e:
            logging.error(f"Error occurred while getting the answer : {e}")
            response = "Error occurred while getting the answer. Please try again."
            placeholder.write(response)
