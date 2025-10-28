from robot.api.deco import keyword
import mysql.connector
from datetime import datetime

# 🔧 Hilfsfunktion für DB-Verbindung
def get_connection():
    return mysql.connector.connect(
        host="localhost",      # falls du in Docker bist und "mysql" heißt, anpassen
        user="root",
        password="geheim",
        database="testdb"
    )

# ✅ Keyword: Benutzer in Datenbank einfügen
@keyword("Benutzer in Datenbank einfügen")
def insert_user(username, password):
    """Fügt einen Benutzer in die users-Tabelle ein."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Keyword: Kaufergebnis speichern oder Cleanup durchführen
@keyword("Kaufergebnis speichern")
def save_purchase_result(username, product_name=None, price=None, success=False, error_message=None):
    """
    Speichert ein Kaufergebnis in 'purchases'.
    Wenn 'username' == 'Cleanup', werden alte Testdaten gelöscht.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 🧹 Cleanup-Befehl
    if username.lower() == "Cleanup":
        cursor.execute("DELETE FROM purchases")
        conn.commit()
        cursor.close()
        conn.close()
        print("🧹 Alte Testdaten in 'purchases' gelöscht.")
        return

    # 🕒 Zeitstempel für Eintrag
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 💾 Normaler Kauf oder Fehler speichern
    cursor.execute("""
        INSERT INTO purchases (username, product_name, price, success, error_message, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (username, product_name, price, success, error_message, timestamp))

    conn.commit()
    cursor.close()
    conn.close()

    # Log-Ausgabe in Konsole
    print(f"💾 Eintrag gespeichert: {username}, Erfolg: {success}")
