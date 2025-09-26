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
            description TEXT,
            importer TEXT NOT NULL,
            productCode TEXT,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            photo_path TEXT,
            assigned_to TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Baza danych zainicjalizowana!")

def add_complaint(title, description, importer, product_code=None, photo_path=None):
    """Dodaj nową reklamację"""
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO complaints (title, description, importer, productCode, photo_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, importer, product_code, photo_path))
    
    complaint_id = c.lastrowid
    conn.commit()
    conn.close()
    return complaint_id

def get_complaints_paginated(page=1, limit=20, status=None, importer=None, date_from=None, date_to=None):
    """Pobierz reklamacje z paginacją i filtrami"""
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    
    # Buduj zapytanie z filtrami
    query = '''
        SELECT id, title, description, importer, productCode, status, created_at, photo_path 
        FROM complaints 
        WHERE 1=1
    '''
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    if importer:
        query += ' AND importer LIKE ?'
        params.append(f'%{importer}%')
    
    if date_from:
        query += ' AND DATE(created_at) >= ?'
        params.append(date_from)
    
    if date_to:
        query += ' AND DATE(created_at) <= ?'
        params.append(date_to)
    
    # Zapytanie o całkowitą liczbę
    count_query = 'SELECT COUNT(*) FROM complaints WHERE 1=1' + query.split('WHERE 1=1')[1]
    c.execute(count_query, params)
    total_count = c.fetchone()[0]
    
    # Dodaj sortowanie i paginację
    query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
    params.extend([limit, (page - 1) * limit])
    
    c.execute(query, params)
    
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
    return complaints, total_count

def get_complaints():
    """Pobierz wszystkie reklamacje (dla kompatybilności)"""
    complaints, _ = get_complaints_paginated(limit=1000)
    return complaints