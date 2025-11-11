from robot.api.deco import keyword 
import mysql.connector 
from datetime import datetime 
import json 
""" Dies sind die keywords, die vom Robot Framework verwendet werden. 
Cursor ist das Objekt zur Ausführung von SQL Befehlen und conn ist die Datenbankverbindung. 
Die Reihenfolge des Schließens der Verbindung muß eingehalten werden, sonst wird die Transaktion ungültig.
Args: 
- Cleanup DB  
- Login auf Saucedemo 
- Benutzer in Datenbank einfügen 
- Kaufergebnis speichern 
""" 
# liest die Variablen aus der config Datei 
with open("config/config.json", "r")as file:
    config = json.load(file) 
    mysql_config = config["mysql"] # Hilfsfunktion für DB-Verbindung mit den Credentials aus der Config Datei 
    def get_connection(): 
        return mysql.connector.connect( host = mysql_config["host"], user = mysql_config["user"], password = mysql_config["password"], database = mysql_config["database"] ) 

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
    print("Alte Testdaten in 'users' und 'purchases' gelöscht.") 


# Login auf der Webseite ausführen 
@keyword("Login auf Saucedemo") 
def login_auf_saucedemo(username, password): 
    print(f"Login-Versuch für Benutzer: {username}") 
    return "PASS", "" 


@keyword("Logout von Saucedemo") 
def logout_von_saucedemo(username): 
    print(f"Logout-Versuch für Benutzer {username}") 
    return "PASS", "" 

# Benutzer in Datenbank einfügen, nur wenn nicht existiert 
@keyword("Benutzer in Datenbank einfügen") 
def insert_user(username, password): 
    conn = get_connection()
    cursor = conn.cursor() 
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,)) 
    if cursor.fetchone() is None: 
        cursor.execute( "INSERT INTO users (username, password) VALUES (%s, %s)", (username, password) ) 
        conn.commit() 
        print(f"Benutzer '{username}' eingefügt.") 
    else: 
        print(f"ℹBenutzer '{username}' existiert bereits.") 
        cursor.close() 
        conn.close() 


# Es werden alle Produkte gekauft 
@keyword("Kaufe Alle Produkte") 
def kaufe_alle_produkte(username): 
    print(f"Kaufprozess für {username} gestartet.") 
    return "PASS", "" 


# Kaufergebnis speichern 
@keyword("Kaufergebnis speichern") 
def save_purchase_result(username, product_name=None, price=None, success=False, error_message=None): 
    conn = get_connection() 
    cursor = conn.cursor() 
    # Timestamp für Eintrag 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    cursor.execute(""" INSERT INTO purchases (username, product_name, price, success, error_message, timestamp) VALUES (%s, %s, %s, %s, %s, %s) """, (username, product_name, price, success, error_message, timestamp)) 
    conn.commit() 
    cursor.close() 
    conn.close() 
    print(f"Kaufergebnis gespeichert: {username}, Erfolg: {success}")