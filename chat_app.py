import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Bhairava ", page_icon="R.png")

Langchain_API_KEY = st.secrets["LANGCHAIN_API_KEY"]
Groq_API_KEY = st.secrets["GROQ_API_KEY"]

st.title("Bhairava")
st.write("नमस्कार!🙏")

models = [ "llama-3.1-70b-versatile", "llama-3.1-8b-instant", "llama3-groq-70b-8192-tool-use-preview",
          "llama3-groq-8b-8192-tool-use-preview", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it",
           "gemma2-9b-it"
]

cols = st.columns(2)
with cols[0]:
    model = st.selectbox(label="**Choose your LLM Model**",
                         options=models,
                         index=2                                              
    )


clicked = st.button("Clear Chat History")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are helpful assistant pretending to be Bhairava"),
        ("placeholder","{Chat_history}"),
        ("user","{query}"),
    ]
)

llm = ChatGroq(model=model) #temperature=temperature

chain = prompt | llm | StrOutputParser()

msgs = StreamlitChatMessageHistory()
if len(msgs.messages) ==0 or clicked:
    msgs.clear()
    msgs.add_ai_message(chain.invoke(
        {"query": "Write a brief welcome message",
         "chat_history":[]
         }

    ))

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="query",
    history_messages_key="chat_history",
)

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)


chat_input = st.chat_input("“अपना प्रश्न पूछें”।   Please ask your Question ")

if chat_input:
    config = {"configurable": {"session_id" :"any"}}
    response = chain_with_history.invoke({"query": chat_input}, config)
    st.chat_message("user").write(chat_input)
    st.chat_message("au").write(response)
    #st.write(llm.model_name)