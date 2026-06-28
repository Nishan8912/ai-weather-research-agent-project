from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for current information about any topic."""
    search = DuckDuckGoSearchRun()
    return search.run(query)
