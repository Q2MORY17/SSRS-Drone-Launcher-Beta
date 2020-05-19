*** Settings ***
Documentation
Library                                     SeleniumLibrary
Library                                     Process
Library                                     ./library/UrlLibrary.py
Resource                                    ./../../keywords/keywords.robot
Resource                                    ./../../keywords/SSRS2_keywords.robot
Test Setup                                  Begin Web Test
Test Teardown                               End Web Test

*** Variables ***
${BROWSER} =                                chrome

*** Keywords ***
#If you want to run the program local and python3 command is not found
#1. Make sure the Python 3 folder is present in the PATH environment variable.
#2. Locate the "python.exe" file in the Python 3 folder.
#3. Copy and Paste the "python.exe" file within the Python 3 folder.
#4. Rename the copied file to "python3" (or whatever you want the command to be).


Press Button Automatic
    Click Element                           xpath://a[contains(text(),'Automatic')]

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
    Verify Function Is Called              app_mount


Stop All Functions
    [Tags]                                  Stop
    Encoders Reset
    Press Button Automatic
    Press Button Stop
    Verify Function Is Called               app_stop


Functionable Button Standby
    Encoders Reset
    Press Button Automatic
    Press Button Standby
    Verify Function Is Called               app_standby


Functionable Button Prepare
    Encoders Reset
    Press Button Automatic
    Press Button Prepare
    Verify Function Is Called               app_prepare


Functionable Button Launch
    Encoders Reset
    Press Button Automatic
    Press Button Launch
    Verify Function Is Called               app_launch
