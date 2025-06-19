# services/memory_service.py

import sqlite3
from datetime import datetime



class MemoryService:
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()



    def _init_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_input TEXT
            )""")



        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                asset TEXT,
                quantity REAL,
                result TEXT
            )""")

        self.conn.commit()



    def log_user_input(self, user_input: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO user_memory (timestamp, user_input) VALUES (?, ?)",
            (datetime.now().isoformat(), user_input)
        )
        self.conn.commit()



    def log_trade(self, action: str, asset: str, quantity: float, result: str = ""):
        cursor = self.conn.cursor()
        
        cursor.execute(
            "INSERT INTO trade_memory (timestamp, action, asset, quantity, result) VALUES (?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), action, asset, quantity, result)
        )
        self.conn.commit()




    def get_user_history(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute("SELECT timestamp, user_input FROM user_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()



    def get_trade_history(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute("SELECT timestamp, action, asset, quantity, result FROM trade_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()


#enddd
