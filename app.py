import streamlit as st
from agent import build_agent

st.set_page_config(page_title="WeatherWise", page_icon="🌤️", layout="centered")
st.title("🌤️ WeatherWise")
st.caption("Powered by Groq + LangChain | Can search the web and check live weather")

if "agent" not in st.session_state:
    with st.spinner("Loading agent..."):
        st.session_state.agent = build_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if query := st.chat_input("Ask me anything... e.g. 'What's the weather in Tokyo?'"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = st.session_state.agent.invoke(
                    {"messages": [("human", query)]}
                )
                response = result["messages"][-1].content
            except Exception as e:
                error_msg = str(e).lower()
                if "rate limit" in error_msg or "429" in error_msg:
                    response = "I'm getting too many requests right now. Please wait a moment and try again."
                elif "api key" in error_msg or "authentication" in error_msg or "401" in error_msg:
                    response = "There's an issue with the API configuration. Please contact the app owner."
                elif "model" in error_msg and ("decommissioned" in error_msg or "deprecated" in error_msg):
                    response = "The AI model is currently unavailable. Please try again later."
                elif "timeout" in error_msg or "timed out" in error_msg:
                    response = "The request took too long. Please try again with a simpler question."
                else:
                    response = "Sorry, something went wrong while processing your request. Please try again."
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
