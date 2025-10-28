from robot.api.deco import keyword
import mysql.connector

@keyword("Benutzer in Datenbank einfügen")
def insert_user(username, password):
    """Fügt einen Benutzer in die users-Tabelle ein."""
    conn = mysql.connector.connect(
        host="localhost",           # Docker-Container Host
        user="root",
        password="geheim",
        database="testdb"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()

@keyword("Kaufergebnis speichern")
def save_purchase_result(username, product_name, price, success, error_message=None):
    """Speichert ein Kaufergebnis in der purchases-Tabelle."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="geheim",
        database="testdb"
    )
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO purchases (username, product_name, price, success, error_message)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, product_name, price, success, error_message))
    conn.commit()
    cursor.close()
    conn.close()
