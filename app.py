from dotenv import load_dotenv
import streamlit as st
from langchain_ollama import OllamaLLM

# load environment variables
load_dotenv()

# streamlit page setup
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("💬 Generative AI Chatbot")

# initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# initialize LLM
llm = OllamaLLM(
    model="llama3.1:8b",
    temperature=0.0,
)

# input box
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    # show user message
    st.chat_message("user").markdown(user_prompt)

    # store user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    # 🔥 build conversation prompt
    history_text = "You are a helpful assistant.\n\n"

    for msg in st.session_state.chat_history:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    history_text += "Assistant:"

    # get response from model
    response = llm.invoke(history_text)

    assistant_response = response

    # store assistant response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_response
    })

    # display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)