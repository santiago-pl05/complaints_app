import sqlite3
import os
from datetime import datetime

def init_database():
    """Inicjalizacja bazy danych"""
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    
    # Tabela reklamacji
    c.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            productCode TEXT,
            importer TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            photo_path TEXT,
            assigned_to TEXT
        )
    ''')
    
    # Tabela komentarzy/akcji
    c.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER,
            action_type TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (complaint_id) REFERENCES complaints (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Baza danych zainicjalizowana!")

def add_complaint(title, description, importer, product_code=None, photo_path=None):
    """Dodaj nową reklamację"""
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    
    # POPRAWIONE: zgodność kolumn z definicją tabeli
    c.execute('''
        INSERT INTO complaints (title, description, importer, productCode, photo_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, importer, product_code, photo_path))
    
    complaint_id = c.lastrowid
    conn.commit()
    conn.close()
    return complaint_id

def get_complaints():
    """Pobierz wszystkie reklamacje"""
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT id, title, description, importer, productCode, status, created_at, photo_path 
        FROM complaints ORDER BY created_at DESC
    ''')
    
    complaints = []
    for row in c.fetchall():
        complaints.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'importer': row[3],
            'productCode': row[4],
            'status': row[5],
            'created_at': row[6],
            'photo_path': row[7]
        })
    
    conn.close()
    return complaints