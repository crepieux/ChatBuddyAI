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
    
    # Drop existing tables
    cur.execute("DROP TABLE IF EXISTS messages")
    cur.execute("DROP TABLE IF EXISTS conversations")
    
    # Create conversations table
    cur.execute('''
        CREATE TABLE conversations (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create messages table with conversation_id
    cur.execute('''
        CREATE TABLE messages (
            id SERIAL PRIMARY KEY,
            conversation_id INTEGER REFERENCES conversations(id),
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

def create_conversation():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO conversations DEFAULT VALUES RETURNING id")
    conversation_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    
    return conversation_id

def add_message(conversation_id, sender, content):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO messages (conversation_id, sender, content) VALUES (%s, %s, %s)", 
                (conversation_id, sender, content))
    
    conn.commit()
    cur.close()
    conn.close()

def get_chat_history(conversation_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if conversation_id:
        cur.execute("""
            SELECT sender, content, timestamp, conversation_id
            FROM messages 
            WHERE conversation_id = %s
            ORDER BY timestamp
        """, (conversation_id,))
    else:
        cur.execute("""
            SELECT sender, content, timestamp, conversation_id
            FROM messages 
            ORDER BY timestamp DESC
            LIMIT 50
        """)
    
    chat_history = [{'sender': row[0], 'content': row[1], 'timestamp': row[2].isoformat(), 'conversation_id': row[3]} 
                    for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return chat_history

def get_conversations():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, created_at
        FROM conversations
        ORDER BY created_at DESC
    """)
    
    conversations = [{'id': row[0], 'created_at': row[1].isoformat()} for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return conversations
