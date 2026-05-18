import sqlite3

DB_PATH = "pepper.db"

def delete_all_chats():
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM chats")
  cursor.execute("DELETE FROM messages")
  conn.commit()
  conn.close()

def init_db():
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  # Chats table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  
  # Messages table 
  cursor.execute("""
      CREATE TABLE IF NOT EXISTS messages (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          chat_id INTEGER NOT NULL,
          role TEXT NOT NULL,
          content TEXT NOT NULL
        )
    """)
  
  conn.commit()
  conn.close()

def create_chat(title):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  cursor.execute("""
      INSERT INTO chats (title) VALUES (?)
""", (title,))
  conn.commit()
  chat_id = cursor.lastrowid
  conn.close()
  return chat_id

def add_message(chat_id, role, content):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  cursor.execute("""
      INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)
""", (chat_id, role, content))
  conn.commit()
  conn.close()

def get_messages(chat_id):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  cursor.execute("""
      SELECT role, content FROM messages WHERE chat_id = ?
""", (chat_id,))
  rows = cursor.fetchall()
  conn.close()
  return [{"role": row[0], "content": row[1]} for row in rows]

def get_all_chats():
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  cursor.execute("""
      SELECT id, title FROM chats ORDER BY created_at DESC
""")
  rows = cursor.fetchall()
  conn.close()
  return rows