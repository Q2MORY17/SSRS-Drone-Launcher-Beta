*** Settings ***
Documentation
Library                 SeleniumLibrary
Library                 Process
Library                 ./library/UrlLibrary.py
Suite Setup              Begin Web Test
Suite Teardown           End Web Test

*** Variables ***
${BROWSER} =            chrome

*** Keywords ***
Begin Web Test
    ${URL}=             Get Url
    Start Process       python3    ./python/dronelauncher_python.py    shell=True
    Open Browser        about:blank     ${BROWSER}
    Maximize Browser Window
    Go To               ${URL}

End Web Test
    Close Browser
    Terminate All Processes

Gui Is Visible
    Wait Until Page Contains Element     id=video

Gui Has Loaded
    Page Should Contain Element          id=script_battery_voltage

Encoders Reset
    Click Button                         id:script_reset_encoders

Press Button Backwards
    Click Button                         id:script_launch_backwards
    Sleep                                150

Verify Button Backwards Clicked
    ${result}       Terminate Process
    Process Should Be Stopped
    Log To Console      ${result.stderr}
    Should Contain      ${result.stderr}  POST /app_launch_backwards HTTP/1.1

*** Test Cases ***
Battery Voltage Button Should Be Visible
    Gui Is Visible
    Gui Has Loaded


Functionable Button Backwards
    [Documentation]       Since there is no intended visible response after pressing button backwards, this testcase tests button function
    ...                   by checking whether the action of clicking button backwards calls the targeted method function_launch_backwards()
    ...                   in dronelauncher_python.py.
    [Tags]                ButtonBackwards
    Given Encoders Reset
    When Press Button Backwards
    Then Verify Button Backwards Clicked
