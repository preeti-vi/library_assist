import os

from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from streamlit import logger
import tools.tools as lib_tools
import logging
import uuid

load_dotenv()


def initialize_agent(st):
    logging.info(f"Langsmith : {os.environ.get("LANGSMITH_TRACING")}")

    if 'user_id' not in st.session_state:

        # Create User ID
        st.session_state.user_id = str(uuid.uuid4())

        # initialize  model
        model = ChatOpenAI(model="gpt-3.5-turbo")
        lib_tools.model = model

        # Define the agent
        memory = MemorySaver()
        tools = [lib_tools.is_book_available, lib_tools.enquiry]
        agent_executor = create_react_agent(model, tools, checkpointer=memory)

        # Define agent configuration
        config = RunnableConfig(recursion_limit=4, configurable={"thread_id": "abc123"})

        # store agent_executor and config in session
        st.session_state.agent_executor = agent_executor
        st.session_state.config = config

    return st.session_state.agent_executor, st.session_state.config


def get_answer(agent_executor, config, user_query, app_logger: logger):

    # app_logger.info("Getting the answer")

    return agent_executor.invoke(
            {"messages": [HumanMessage(content=user_query)]},
            config,
            stream_mode="values",
    )
