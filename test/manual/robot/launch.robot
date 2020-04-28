*** Settings ***
Documentation
Library                 SeleniumLibrary
Library                 Process
Library                 ./library/UrlLibrary.py
Test Setup              Begin Web Test
Test Teardown           End Web Test

*** Variables ***
${BROWSER} =            headlesschrome

*** Keywords ***
Begin Web Test
    ${URL}=             Get Url
    Start Process       python3    ./python/dronelauncher_python.py    shell=True
    Open Browser        about:blank    ${BROWSER}
    Maximize Browser Window
    Go To               ${URL}

End Web Test
    Close Browser
    Terminate All Processes

Gui Is Visible
    Wait Until Page Contains Element    id=video

Gui Has Loaded
    Page Should Contain Element         id=script_battery_voltage

*** Test Cases ***
Battery Voltage Button Should Be Visible
    Gui Is Visible
    Gui Has Loaded
