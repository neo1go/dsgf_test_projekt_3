from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary import SeleniumLibrary
from selenium.webdriver.firefox.options import Options
import mysql.connector
from datetime import datetime
import json
import time

"""
Keywords für die nun strikt getrennten Testfälle für eine bessere Abgrenzung.

Args:
- sl      alle Seleniumaktionen, die im Browser ausgeführt werden
- rf      die BuiltIn Funktionen steuern Robot-Framework Keywords und Logik
- LOGIN_STATUS   globaler Zustand jedes Users
- options         dient hier dem Browser Headless Modus

Keywords
- Cleanup DB
- Benutzer in Datenbank einfügen
- Login auf Saucedemo
- Ist User eingeloggt
- Kaufe alle Produkte
- Logout von Saucedemo
- Bowser schließen
"""
# ==================== Setup ====================
sl = SeleniumLibrary()
rf = BuiltIn()
LOGIN_STATUS = {}

# Headless-Konfiguration
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")

options.set_preference("dom.webnotifications.enabled", False)    # firefox spezifisch
options.set_preference("media.volume_scale", "0.0")


# hier werden die json-credentials geladen für adminer
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
    if cursor.fetchone() is None:    # fetchone holt 1 Zeile aus DB als tuple. Wenn 1te Zeile leer, dann...
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

        # Die Browser öffnen und im headless Modus offen lassen
        sl.open_browser("https://www.saucedemo.com/", browser = "firefox", options = options, alias = username)
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
            sl.wait_until_element_is_visible("xpath://div[contains(@class,'inventory_item_name')]", timeout="10s")  #geändert von 15s
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


# Speichert login Zustände in der DB
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


# Zustand für jeden User erfassen
@keyword("Ist User eingeloggt")
def ist_user_eingeloggt(username):
    return LOGIN_STATUS.get(username, False)      # default ist FALSE



# ==================== Kauf ====================
@keyword("Kaufe Alle Produkte")
def kaufe_alle_produkte(username):
        
    if not LOGIN_STATUS.get(username, False):
        print(f"⚠️ Benutzer {username} ist nicht eingeloggt – Kauf übersprungen.")
        save_purchase_result(username, product_name=None, price=None, success=False, error_message="Login fehlgeschlagen – kein Kauf möglich")
        return "FAIL", "Login fehlgeschlagen – kein Kauf möglich"

    try:
        sl.switch_browser(username)
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
                sl.go_to("https://www.saucedemo.com/inventory.html")
                time.sleep(1)

            except Exception as product_error:
                print(f"❌ Fehler beim Kauf von Produkt {index}: {product_error}")
                sl.capture_page_screenshot(f"screenshots/purchase_error_{username}_{index}.png")
                save_purchase_result(username, product_name=None, price=None, success=False, error_message=str(product_error))
                try:
                    sl.go_to("https://www.saucedemo.com/inventory.html")
                    time.sleep(2)
                except:
                    pass
                
                continue
            
        # immer zurück zur Hauptseite, damit der logout auch ausgeführt wird
        sl.go_to("https://www.saucedemo.com/inventory.html")
        time.sleep(2)
            
        return "PASS", ""

    except Exception as e:
        sl.capture_page_screenshot(f"screenshots/purchase_error_{username}.png")
        save_purchase_result(username, product_name=None, price=None, success=False, error_message=str(e))
        return "FAIL", str(e)


# speichert Kaufergebnis in DB für jedes Kaufelement
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
    print(f"🚪 Starte Logout für Benutzer: {username}")
    
    if not LOGIN_STATUS.get(username, False):
        print(f"⚠️ Benutzer {username} ist nicht im STATUS eingeloggt")
        save_logout_result(username, False, "Kein aktiver Login im STATUS")
        return "FAIL", "Kein aktiver Login im STATUS"

    try:
        sl.switch_browser(username)
        
        # Immer erst direkten Logout versuchen, dann Fallback
        try:
            # normaler Logout
            sl.click_button("id:react-burger-menu-btn")
            sl.wait_until_element_is_visible("id:logout_sidebar_link", timeout="3s")  # von 5s
            sl.click_element("id:logout_sidebar_link")
            time.sleep(2)
        except:
            # Fallback: Direkt zur Login-Seite
            print("🔄 Normales Menü fehlgeschlagen, verwende direkte Navigation")
            sl.go_to("https://www.saucedemo.com")
            time.sleep(2)
        
        # Erfolg prüfen
        sl.wait_until_element_is_visible("id:user-name", timeout="5s")  # von 10s
        
        LOGIN_STATUS[username] = False
        save_logout_result(username, True)
        print(f"✅ Logout erfolgreich für {username}")
        
        sl.close_browser()
        return "PASS", ""

    except Exception as e:
        error_msg = f"Logout fehlgeschlagen: {str(e)}"
        print(f"❌ {error_msg}")
        sl.capture_page_screenshot(f"screenshots/logout_error_{username}.png")
        
        LOGIN_STATUS[username] = False
        save_logout_result(username, False, error_msg)
        
        try:
            sl.close_browser()
        except:
            pass
            
        return "FAIL", error_msg



# speichert Logout Resultate
def save_logout_result(username, success, error_message=None):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        cursor.execute(
            "INSERT INTO logout_results (username, success, error_message, timestamp) VALUES (%s, %s, %s, %s)",
            (username, success, error_message, timestamp)
        )
        cursor.execute(
            "UPDATE users SET logged_in=%s WHERE username=%s",
            (False, username)  # Immer auf False setzen beim Logout
        )
        conn.commit()
        status_text = "erfolgreich" if success else "fehlgeschlagen"
        print(f"📝 Logout gespeichert: {username}, {status_text}")
        
    except Exception as e:
        print(f"❌ Fehler beim Speichern des Logout-Results: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()




# Prüft User Login Status aus Datenbank
def check_user_login_status_from_db(username):
    """Prüft den Login-Status direkt aus der Datenbank"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT logged_in FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result:
            status = result[0]
            return bool(status)
        else:
            return False
    except Exception as e:
        print(f"❌ Fehler beim Datenbank-Check: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
        
        
        
@keyword("Browser schließen")
def browser_schliessen():
    """Schließt alle Browser bis auf den zuerst geöffneten."""
    browser_ids = sl.get_browser_ids()

    if len(browser_ids) > 1:
        # Alle außer dem ersten Browser schließen
        for browser_id in browser_ids[1:]:
            print(f"🧩 Schließe Browser (ID: {browser_id})")
            sl.close_browser(browser_id)
        print("✅ Alle zusätzlichen Browser wurden geschlossen, der erste bleibt offen.")
    elif browser_ids:
        print("ℹ️ Nur ein Browser offen – bleibt bestehen.")
    else:
        print("⚠️ Kein Browser offen – nichts zu schließen.")
        
        


