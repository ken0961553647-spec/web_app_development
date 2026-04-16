import sqlite3
import os

def get_db_connection():
    # 確保資料庫路徑是正確的
    # instance/database.db 位於專案根目錄
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')
    
    # 若 instance 目錄不存在，可以先建立
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # 啟用 foreign keys 支援
    conn.execute('PRAGMA foreign_keys = ON')
    return conn
