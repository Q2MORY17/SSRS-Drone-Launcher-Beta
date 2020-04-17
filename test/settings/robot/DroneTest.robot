*** Settings ***
Documentation  Dronelauncher tests regarding settings for the automatic use
Resource  Resources/keywords.robot
Library  SeleniumLibrary
#Test Setup  Begin web test
#Test Teardown  End web test

*** Variables ***
${BROWSER} =    chrome
${URL} =  http://192.168.1.216:5000/
${IP} =  return ip
${PORT} =  5000

*** Test Cases ***
IP address test
    [Documentation]
    [Tags]         IPtest
    Open Browser   about:blank  ${BROWSER}
    Go To          ${URL}
