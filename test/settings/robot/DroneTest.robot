*** Settings ***
Documentation  Dronelauncher tests regarding settings for the automatic use
Resource  Resources/keywords.robot
Library  SeleniumLibrary
#Test Setup  Begin web test
#Test Teardown  End web test

*** Variables ***
${BROWSER} =    chrome
${URL} =  http://192.168.1.236:5000/
${IP} =  return ip
${PORT} =  5000

*** Test Cases ***
IP address test
    [Documentation]
    [Tags]         IPtest
    Open Browser   about:blank  ${BROWSER}
    Go To          ${URL}
    Click Element    xpath:/html/body/ul/li[4]/a
    Input Text      xpath://*[@id="settings_launch"]/div[1]/input     -100
    Click Button    xpath://*[@id="script_change_pitch"]
    Handle Alert