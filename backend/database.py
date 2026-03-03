# backend/database.py

import sqlite3
from datetime import datetime
from .models import QuestionnaireSession, Answer, Question
from typing import List

# Ensure the DB path works relative to the backend folder
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent / "questionnaire_sessions.db"

def init_db():
    """Initialize the SQLite database and tables."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                question_number INTEGER,
                question_text TEXT,
                answer_text TEXT,
                citations TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        ''')
        conn.commit()

def save_session(filename: str) -> int:
    """Save a new session and return its ID."""
    now = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO sessions (filename, created_at) VALUES (?, ?)",
            (filename, now)
        )
        session_id = c.lastrowid
    return session_id

def save_answers(session_id: int, answers: List[Answer]):
    """Save answers for a given session."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for ans in answers:
            citations_str = " | ".join(ans.citations) if ans.citations else ""
            c.execute(
                """
                INSERT INTO answers (session_id, question_number, question_text, answer_text, citations)
                VALUES (?, ?, ?, ?, ?)
                """,
                (session_id, ans.question.number, ans.question.text, ans.text, citations_str)
            )
        conn.commit()

def get_session_answers(session_id: int) -> List[Answer]:
    """Retrieve all answers for a given session."""
    answers = []
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            """
            SELECT question_number, question_text, answer_text, citations 
            FROM answers 
            WHERE session_id = ? 
            ORDER BY question_number
            """,
            (session_id,)
        )
        rows = c.fetchall()
        for q_num, q_text, a_text, cit_str in rows:
            citations = cit_str.split(" | ") if cit_str else []
            answers.append(
                Answer(
                    question=Question(number=q_num, text=q_text),
                    text=a_text,
                    citations=citations,
                    not_found="not found" in a_text.lower()
                )
            )
    return answers