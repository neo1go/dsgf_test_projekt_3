from robot.api.deco import keyword
import mysql.connector
from datetime import datetime
import json
"""
Dies sind die keywords, die vom Robot Framework 
verwendet werden.
Args:
Cleanup DB
Benutzer in Datenbank einfügen
Kaufergebnis speichern
"""

# liest die Variablen aus der config 
with open("config/config.json", "r")as file:
    config = json.load(file)
    
mysql_config = config["mysql"]

# Hilfsfunktion für DB-Verbindung
def get_connection():
    return mysql.connector.connect(
        host = mysql_config["host"],    
        user = mysql_config["user"],
        password = mysql_config["password"],
        database = mysql_config["database"]
    )

# Cleanup: löscht alle Einträge in purchases und users
@keyword("Cleanup DB")
def cleanup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM purchases")
    cursor.execute("DELETE FROM users")
    conn.commit()
    cursor.close()
    conn.close()
    print("🧹 Alte Testdaten in 'users' und 'purchases' gelöscht.")

# Benutzer in Datenbank einfügen, nur wenn nicht existiert
@keyword("Benutzer in Datenbank einfügen")
def insert_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        print(f"✅ Benutzer '{username}' eingefügt.")
    else:
        print(f"ℹ️ Benutzer '{username}' existiert bereits.")
    cursor.close()
    conn.close()

# Kaufergebnis speichern
@keyword("Kaufergebnis speichern")
def save_purchase_result(username, product_name=None, price=None, success=False, error_message=None):
    conn = get_connection()
    cursor = conn.cursor()

    # Timestamp für Eintrag
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO purchases (username, product_name, price, success, error_message, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (username, product_name, price, success, error_message, timestamp))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"💾 Kaufergebnis gespeichert: {username}, Erfolg: {success}")
