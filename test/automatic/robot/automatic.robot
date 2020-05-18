*** Settings ***
Documentation
Library                                     SeleniumLibrary
Library                                     Process
Library                                     ./library/UrlLibrary.py
Test Setup                                  Begin Web Test
Test Teardown                               End Web Test

*** Variables ***
${BROWSER} =                                headlesschrome

*** Keywords ***
#If you want to run the program local and python3 command is not found
#1. Make sure the Python 3 folder is present in the PATH environment variable.
#2. Locate the "python.exe" file in the Python 3 folder.
#3. Copy and Paste the "python.exe" file within the Python 3 folder.
#4. Rename the copied file to "python3" (or whatever you want the command to be).

Begin Web Test
    ${URL}=                                 Get Url
    Start Process                           python3    ./python/dronelauncher_python.py    shell=True
    Open Browser                            about:blank     ${BROWSER}
    Maximize Browser Window
    Go To                                   ${URL}

End Web Test
    Close Browser
    Terminate All Processes

Gui Is Visible
    Wait Until Page Contains Element        id:video

Gui Has Loaded
    Page Should Contain Element             id:script_battery_voltage

Encoders Reset
    Click Button                            id:script_reset_encoders

Press Button Automatic
    Click Element                           xpath://html[1]/body[1]/ul[1]/li[3]/a[1]

Verify Automatic Loaded
    Page Should Contain Element             id:script_standby

Press Button Mount
    Click Element                           id:script_mount
    Sleep                                   1

Press Button Standby
    Click Element                           id:script_standby
    Sleep                                   1

Press Button Prepare
    Click Element                           id:script_prepare
    Sleep                                   1

Press Button Launch
    Click Element                           id:script_launch
    Sleep                                   1

Press Button Stop
    Click Button                            id:script_stop
    Sleep                                   1

Verify Function Is Called
    [Arguments]                             ${function}
    ${result}                               Terminate Process
    Process Should Be Stopped
    Should Contain                          ${result.stderr}  ${function}

*** Test Cases ***
Battery Voltage Button Should Be Visible
    Gui Is Visible
    Gui Has Loaded


Automatic Page Loads
    [Tags]                                  Automaticpage
    Press Button Automatic
    Verify Automatic Loaded


Functionable Button Mount
    [Tags]                                  ButtonMount
    Encoders Reset
    Press Button Automatic
    Press Button Mount
    Verify Function Is Called               POST /app_mount HTTP/1.1


Stop All Functions
    [Tags]                                  Stop
    Encoders Reset
    Press Button Automatic
    Press Button Stop
    Verify Function Is Called               POST /app_stop HTTP/1.1


Functionable Button Standby
    Encoders Reset
    Press Button Automatic
    Press Button Standby
    Verify Function Is Called               POST /app_standby HTTP/1.1


Functionable Button Prepare
    Encoders Reset
    Press Button Automatic
    Press Button Prepare
    Verify Function Is Called               POST /app_prepare HTTP/1.1


Functionable Button Launch
    Encoders Reset
    Press Button Automatic
    Press Button Launch
    Verify Function Is Called               POST /app_launch HTTP/1.1
