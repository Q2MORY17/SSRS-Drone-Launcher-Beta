*** Settings ***
Documentation     Maximizing and Minimizing the Drone Positions
Library           SeleniumLibrary
Test Setup         Begain Web Test
Test Teardown       End Web Test

*** Variables ***
${BROWSER} =        chrome
${URL} =            http://192.168.1.172:5000
${IP}=              return ip
${PORT} =           5000

*** Keywords ***
Begain Web Test
    Open Browser       ${URL}        ${BROWSER}
    Maximize Browser Window
End Web Test
    Close Browser
Display Page
       Wait Until Page Contains       Positions

User Click Button Max pitch
        Click Button        //*[@id="script_max_pitch"]

User Click Button Min pitch
        Click Button             //*[@id="script_min_pitch"]

User Click Button Max lift
        Click Button            //*[@id="script_max_lift"]

User Click Button Min lift
        Click Button            //*[@id="script_min_lift"]
*** Test Cases ***
Max pitch
    [Documentation]     Clicking the Positions Max pitch
    [Tags]              max_pitch
    Display Page
    User Click Button Max pitch
Min pitch
    [Documentation]         Clicking the Positions Max pitch
    [Tags]                  min_pitch
    Display Page
    User Click Button Min pitch

Max lift
    [Documentation]     Clicking the Positions Max pitch
    [Tags]              max_lift
    Display Page
    User Click Button Max lift
Min lift
    [Documentation]         Clicking the Positions Max pitch
    [Tags]                  min_lift
    Display Page
    User Click Button Min lift

