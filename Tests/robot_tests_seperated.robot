*** Settings ***
Library           SeleniumLibrary
Library           Settings.keywords.db_keywords
Variables         ../saucedemo_users.py
Suite Setup       Cleanup DB
Test Setup        Log    Starte Test

*** Test Cases ***
Login Test
    [Documentation]    Führt Login für alle Benutzer durch und speichert Ergebnisse
    FOR    ${user}    IN    @{USERS}
        Benutzer in Datenbank einfügen    ${user}[username]    ${user}[password]   
        
        ${status}    ${msg}=    Login auf Saucedemo    ${user}[username]    ${user}[password]
        Run Keyword If    '${status}[0]' == 'FAIL'    Log    ⚠️ Login fehlgeschlagen für ${user}[username]: ${msg}
    END

Käufe durchführen
    [Documentation]    Führt für alle eingeloggten Benutzer einen Einkauf durch
    FOR    ${user}    IN    @{USERS}
        ${logged_in}=    Ist User eingeloggt    ${user}[username]
        Run Keyword If    ${logged_in}    Kaufe Alle Produkte    ${user}[username] 
        Run Keyword If    not ${logged_in}    Log    ⚠️ Benutzer ${user}[username] nicht eingeloggt – Kauf übersprungen
    END

Logout Test
    [Documentation]    Führt Logout für alle eingeloggten Benutzer durch
    FOR    ${user}    IN    @{USERS}
        ${logged_in}=    Ist User eingeloggt    ${user}[username]
        Run Keyword If    ${logged_in}    Logout von Saucedemo    ${user}[username]
        Run Keyword If    not ${logged_in}    Log    ⚠️ Benutzer ${user}[username] war nicht eingeloggt – Logout übersprungen
    END
