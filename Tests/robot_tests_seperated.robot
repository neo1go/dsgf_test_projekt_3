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
        Insert User into DB    ${user}[username]    ${user}[password]     # Keyword
        
        ${status}    ${msg}=    Login to Saucedemo    ${user}[username]    ${user}[password]   # Keyword
        Run Keyword If    '${status}' == 'FAIL'    Log    ⚠️ Login fehlgeschlagen für ${user}[username]: ${msg}
    END

Käufe durchführen
    [Documentation]    Führt für alle eingeloggten Benutzer einen Einkauf durch
    FOR    ${user}    IN    @{USERS}
        ${logged_in}=    Is User logged in    ${user}[username]      # Keyword
        Run Keyword If    ${logged_in}    Buy all products    ${user}[username]     # Keyword
        Run Keyword If    not ${logged_in}    Log    ⚠️ Benutzer ${user}[username] nicht eingeloggt – Kauf übersprungen
    END

Logout Test
    [Documentation]    Führt Logout für alle eingeloggten Benutzer durch
    FOR    ${user}    IN    @{USERS}
        ${username}=    Set Variable    ${user}[username]    # erstellt eine Variable aus beiden Werten
        ${logged_in}=    Is User logged in   ${username}     # Keyword
        
        Run Keyword If    ${logged_in}    
        ...    Run Keywords    
        ...    Logout from Saucedemo    ${username}    # Keyword
        ...    AND    
        ...    Log    ✅ Logout durchgeführt für ${username}
        ...    ELSE    
        ...    Log    ⚠️ ${username} war nicht eingeloggt – Logout übersprungen
    END
    
    Close active Browser            # Keyword
