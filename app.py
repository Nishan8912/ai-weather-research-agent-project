import streamlit as st
from agent import build_agent

st.set_page_config(page_title="AI Agent", page_icon="🤖", layout="centered")
st.title("🤖 AI Research Agent")
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
                response = f"Error: {str(e)}"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
