import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# 💡 Use your own OpenAI API key here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="🧠 SQL Chatbot", layout="centered")
st.title("💬 Smart SQL Chatbot")

# --- Sidebar for Database Credentials ---
with st.sidebar:
    st.header("🔐 Connect to your SQL Database")

    db_user = st.text_input("DB Username", value="root")
    db_password = st.text_input("DB Password", type="password")
    db_host = st.text_input("DB Host", value="localhost")
    db_port = st.text_input("DB Port", value="3306")
    db_name = st.text_input("Database Name", value="your_database")
    connect_btn = st.button("🔌 Connect")

# Session states
if "connected" not in st.session_state:
    st.session_state.connected = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# DB connection
if connect_btn:
    try:
        engine_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        db_engine = create_engine(engine_url)
        db = SQLDatabase(db_engine)

        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

        query_chain = (
            RunnablePassthrough.assign(schema=lambda _: db.get_table_info())
            | ChatPromptTemplate.from_template(
                """Based on the following database schema, write a SQL query that answers the question:
                {schema}

                Question: {question}
                SQL Query:"""
            )
            | llm
            | StrOutputParser()
        )

        st.session_state.db = db
        st.session_state.query_chain = query_chain
        st.session_state.connected = True
        st.session_state.messages.append({"role": "assistant", "content": "✅ Connected! Ask me anything about your database."})
        st.success("Connected successfully!")

    except Exception as e:
        st.session_state.connected = False
        st.error(f"❌ Connection failed: {str(e)}")

# Chat UI
if st.session_state.connected:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question about your data...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            sql_query = st.session_state.query_chain.invoke({"question": user_input})
            result = st.session_state.db.run(sql_query)

            full_response = f"**📊 Result:**\n{result}\n\n**🤖 SQL:**\n```sql\n{sql_query}\n```"
            st.chat_message("assistant").markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            st.chat_message("assistant").markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
else:
    st.info("👈 Connect to your database to begin.")
