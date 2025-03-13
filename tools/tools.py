from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, AIMessage
import helper_functions.library as helper
from langchain_core.output_parsers import StrOutputParser


model = None

# define prompt
sp_enquiry = """ You are a helpful library assistant. Consider that there is a library and customers come to you for enquiries related to library.

Generate the answers to the queries with best of your knowledge and some hypothetical data about the general functioning of libraries.
Even if you don't know the exact answer, generate hypothetical answer with best of your knowledge.

Example:
Query: What are library timings?
AI: 9 am till 6 pm

Query: How much do you charge?
AI: 500 rupees per month

User can ask any query about the library. Answer it in a natural human language and not as a robo.
If the query is not about the library, politely refuse to answer and get the conversation back on track about the library. 

"""

prompt_enquiry = SystemMessage(content=sp_enquiry)
prompt_enquiry = (prompt_enquiry + "what is the chrage" + AIMessage(content="The monthly charge is $10.") + "{user_query}")


@tool
def is_book_available(book_name: str) -> str:
    """To check if a book is available or not.
    Returns the details of the book if the book is available
    """

    # # Extract book name from the query
    # response = extract_book_name(query)

    # Search whether the book is available online
    response = helper.search_online(book_name)

    # Analyze the search results and construct the output response
    response = helper.analyze_search_results(book_name, response, model)

    return response


@tool
def enquiry(user_query: str) -> str:
    """Answer all the user queries except for book availability check"""

    chain = prompt_enquiry | model | StrOutputParser()

    response = chain.invoke({"user_query": user_query})

    return response
