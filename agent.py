from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools import all_tools
from dotenv import load_dotenv

load_dotenv()

def build_agent():
    llm = ChatGroq(model="openai/gpt-oss-20b")
    return create_react_agent(llm, all_tools)
