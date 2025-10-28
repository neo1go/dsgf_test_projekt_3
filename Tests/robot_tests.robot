*** Settings ***
Library    SeleniumLibrary
Library    Settings.keywords.db_keywords
Variables  ../saucedemo_users.py

*** Test Cases ***
Käufe durchführen
    [Documentation]  Führt mit jedem Benutzer einen Einkauf auf saucedemo.com durch.
    FOR    ${user}    IN    @{USERS}
        ${status}=    Run Keyword And Ignore Error    Öffne Seite Und Kaufe Ein    ${user}[username]    ${user}[password]    ${user}[first_name]    ${user}[last_name]    ${user}[postal_code]
        IF    '${status}[0]' == 'FAIL'
            Log To Console    ❌ Einkauf fehlgeschlagen für ${user}[username]
            Kaufergebnis speichern    ${user}[username]    ${EMPTY}    ${EMPTY}    ${False}    ${status}[1]
        END
    END

*** Keywords ***
Öffne Seite Und Kaufe Ein
    [Arguments]    ${username}    ${password}    ${first_name}    ${last_name}    ${postal_code}
    Open Browser    https://www.saucedemo.com/    firefox
    Input Text    id:user-name    ${username}
    Input Text    id:password     ${password}
    Click Button   id:login-button
    Wait Until Page Contains Element    class:inventory_item_name

    # Beispielhaft: erstes Produkt kaufen
    ${product_name}=    Get Text    xpath:(//div[@class="inventory_item_name"])[1]
    ${price}=           Get Text    xpath:(//div[@class="inventory_item_price"])[1]
    Click Button        xpath:(//button[contains(text(),'Add to cart')])[1]
    Click Element       id:shopping_cart_container
    Click Button        id:checkout
    Input Text          id:first-name    ${first_name}
    Input Text          id:last-name     ${last_name}
    Input Text          id:postal-code    ${postal_code}
    Click Button        id:continue
    Click Button        id:finish
    Page Should Contain  Thank you for your order!

    Kaufergebnis speichern    ${username}    ${product_name}    ${price}    ${True}

    Close Browser
