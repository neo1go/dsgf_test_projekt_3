import os
import glob

# Pfad zum Log-Ordner
log_dir = "logs/"
pattern = os.path.join(log_dir, "log-*.html")

# Alle passenden Dateien finden
log_files = glob.glob(pattern)

# Nach Erstellungszeit sortieren (neueste zuerst)
log_files.sort(key=os.path.getmtime, reverse=True)

# Nur die ältesten behalten (alles ab Index 5 löschen)
for old_file in log_files[5:]:
    os.remove(old_file)
    print(f"Gelöscht: {old_file}")