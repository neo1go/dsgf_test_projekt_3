"""
Die keywords können so in python definiert werden und von robot ausgeführt werden.
Bei diesem Keyword handelt es sich um eine Datenbankoperation.

"""
from robot.api.deco import keyword
import mysql.connector

@keyword("Benutzer in Datenbank einfügen")
def insert_user(username, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="geheim",
        database="dbtest"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()
