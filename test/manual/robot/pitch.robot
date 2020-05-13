#
#	Change all references of error code 500 to 200 when running
#	test on a real system. Response code 500 is used as the development
#	server can't find the resources. When connected to a pi the response
#	should be 200 rather than 500.
#
	
*** Settings ***
Documentation	Check functionality of buttons and input fields in the Pitch-section.
Library		SeleniumLibrary
Library		Process
Library         OperatingSystem	
Suite Setup	Begin Web Test
Suite Teardown	End Web Test


*** Variables ***
${BROWSER} =	firefox
${URL} =   	http://192.168.0.4:5000
${PORT} =	5000
${logfile}  	Get File  .dronelauncher.log


*** Keywords ***
Begin Web Test
    Open Browser  ${URL}  ${BROWSER}
    Maximize Browser Window

End Web Test
    Close Browser

Server Is Up 
    Wait Until Page Contains Element  xpath://button[@id="script_pitch_up"]
    Page Should Contain  Pitch
    Click Button  xpath://button[@id="script_reset_encoders"]

User Clicks Button Pitch Up
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
    Click Button  xpath://button[@id="script_pitch_up"]

User Clicks Button Pitch Down
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
    Click Button  xpath://button[@id="script_pitch_down"]

User Enters Value In Field
    [Arguments]	${input}
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
    Click Element  xpath://input[@class="form-2" and @name="pitch_position"]
    Input Text  xpath://input[@class="form-2" and @name="pitch_position"]  ${input}
    Click Button  xpath://button[@id="script_pitch_position"]

User Expects The Pitch To Increase
    ${target_string} =	Set Variable  POST /app_pitch_up HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
    ${target_string} =	Set Variable  POST /app_pitch_stop HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
	
User Expects The Pitch To Decrease
    ${target_string} =  Set Variable  POST /app_pitch_down HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
    ${target_string} =  Set Variable  POST /app_pitch_stop HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

User Expects The Pitch To Change With Code
    [Arguments]    ${error_code}
    ${target_string} =  Set Variable  POST /app_pitch_position HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  ${error_code}

Then User Expects An Error Message
    Alert Should Be Present  action=ACCEPT

Check Log
    [Arguments]	 ${target_string}  ${error_code}
    ${logfile}  Get File  .dronelauncher.log
    Should match  ${logfile}  *${target_string}*\"*${error_code}*


*** Test Cases ***

Pitch Up
    [Documentation]  Clicking the pitch up button
    [Tags]  pitch_up
    Given Server Is Up
    When User Clicks Button Pitch Up 
    Then User Expects The Pitch To Increase
	
Pitch Down
    [Documentation]  Clicking the pitch down button
    [Tags]  pitch_down
    Given Server Is Up
    When User Clicks Button Pitch Down
    Then User Expects The Pitch To Decrease

Pitch Value
    [Documentation]  Change pitch value arbitrarily
    [Tags]  pitch_value
    Given Server Is Up
    When User Enters Value In Field  -1
    Then User Expects An Error Message
    User Expects The Pitch To Change With Code	400
    When User Enters Value In Field  1
    User Expects The Pitch To Change With Code	500
    When User Enters Value In Field  89
    User Expects The Pitch To Change With Code	500
    When User Enters Value In Field  91
    User Expects The Pitch To Change With Code	400
    Then User Expects An Error Message
