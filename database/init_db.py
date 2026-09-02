"""
Database Initialization & Seed Runner
Executes database schema DDL and seeds initial physics concepts, prerequisites, and learner state.
Supports PostgreSQL (when DATABASE_URL is reachable) and SQLite for local offline development.
"""

import os
import sys
import sqlite3

def init_sqlite_db(db_path: str = "ai_teacher.db"):
    """
    Initializes a lightweight local SQLite database matching the schema for instant offline development.
    """
    print(f"[DB] Initializing local database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        is_guest INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        display_name TEXT DEFAULT 'Learner',
        default_language TEXT DEFAULT 'Hinglish',
        learning_level TEXT DEFAULT 'beginner',
        learning_goal TEXT,
        total_learning_time_seconds INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS concepts (
        id TEXT PRIMARY KEY,
        key TEXT UNIQUE,
        name TEXT,
        domain TEXT,
        description TEXT,
        difficulty_level TEXT DEFAULT 'beginner'
    );

    CREATE TABLE IF NOT EXISTS concept_prerequisites (
        concept_id TEXT,
        prerequisite_id TEXT,
        PRIMARY KEY (concept_id, prerequisite_id)
    );

    CREATE TABLE IF NOT EXISTS student_concept_mastery (
        student_id TEXT,
        concept_id TEXT,
        mastery_score REAL DEFAULT 0.0,
        confidence_score REAL DEFAULT 0.0,
        attempts_count INTEGER DEFAULT 0,
        successful_attempts INTEGER DEFAULT 0,
        PRIMARY KEY (student_id, concept_id)
    );

    CREATE TABLE IF NOT EXISTS lessons (
        id TEXT PRIMARY KEY,
        student_id TEXT,
        topic TEXT,
        target_duration_minutes INTEGER,
        language TEXT,
        level TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Seed core concepts
    concepts = [
        ('c-01', 'electric_charge', 'Electric Charge', 'Physics', 'beginner', "Coulomb's Law, fundamental charge carriers, positive and negative charges."),
        ('c-02', 'electric_current', 'Electric Current', 'Physics', 'beginner', 'Rate of charge flow over time (I = Q / t). Measured in Amperes.'),
        ('c-03', 'voltage', 'Voltage & Potential Difference', 'Physics', 'beginner', 'Work done per unit charge (ΔV = W / Q). Electric driving pressure.'),
        ('c-04', 'resistance', 'Resistance & Impedance', 'Physics', 'intermediate', 'Opposition to current flow caused by atomic collisions. Measured in Ohms (Ω).'),
        ('c-05', 'ohms_law', "Ohm's Law", 'Physics', 'intermediate', 'Fundamental relationship V = I * R linking voltage, current, and resistance.'),
        ('c-06', 'circuit_analysis', "Circuit Analysis & Kirchhoff's Laws", 'Physics', 'advanced', 'Series and parallel topologies, current division, loop conservation.')
    ]

    for c in concepts:
        cursor.execute("""
        INSERT OR IGNORE INTO concepts (id, key, name, domain, difficulty_level, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """, c)

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully with 6 core physics concept nodes!")

if __name__ == "__main__":
    init_sqlite_db()
