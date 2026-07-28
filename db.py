import sqlite3
import json
import os

DB_PATH = "candidates.db"

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enables returning rows as dictionaries
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if not conn:
        return
        
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                extracted_skills TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("SQLite Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

def add_candidate(filename, content, extracted_skills):
    conn = get_db_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        # Check if file already exists to prevent exact duplicates
        cursor.execute("SELECT id FROM candidates WHERE filename = ?", (filename,))
        if cursor.fetchone():
            print(f"Candidate {filename} already exists in DB. Skipping insert.")
            return None
            
        cursor.execute(
            "INSERT INTO candidates (filename, content, extracted_skills) VALUES (?, ?, ?)",
            (filename, content, json.dumps(list(extracted_skills)))
        )
        inserted_id = cursor.lastrowid
        conn.commit()
        return inserted_id
    except Exception as e:
        print(f"Error inserting candidate: {e}")
        return None
    finally:
        conn.close()

def get_all_candidates():
    conn = get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, content, extracted_skills FROM candidates ORDER BY upload_date DESC")
        rows = cursor.fetchall()
        # Convert sqlite3.Row to standard dict for compatibility
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error fetching candidates: {e}")
        return []
    finally:
        conn.close()
