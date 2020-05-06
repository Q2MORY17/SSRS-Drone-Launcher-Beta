*** Settings ***
Documentation
Library                                     SeleniumLibrary
Library                                     Process
Library                                     ./library/UrlLibrary.py
Library                                     DataDriver       ./testData/invalidInputs.csv
Test Setup                                  Begin Web Test
Test Teardown                               End Web Test
Test Template                               Invalid Input

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
    Terminate All Processes                 1

Encoders Reset
    Click Button                            id:script_reset_encoders

Invalid Input
    [Arguments]                             ${invalidInput}
    Encoders Reset
    Input Text                              name:launch_position       ${invalidInput}
    Wait until element is visible           CSS:#manual_launch_buttons > div > input:invalid

*** Test Cases ***
Launch Invalid Inputs Should Fail           ${invalidInput}
    [Documentation]                         Failing test means the input value is acceptable
