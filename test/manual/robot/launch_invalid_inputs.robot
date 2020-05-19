*** Settings ***
Documentation
Library                                     SeleniumLibrary
Library                                     Process
Library                                     ./library/UrlLibrary.py
Library                                     DataDriver       ./resources/invalidInputs.csv
Resource                                    ./../../keywords/keywords.robot
Resource                                    ./../../keywords/SSRS2_keywords.robot
Test Setup                                  Begin Web Test
Test Teardown                               End Web Test
Test Template                               Invalid Input

#If you want to run the program local and python3 command is not found
#1. Make sure the Python 3 folder is present in the PATH environment variable.
#2. Locate the "python.exe" file in the Python 3 folder.
#3. Copy and Paste the "python.exe" file within the Python 3 folder.
#4. Rename the copied file to "python3" (or whatever you want the command to be).

*** Variables ***
${BROWSER} =                                headlesschrome

*** Keywords ***
Invalid Input
    [Arguments]                             ${invalidInput}
    Encoders Reset
    Input Text                              name:launch_position       ${invalidInput}
    Wait until element is visible           CSS:#manual_launch_buttons > div > input:invalid

*** Test Cases ***
Launch Invalid Inputs Should Fail           ${invalidInput}
    [Documentation]                         Failing test means the input value is acceptable
