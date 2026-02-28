import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine
import sqlite3

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_groq import ChatGroq


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Chat with SQL DB", page_icon="🦜")
st.title("🦜 Chat with SQL Database")


# ---------------- DATABASE SELECTION ----------------
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = [
    "Use SQLite 3 Database - student.db",
    "Connect to your MySQL Database"
]

selected_opt = st.sidebar.radio(
    "Choose the DB which you want to chat",
    radio_opt
)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database")
else:
    db_uri = LOCALDB


# ---------------- API KEY ----------------
api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.info("Please enter your Groq API Key to continue.")
    st.stop()


# ---------------- LLM ----------------
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.3-70b-versatile"
)


# ---------------- DATABASE CONFIG ----------------
@st.cache_resource
def configure_db():
    if db_uri == LOCALDB:
        db_path = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))

    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please fill all MySQL fields.")
            st.stop()

        engine = create_engine(
            f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
        )
        return SQLDatabase(engine)


db = configure_db()


# ---------------- AGENT ----------------
@st.cache_resource
def create_agent_cached():
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )


agent = create_agent_cached()


# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# ---------------- USER INPUT ----------------
user_query = st.chat_input("Ask anything about your database")

if user_query:
    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        response = agent.run(user_query)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

        st.write(response)