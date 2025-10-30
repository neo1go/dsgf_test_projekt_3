*** Settings ***
Library    SeleniumLibrary
Library    Settings.keywords.db_keywords
Variables  ../saucedemo_users.py


*** Test Cases ***
Käufe durchführen
    [Documentation]  Führt mit jedem Benutzer einen Einkauf auf saucedemo.com durch.
    Log To Console    🧹 Lösche alte Testdaten...
    Cleanup DB

    FOR    ${user}    IN    @{USERS}
        Log To Console    🧩 Starte Test für Benutzer: ${user}[username]
        Benutzer in Datenbank einfügen    ${user}[username]    ${user}[password]

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

    # Login
    Input Text    id:user-name    ${username}
    Input Text    id:password     ${password}
    Click Button  id:login-button

    # Locked-Out-User prüfen
    ${locked}=    Run Keyword And Return Status    Page Should Contain Element    xpath://h3[contains(text(),'locked out')]
    IF    ${locked}
        Fail    Benutzer ist gesperrt: ${username}
    END

    # Warte bis Produkte sichtbar sind
    Wait Until Element Is Visible    xpath://div[contains(@class,"inventory_item_name")]    timeout=20s

    # Alle Produkte zählen
    ${count}=    Get Element Count    xpath://div[contains(@class,"inventory_item_name")]
    Log To Console    🛒 Benutzer ${username} sieht ${count} Produkte.

    # Schleife über alle Produkte
    FOR    ${index}    IN RANGE    1    ${count + 1}
        ${product_name}=    Get Text    xpath:(//div[contains(@class,"inventory_item_name")])[${index}]
        ${price}=           Get Text    xpath:(//div[contains(@class,"inventory_item_price")])[${index}]
        Log To Console    🧾 Kaufe Produkt ${index}/${count}: ${product_name} - ${price}

        Click Button    xpath:(//button[contains(translate(text(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"add to cart")])[${index}]
        Click Element   id:shopping_cart_container
        Wait Until Element Is Visible    id:checkout    timeout=10s
        Click Button    id:checkout

        Run Keyword And Ignore Error    Input Text    id:first-name    Test
        Run Keyword And Ignore Error    Input Text    id:last-name     User
        Run Keyword And Ignore Error    Input Text    id:postal-code   12345

        Click Button    id:continue
        Click Button    id:finish
        Page Should Contain    Thank you for your order!

        Kaufergebnis speichern    ${username}    ${product_name}    ${price}    ${True}
        Click Button    id:back-to-products
    END

    Close Browser
