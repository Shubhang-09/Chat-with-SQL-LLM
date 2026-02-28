# Chat with SQL Database using LLM

This project allows users to query a SQL database using natural language.  
It converts user input into SQL queries using a Groq-powered LLM and executes them on either SQLite or MySQL.

## Motivation

I built this project to understand how Large Language Models can be integrated with structured databases and used for practical data querying applications.

## How It Works

- User selects SQLite or MySQL
- User enters a natural language query
- The LLM generates an SQL query
- The SQL query is executed on the selected database
- The results are returned in readable format

## Tech Stack

- Python
- Streamlit
- Groq API
- SQLite
- MySQL
- SQLAlchemy
- LangChain

## Features

- Natural language to SQL conversion
- Dynamic database switching (SQLite / MySQL)
- Secure API key handling using environment variables
- Interactive Streamlit interface

## Setup

1. Clone the repository
