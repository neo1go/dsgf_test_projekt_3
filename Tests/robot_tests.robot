*** Settings ***
Library    SeleniumLibrary
Library    Settings.keywords.db_keywords
Variables  ../saucedemo_users.py

*** Test Cases ***
Käufe durchführen
    [Documentation]  Führt mit jedem Benutzer einen Einkauf auf saucedemo.com durch.

    Log To Console    🧹 Lösche alte Testdaten...
    Kaufergebnis speichern    Cleanup    ${EMPTY}    ${EMPTY}    ${False}    ${EMPTY}
    
    FOR    ${user}    IN    @{USERS}
        Log To Console    🧩 Starte Test für Benutzer: ${user}[username]
        
        Benutzer in Datenbank einfügen    ${username}    ${password}

        ${status}=    Run Keyword And Ignore Error    Öffne Seite Und Kaufe Ein    ${user}[username]    ${user}[password]

        IF    '${status}[0]' == 'FAIL'
            Log To Console    ❌ Einkauf fehlgeschlagen für ${user}[username]
            Kaufergebnis speichern    ${user}[username]    ${EMPTY}    ${EMPTY}    ${False}    ${status}[1]
        ELSE
            Log To Console    ✅ Einkauf erfolgreich für ${user}[username]
        END
    END


*** Keywords ***
Öffne Seite Und Kaufe Ein
    [Arguments]    ${username}    ${password}
    Open Browser    https://www.saucedemo.com/    firefox
    Maximize Browser Window

    # Login-Bereich
    Input Text    id:user-name    ${username}
    Input Text    id:password     ${password}
    Click Button  id:login-button

    # Falls Benutzer gesperrt ist, abbrechen
    ${locked}=    Run Keyword And Return Status    Page Should Contain Element    xpath://h3[contains(text(),'locked out')]
    IF    ${locked}
        Fail    Benutzer ist gesperrt: ${username}
    END

    # Warte bis Produktseite sichtbar ist
    Wait Until Page Contains Element    class:inventory_item_name    timeout=20s
    Run Keyword And Continue On Failure    Page Should Contain Element    class:inventory_item_name

    # Produktinformationen auslesen
    ${product_name}=    Get Text    xpath:(//div[@class="inventory_item_name"])[1]
    ${price}=           Get Text    xpath:(//div[@class="inventory_item_price"])[1]

    # Kauf durchführen
    Click Button        xpath:(//button[contains(text(),'Add to cart')])[1]
    Click Element       id:shopping_cart_container
    Click Button        id:checkout
    Input Text          id:first-name    Test
    Input Text          id:last-name     User
    Click Button        id:continue
    Click Button        id:finish
    Page Should Contain  Thank you for your order!

    # Ergebnis speichern
    Kaufergebnis speichern    ${username}    ${product_name}    ${price}    ${True}

    Close Browser
