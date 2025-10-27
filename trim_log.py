import os
import glob

def trim_robot_log():
    log_dir = "logs/"  #Pfad muss noch gesetzt werden.
    pattern = os.path.join(log_dir, "log-*.html")

    # Alle passenden Dateien finden
    log_files = glob.glob(pattern)

    # Nach Erstellungszeit sortieren (neueste zuerst)
    log_files.sort(key=os.path.getmtime, reverse=True)

    # Nur die neuesten behalten (alles ab Index 5 löschen)
    if len(log_files) > 5:
        for old_file in log_files[5:]:
            try:
                os.remove(old_file)
                print(f"Gelöscht: {old_file}")
            except Exception as e:
                print(f"Fehler beim Löschen von {old_file}: {e}")
    
    