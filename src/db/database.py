import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "helmet_detection.db")

def get_connection():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create detections table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            image_path TEXT NOT NULL,
            confidence REAL NOT NULL,
            status TEXT NOT NULL,
            gemini_description TEXT,
            is_batched BOOLEAN DEFAULT 0,
            violation_count INTEGER DEFAULT 1
        )
    ''')
    
    # Migration for existing database instances
    cursor.execute("PRAGMA table_info(detections)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'violation_count' not in columns:
        cursor.execute("ALTER TABLE detections ADD COLUMN violation_count INTEGER DEFAULT 1")
    
    conn.commit()
    conn.close()

def insert_detection(image_path, confidence, status, violation_count=1):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO detections (image_path, confidence, status, violation_count)
        VALUES (?, ?, ?, ?)
    ''', (image_path, confidence, status, violation_count))
    
    detection_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return detection_id

def update_detection_status(detection_id, status, gemini_description=None, violation_count=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    if gemini_description is not None and violation_count is not None:
        cursor.execute('''
            UPDATE detections 
            SET status = ?, gemini_description = ?, violation_count = ?
            WHERE id = ?
        ''', (status, gemini_description, violation_count, detection_id))
    elif gemini_description is not None:
        cursor.execute('''
            UPDATE detections 
            SET status = ?, gemini_description = ?
            WHERE id = ?
        ''', (status, gemini_description, detection_id))
    elif violation_count is not None:
        cursor.execute('''
            UPDATE detections 
            SET status = ?, violation_count = ?
            WHERE id = ?
        ''', (status, violation_count, detection_id))
    else:
        cursor.execute('''
            UPDATE detections 
            SET status = ?
            WHERE id = ?
        ''', (status, detection_id))
        
    conn.commit()
    conn.close()

def get_unbatched_detections():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM detections 
        WHERE is_batched = 0 AND (status = 'CONFIRMED_BY_YOLO' OR status = 'CONFIRMED_BY_GEMINI')
        ORDER BY timestamp ASC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_as_batched(detection_ids):
    if not detection_ids:
        return
        
    conn = get_connection()
    cursor = conn.cursor()
    
    placeholders = ','.join(['?'] * len(detection_ids))
    cursor.execute(f'''
        UPDATE detections 
        SET is_batched = 1
        WHERE id IN ({placeholders})
    ''', detection_ids)
    
    conn.commit()
    conn.close()

def get_pending_gemini_detections():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, image_path FROM detections 
        WHERE status = 'PENDING_GEMINI'
        ORDER BY timestamp ASC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
