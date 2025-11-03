import os
import webbrowser

def show_log_in_browser():
    if os.path.exists("./results/log.html") and os.path.getsize("./results/log.html") > 240:
        webbrowser.get("firefox").open_new_tab("./results/log.html")
    else:
        print("Datei existiert nicht oder ist noch leer.")


