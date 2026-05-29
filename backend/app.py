"""
Task Manager Backend API

This module contains a FastAPI application that interfaces with a PostgreSQL
database to manage tasks. It provides basic CRUD endpoints to fetch and add tasks.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

# Initialize the FastAPI app
app = FastAPI(
    title="Docker Task Manager API",
    description="A simple task manager backend service integrating with PostgreSQL.",
    version="1.0.0"
)

# Configure Cross-Origin Resource Sharing (CORS)
# This allows communication from different domains/ports (useful for local React development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific origins in a production environment
    allow_credentials=True,
    allow_methods=["*"],  # Allow all standard methods (GET, POST, OPTIONS, and so on)
    allow_headers=["*"],  # Allow all custom/standard request headers
)

# Retrieve PostgreSQL database credentials from environment variables (loaded via Docker Compose)
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

def get_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    
    Returns:
        psycopg2.extensions.connection: A connection object to interface with PostgreSQL.
    """
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.get("/")
def read_root():
    """
    Root endpoint.
    
    Returns:
        dict: A health check or welcome message.
    """
    return {"message": "Task Manager API running!"}

@app.get("/tasks")
def get_tasks():
    """
    Retrieves all tasks from the database. Creates the tasks table if it does not exist.
    
    Returns:
        dict: A list of tasks where each task is represented as [id, title].
    """
    conn = get_connection()
    cur = conn.cursor()
    # Initialize the table schema if it's the first time running
    cur.execute("CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, title TEXT);")
    # Fetch all tasks from the database table
    cur.execute("SELECT * FROM tasks;")
    tasks = cur.fetchall()
    
    # Clean up cursor and connection resources
    cur.close()
    conn.close()
    return {"tasks": tasks}

@app.post("/tasks/{title}")
def add_task(title: str):
    """
    Adds a new task with the specified title to the database.
    
    Args:
        title (str): The name/description of the task to add.
        
    Returns:
        dict: A confirmation message indicating the task was successfully added.
    """
    conn = get_connection()
    cur = conn.cursor()
    # Insert new record using parameterized queries to prevent SQL injection
    cur.execute("INSERT INTO tasks (title) VALUES (%s);", (title,))
    # Commit transaction to persist changes in PostgreSQL
    conn.commit()
    
    # Clean up resources
    cur.close()
    conn.close()
    return {"message": "Task added"}
