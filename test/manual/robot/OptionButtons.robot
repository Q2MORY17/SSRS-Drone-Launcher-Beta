*** Settings ***
Documentation  Dronelauncher tests regarding settings for the automatic use
Resource  Resources/keywords.robot
Library  SeleniumLibrary
Library  Process
Library  ./Library/UrlLibrary.py
Library    OperatingSystem
Test Setup  Begin web test
Test Teardown  End web test

*** Variables ***
${BROWSER}  firefox
# ${URL} =  http://192.168.2.52:5000/
# ${IP} =  return ip
# ${PORT} =  5000
${logfile}  	Get File  .dronelauncher.log

*** Keywords ***
Begin Web Test
    ${URL}=                     Get Url
    Start Process               python3    ./python/dronelauncher_python.py    shell=True
    Open Browser                about:blank     ${BROWSER}
    Maximize Browser Window
    Sleep                       3s
    Go To                       ${URL}
    Sleep                       3s
#    Server Is Up

End Web Test
    Close Browser

Server Is Up
    Wait Until Page Contains Element  xpath://button[@id="script_pitch_up"]
    Page Should Contain  Pitch
    Click Button  xpath://button[@id="script_reset_encoders"]

User Clicks Home Button
	Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
	Click Button	//*[@id="script_home"]

User Expects The Right Function Call
	${target_string} =	Set Variable  POST /app_home HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

Check Log
    [Arguments]	 ${target_string}  ${error_code}
    ${logfile}  Get File  .dronelauncher.log
    Should match  ${logfile}  *${target_string}*\"*${error_code}*

*** Test Cases ***

Home Button
	[Documentation]		Clicking the Home button
	[Tags]			Home_Button

    Given Server Is Up
	When User Clicks Home Button
	Then User Expects The Right Function Call