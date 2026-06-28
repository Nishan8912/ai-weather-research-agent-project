from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools import all_tools
from dotenv import load_dotenv

load_dotenv()

def build_agent():
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    return create_react_agent(llm, all_tools)
