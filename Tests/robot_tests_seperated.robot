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
        Run Keyword If    '${status}' == 'FAIL'    Log    ⚠️ Login fehlgeschlagen für ${user}[username]: ${msg}
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
        ${username}=    Set Variable    ${user}[username]
        ${logged_in}=    Ist User eingeloggt    ${username}
        
        Run Keyword If    ${logged_in}    
        ...    Run Keywords    
        ...    Logout von Saucedemo    ${username}    
        ...    AND    
        ...    Log    ✅ Logout durchgeführt für ${username}
        ...    ELSE    
        ...    Log    ⚠️ ${username} war nicht eingeloggt – Logout übersprungen
    END
    
    Browser schließen
