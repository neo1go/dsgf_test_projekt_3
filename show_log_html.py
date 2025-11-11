import os
import subprocess
import time
import geckodriver

# 🔧 Globale Variable definieren
webserver_process = None

def start_webserver(port=8000, directory="./results"):
    global webserver_process
    webserver_process = subprocess.Popen(
        ["python", "-m", "http.server", str(port)],
        cwd=directory,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)

def show_log_in_browser():
    log_path = os.path.abspath("./results/log.html")
    if os.path.exists(log_path) and os.path.getsize(log_path) > 240:
        start_webserver(port=8000)
        url = "http://localhost:8000/log.html"
        geckodriver.driver.execute_script(f"window.open('{url}', '_blank');")
        geckodriver.driver.switch_to.window(geckodriver.driver.window_handles[-2])
        stop_webserver()  # 🧹 Webserver direkt schließen
    else:
        print("Datei existiert nicht oder ist noch leer.")


def stop_webserver():
    global webserver_process
    if webserver_process and webserver_process.poll() is None:
        webserver_process.terminate()
        webserver_process.wait()
        print("🧹 Webserver wurde beendet.")
    else:
        print("ℹ️ Kein aktiver Webserver-Prozess gefunden.")
