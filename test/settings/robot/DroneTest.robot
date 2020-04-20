*** Settings ***
Documentation  Dronelauncher tests regarding settings for the automatic use
Resource  Resources/keywords.robot
Library  SeleniumLibrary
Test Setup  Begin web test
Test Teardown  End web test

*** Variables ***
${BROWSER} =    chrome
${URL} =  http://192.168.1.236:5000/
${IP} =  return ip
${PORT} =  5000

*** Keywords ***
Begin Web Test
    Open Browser        about:blank     ${BROWSER}
    Maximize Browser Window

End Web Test
    Close Browser

*** Test Cases ***
Change Pitch Test
    [Documentation]     Test the "change pitch" function with negative outcome
    [Tags]              CPtest
    Go To               ${URL}
    Click Element       xpath:/html/body/ul/li[4]/a
    Input Text          xpath://*[@id="settings_launch"]/div[1]/input     -1
    Click Button        xpath://*[@id="script_change_pitch"]
    Handle Alert
    Input Text          xpath://*[@id="settings_launch"]/div[1]/input     91
    Click Button        xpath://*[@id="script_change_pitch"]
    Handle Alert


Change Lift Test
    [Documentation]    Test the "change lift" function with negative outcome
    [Tags]             CLtest
    Go To              ${URL}
    Click Element      xpath:/html/body/ul/li[4]/a
    Input Text         xpath://*[@id="settings_launch"]/div[2]/input   131
    Click Button       xpath://*[@id="script_change_lift"]
    Handle Alert
    Input Text         xpath://*[@id="settings_launch"]/div[2]/input   -1
    Click Button       xpath://*[@id="script_change_lift"]
    Handle Alert

Change Rotation Test
    [Documentation]    Test the "change rotation" function with negative outcome
    [Tags]             CRtest
    Go To              ${URL}
    Click Element      xpath:/html/body/ul/li[4]/a
    Input Text         xpath://*[@id="settings_launch"]/div[3]/input   181
    Click Button       xpath://*[@id="script_change_rotation"]
    Handle Alert
    Input Text         xpath://*[@id="settings_launch"]/div[3]/input   -181
    Click Button       xpath://*[@id="script_change_rotation"]
    Handle Alert