# Projekt Setup Übersicht

## Installierte Anwendungen

| Anwendung / Tool                 | Version      | Anmerkung |
|----------------------------------|--------------|-----------|
| Python                           | 3.11.8       | Basisinstallation |
| Mozilla Firefox                  | 144.0.2      | schon vorhanden |
| GeckoDriverManager               | -            | Muss noch installiert werden |
| Robot Framework                  | 7.3.2        | via requirements.txt |
| Selenium Library                 | 6.8.0        | via requirements.txt |
| Docker                           | 28.5.1       | lokal, über pip für Python auch 7.1.0 |
| Docker Desktop                   | 4.49.0       | WSL/Ubuntu Backend |
| Adminer                          | 5.4.1        | eingebunden in Docker |
| MySQL                            | 15.1         | über Docker |
| WSL Ubuntu                       | 24.04.3      | Backend für Container-Ausführung unter Windows |
| MySQL Shell (VSCode)             | -            | zur DB-Nutzung |
| MySQL Connector (Python)         | 9.5.0        | für SQL-Befehle aus Python |
| VS-Code                          | 1.105.1      | IDE
| Python                           | 3.11.8       | Programmiersprache
---

## Python-Pakete in venv

| Paket                             | Version      |
|-----------------------------------|--------------|
| attrs                             | 25.4.0       |
| certifi                           | 2025.10.5    |
| cffi                              | 2.0.0        |
| charset-normalizer                | 3.4.4        |
| click                             | 8.3.0        |
| colorama                          | 0.4.6        |
| docker                            | 7.1.0        |
| geckodriver-autoinstaller         | 0.1.0        |
| h11                               | 0.16.0       |
| idna                              | 3.11         |
| mysql-connector-python            | 9.5.0        |
| outcome                           | 1.3.0.post0  |
| packaging                         | 25.0         |
| pip                               | 25.3         |
| pycparser                         | 2.23         |
| PySocks                           | 1.7.1        |
| python-dotenv                     | 1.2.1        |
| pywin32                           | 311          |
| requests                          | 2.32.5       |
| robotframework                    | 7.3.2        |
| robotframework-assertion-engine   | 3.0.3        |
| robotframework-databaselibrary    | 2.3.2        |
| robotframework-pythonlibcore      | 4.4.1        |
| robotframework-seleniumlibrary    | 6.8.0        |
| selenium                          | 4.38.0       |
| setuptools                        | 65.5.0       |
| sniffio                           | 1.3.1        |
| sortedcontainers                  | 2.4.0        |
| sqlparse                          | 0.5.3        |
| trio                              | 0.31.0       |
| trio-websocket                    | 0.12.2       |
| typing_extensions                 | 4.15.0       |
| urllib3                           | 2.5.0        |
| webdriver-manager                 | 4.0.2        |
| websocket-client                  | 1.9.0        |
| wsproto                           | 1.2.0        |

---


## Projekt Setup Schritte

1. Lokales Repository initialisiert
2. Virtuelle Umgebung (venv) erstellt
3. venv aktiviert mit venv\Scripts\activate 
4. Pakete aus requirements.txt installieren mit pip install -r requirements.txt
5. Zusätzliche Pakete nachträglich installieren
6. GeckoDriver und WebDriver Manager installieren / Umgebungsvariable setzen
     - Automatische Driver-Erkennung für Firefox
     - Umgebungsvariable für geckodriver gesetzt
7. Docker Desktop auf Linux-Modus umstellen
8. Adminer in Docker einbinden
9. MySQL Shell für VSCode installieren

---

# Hinweise / Tipps

venv nutzen: Alle Pakete sollten in der aktivierten virtuellen Umgebung installiert sein, sonst können Importfehler auftreten.

Versionen beachten: Robot Framework, Selenium, MySQL-Connector und Docker haben bekannte, getestete Versionen – andere Versionen könnten Fehler verursachen.

GeckoDriver: Autoinstaller sorgt dafür, dass immer der richtige Firefox-Treiber verwendet wird.

Docker-Container: Adminer und MySQL laufen in Containern, bitte sicherstellen, dass Docker Desktop läuft.

Robot Framework Tests: Nutzen Selenium + GeckoDriver für Browserinteraktion.

MySQL: Wird lokal über Docker bereitgestellt, Zugang über VSCode Shell oder Adminer möglich.

Optional: Libraries wie robotframework-datadriver oder robotframework-requests können nach Bedarf installiert werden. Wegen der Eigenerstellung mittels Custom Keywords wurd auf deren Nutzung verzichtet.