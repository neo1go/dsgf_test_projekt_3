from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary import SeleniumLibrary
from selenium.webdriver.firefox.options import Options
import mysql.connector
from datetime import datetime
import json
import time

# ==================== Setup ====================
sl = SeleniumLibrary()
rf = BuiltIn()
LOGIN_STATUS = {}

options = Options()
options.headless = True


with open("config/config.json", "r") as file:
    config = json.load(file)
mysql_config = config["mysql"]

def get_connection():
    return mysql.connector.connect(
        host=mysql_config["host"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"]
    )

# ==================== DB Cleanup ====================
@keyword("Cleanup DB")
def cleanup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM purchases")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM login_results")
    cursor.execute("DELETE FROM logout_results")
    conn.commit()
    cursor.close()
    conn.close()
    print("Alte Testdaten gelöscht.")

# ==================== Benutzer ====================
@keyword("Benutzer in Datenbank einfügen")
def insert_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (username, password, logged_in) VALUES (%s, %s, %s)",
            (username, password, False)
        )
        conn.commit()
        print(f"Benutzer '{username}' eingefügt.")
    else:
        print(f"ℹ Benutzer '{username}' existiert bereits.")
    cursor.close()
    conn.close()

# ==================== Login ====================
@keyword("Login auf Saucedemo")
def login_auf_saucedemo(username, password):
    try:
        print(f"🔐 Login-Versuch für Benutzer: {username}")

        # Browser einmal öffnen und offen lassen
        sl.open_browser("https://www.saucedemo.com/", browser="firefox", options = options)
        sl.input_text("id:user-name", username)
        sl.input_text("id:password", password)
        sl.click_button("id:login-button")
        time.sleep(1)

        # Gesperrte Benutzer prüfen
        if rf.run_keyword_and_return_status("Page Should Contain Element", "xpath://h3[contains(text(),'locked out')]"):
            LOGIN_STATUS[username] = False
            sl.capture_page_screenshot(f"screenshots/login_locked_{username}.png")
            save_login_result(username, False, "Benutzer gesperrt")
            sl.close_browser()
            return "FAIL", f"Benutzer gesperrt: {username}"

        # Produkte sichtbar?
        try:
            sl.wait_until_element_is_visible("xpath://div[contains(@class,'inventory_item_name')]", timeout="15s")
        except:
            LOGIN_STATUS[username] = False
            sl.capture_page_screenshot(f"screenshots/login_failed_{username}.png")
            save_login_result(username, False, "Keine Produkte sichtbar oder Timeout")
            sl.close_browser()
            return "FAIL", f"Login fehlgeschlagen für {username}"

        LOGIN_STATUS[username] = True
        save_login_result(username, True)
        return "PASS", ""

    except Exception as e:
        sl.capture_page_screenshot(f"screenshots/login_error_{username}.png")
        try: sl.close_browser()
        except: pass
        LOGIN_STATUS[username] = False
        save_login_result(username, False, str(e))
        return "FAIL", str(e)

@keyword("Login Ergebnis speichern")
def save_login_result(username, success, error_message=None):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO login_results (username, success, error_message, timestamp) VALUES (%s, %s, %s, %s)",
        (username, success, error_message, timestamp)
    )
    cursor.execute(
        "UPDATE users SET logged_in=%s WHERE username=%s",
        (success, username)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Login Ergebnis gespeichert: {username}, Erfolg: {success}")



@keyword("Ist User eingeloggt")
def ist_user_eingeloggt(username):
    return LOGIN_STATUS.get(username, False)



# ==================== Kauf ====================
@keyword("Kaufe Alle Produkte")
def kaufe_alle_produkte(username):
    
    
        
    if not LOGIN_STATUS.get(username, False):
        print(f"⚠️ Benutzer {username} ist nicht eingeloggt – Kauf übersprungen.")
        save_purchase_result(username, product_name=None, price=None, success=False, error_message="Login fehlgeschlagen – kein Kauf möglich")
        return "FAIL", "Login fehlgeschlagen – kein Kauf möglich"

    try:
        count = sl.get_element_count("xpath://div[contains(@class,'inventory_item_name')]")
        print(f"🛍️ {username} sieht {count} Produkte.")

        for index in range(1, count + 1):
            try:
                product_name = sl.get_text(f"xpath:(//div[contains(@class,'inventory_item_name')])[{index}]")
                price = sl.get_text(f"xpath:(//div[contains(@class,'inventory_item_price')])[{index}]")
                print(f"🧾 Kaufe Produkt {index}/{count}: {product_name} - {price}")

                sl.click_button(f"xpath:(//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'add to cart')])[{index}]")
                sl.click_element("id:shopping_cart_container")
                sl.wait_until_element_is_visible("id:checkout", timeout="10s")
                sl.click_button("id:checkout")

                sl.input_text("id:first-name", "Test")
                sl.input_text("id:last-name", "User")
                sl.input_text("id:postal-code", "12345")
                sl.click_button("id:continue")
                sl.click_button("id:finish")

                sl.page_should_contain("Thank you for your order!")
                save_purchase_result(username, product_name=product_name, price=price, success=True)

                sl.click_button("id:back-to-products")
                time.sleep(1)

            except Exception as product_error:
                sl.capture_page_screenshot(f"screenshots/purchase_error_{username}_{index}.png")
                save_purchase_result(username, product_name=None, price=None, success=False, error_message=str(product_error))
                print(f"❌ Fehler beim Kauf von Produkt {index}: {product_error}")
                sl.go_to("https://www.saucedemo.com/inventory.html")
                time.sleep(1)

        return "PASS", ""

    except Exception as e:
        sl.capture_page_screenshot(f"screenshots/purchase_error_{username}.png")
        save_purchase_result(username, product_name=None, price=None, success=False, error_message=str(e))
        return "FAIL", str(e)



@keyword("Kaufergebnis speichern")
def save_purchase_result(username, product_name=None, price=None, success=False, error_message=None):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO purchases (username, product_name, price, success, error_message, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
        (username, product_name, price, success, error_message, timestamp)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Kaufergebnis gespeichert: {username}, Erfolg: {success}")

# ==================== Logout ====================
@keyword("Logout von Saucedemo")
def logout_von_saucedemo(username):
    if not LOGIN_STATUS.get(username, False):
        save_logout_result(username, False, "Kein Login vorhanden")
        return "FAIL", "Kein Login vorhanden"

    try:
        sl.go_to("https://www.saucedemo.com/inventory.html")
        time.sleep(2)

        menu_visible = rf.run_keyword_and_return_status("Page Should Contain Element", "id:react-burger-menu-btn")
        if not menu_visible:
            save_logout_result(username, False, "Logout fehlgeschlagen: Menü nicht sichtbar")
            return "FAIL", "Menü nicht sichtbar"

        sl.click_button("id:react-burger-menu-btn")
        sl.wait_until_element_is_visible("id:logout_sidebar_link", timeout="10s")
        sl.click_element("id:logout_sidebar_link")

        LOGIN_STATUS[username] = False
        save_logout_result(username, True)
        sl.close_browser()
        return "PASS", ""

    except Exception as e:
        save_logout_result(username, False, str(e))
        LOGIN_STATUS[username] = False
        return "FAIL", str(e)

@keyword("Logout Ergebnis speichern")
def save_logout_result(username, success, error_message=None):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO logout_results (username, success, error_message, timestamp) VALUES (%s, %s, %s, %s)",
        (username, success, error_message, timestamp)
    )
    cursor.execute(
        "UPDATE users SET logged_in=%s WHERE username=%s",
        (False, username)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Logout Ergebnis gespeichert: {username}, Erfolg: {success}")
