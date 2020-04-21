*** Settings ***
Documentation  Dronelauncher tests regarding settings for the automatic use
Resource  Resources/keywords.robot
Library  SeleniumLibrary
Test Setup  Begin web test
Test Teardown  End web test

*** Variables ***
${BROWSER} =    firefox
${URL} =  http://192.168.2.52:5000/
${IP} =  return ip
${PORT} =  5000

*** Keywords ***
Begin Web Test
    Open Browser        about:blank     ${BROWSER}
    Maximize Browser Window

End Web Test
    Close Browser

*** Test Cases ***
Change Pitch Test1
    [Documentation]     Test the "change pitch" function with negative outcome
    [Tags]              CPtest
    Go To               ${URL}
    Click Element       xpath:/html/body/ul/li[4]/a
    Input Text          xpath://*[@id="settings_launch"]/div[1]/input     -1
    Click Button        xpath://*[@id="script_change_pitch"]
    Alert Should be Present   Value should be between 0 and 90
    #Wait Until Page Contains    Value should be between 0 and 90
    #Handle Alert

Change Pitch Test2
    Go To                       ${URL}
    Click Element               xpath:/html/body/ul/li[4]/a
    Input Text                  xpath://*[@id="settings_launch"]/div[1]/input     91
    Click Button                xpath://*[@id="script_change_pitch"]
    Alert Should be Present     Value should be between 0 and 90

Change Pitch Test3
    Go To               ${URL}
    Click Element       xpath:/html/body/ul/li[4]/a
    Input Text          xpath://*[@id="settings_launch"]/div[1]/input     45
    Click Button        xpath://*[@id="script_change_pitch"]
    Alert Should Not be Present

Change Lift Test1
    [Documentation]    Test the "change lift" function with negative outcome
    [Tags]             CLtest
    Go To              ${URL}
    Click Element      xpath:/html/body/ul/li[4]/a
    Input Text         xpath://*[@id="settings_launch"]/div[2]/input   131
    Click Button       xpath://*[@id="script_change_lift"]
    Alert Should be Present     Value should be between 0 and 130

Change Lift Test2
    [Documentation]    Test the "change lift" function with negative outcome
    [Tags]             CLtest
    Go To              ${URL}
    Click Element      xpath:/html/body/ul/li[4]/a
    Input Text         xpath://*[@id="settings_launch"]/div[2]/input   -1
    Click Button       xpath://*[@id="script_change_lift"]
    Alert Should be Present     Value should be between 0 and 130

Change Lift Test3
    [Documentation]    Test the "change lift" function with negative outcome
    [Tags]             CLtest
    Go To              ${URL}
    Click Element      xpath:/html/body/ul/li[4]/a
    Input Text         xpath://*[@id="settings_launch"]/div[2]/input   65
    Click Button       xpath://*[@id="script_change_lift"]
    Alert Should Not be Present

Change Rotation Test1
    [Documentation]             Test the "change rotation" function with negative outcome
    [Tags]                      CRtest
    Go To                       ${URL}
    Click Element               xpath:/html/body/ul/li[4]/a
    Input Text                  xpath://*[@id="settings_launch"]/div[3]/input   181
    Click Button                xpath://*[@id="script_change_rotation"]
    Alert Should be Present     Value should be between -180 and 180

Change Rotation Test2
    [Documentation]             Test the "change rotation" function with negative outcome
    [Tags]                      CRtest
    Go To                       ${URL}
    Click Element               xpath:/html/body/ul/li[4]/a
    Input Text                  xpath://*[@id="settings_launch"]/div[3]/input   -181
    Click Button                xpath://*[@id="script_change_rotation"]
    Alert Should be Present     Value should be between -180 and 180

Change Rotation Test3
    [Documentation]             Test the "change rotation" function with negative outcome
    [Tags]                      CRtest
    Go To                       ${URL}
    Click Element               xpath:/html/body/ul/li[4]/a
    Input Text                  xpath://*[@id="settings_launch"]/div[3]/input   80
    Click Button                xpath://*[@id="script_change_rotation"]
    Alert Should Not be Present