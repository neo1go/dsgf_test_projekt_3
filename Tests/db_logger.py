import mysql.connector
from datetime import datetime

def log_failure_to_db(username, reason):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="dbtest"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_failures (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            reason TEXT,
            timestamp DATETIME
        )
    """)
    cursor.execute("""
        INSERT INTO login_failures (username, reason, timestamp)
        VALUES (%s, %s, %s)
    """, (username, reason, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
