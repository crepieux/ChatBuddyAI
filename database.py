import os
import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'dbname': os.environ.get('PGDATABASE'),
    'user': os.environ.get('PGUSER'),
    'password': os.environ.get('PGPASSWORD'),
    'host': os.environ.get('PGHOST'),
    'port': os.environ.get('PGPORT')
}

def get_db_connection():
    return psycopg2.connect(**db_params)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create messages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def add_message(sender, content):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO messages (sender, content) VALUES (%s, %s)", (sender, content))
    
    conn.commit()
    cur.close()
    conn.close()

def get_chat_history():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT sender, content, timestamp 
        FROM messages 
        ORDER BY timestamp
    """)
    
    chat_history = [{'sender': row[0], 'content': row[1], 'timestamp': row[2].isoformat()} for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return chat_history
