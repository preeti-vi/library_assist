from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import SystemMessage


# define system prompts
sp_extract_book_name = """
  You are an intelligent assistant. Given a query, extract the book name and return only the book name.
"""

prompt_extract_book_name = (SystemMessage(content=sp_extract_book_name) + "{user_query}")

# Define helper functions


# Extract book name from the query
def extract_book_name(user_query: str, model):
    chain = prompt_extract_book_name | model | StrOutputParser()
    return chain.invoke({"user_query": user_query})


# Search whether the book is available online
def search_online(book_name: str):
    search = TavilySearchResults(max_results=1)
    response= search.invoke(f"Is there a book with name \"{book_name}\" and if yes, find the author of the book.")
    return book_name, response


# Analyze the search results and construct the output response
def analyze_search_results(book_name: str, search_result: str, model):
    sp_analyze_search_results = f"""
    Given a text, follow 2 steps:

    Step 1:
    Extract the author name for the book - "{book_name}" .
    If you do not find author name, return the output saying "The book is not available"
    Proceed to step 2, only If you get the author name.

    Steps:
    Return the output in the following format:

    The book is available.
    Title:
    Author:

    Do not mention steps in the output.
  """

    prompt_analyze_search_results = (SystemMessage(content=sp_analyze_search_results) + "{search_result}")

    chain = prompt_analyze_search_results | model | StrOutputParser()
    return chain.invoke({"search_result": search_result})
