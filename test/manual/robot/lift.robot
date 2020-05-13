
*** Settings ***
Documentation    Global documentation

Library   SeleniumLibrary
Library	    ./library/getip.py
Library    Process
Library    OperatingSystem
Suite Setup    Begin Web Test
Suite Teardown    End Web Test

*** Variables ***
${BROWSER} = 		firefox
${URL} =    		http://192.168.1.15:5000
${IP} = 		return_ip
${PORT} =		5000
${logfile}  	Get File  .dronelauncher.log
	
*** Keywords ***

Begin Web Test
    Open Browser	${URL}  	${BROWSER}
    Maximize Browser Window

End Web Test
    Close Browser

Server Is Up
	Wait Until Page Contains Element  xpath://button[@id="script_lift_up"]
	Page Should Contain	lift
	Click Button		xpath://button[@id="script_reset_encoders"]

User Clicks Button Lift Up
	Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
	Click Button	xpath://button[@id="script_lift_up"]

User Clicks Button Lift Down
	Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
	Click Button	xpath://button[@id="script_lift_down"]

User Enters Value In Field
	[Arguments]	${input}				 
	Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
	Click Element	xpath://input[@class="form-3" and @name="lift_position"]
	Input Text	xpath://input[@class="form-3" and @name="lift_position"]  ${input}
	Click Button	xpath://button[@id="script_lift_position"]


User Expects The Lift To Increase
	${target_string} =	Set Variable  POST /app_lift_up HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
    ${target_string} =	Set Variable  POST /app_lift_stop HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

User Expects The Lift To Decrease
	${target_string} =  Set Variable  POST /app_lift_down HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
    ${target_string} =  Set Variable  POST /app_lift_stop HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

User Expects The Lift To Change with Code
	[Arguments]    ${error_code}
    ${target_string} =  Set Variable  POST /app_lift_position HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  ${error_code}

Then User Expects An Error Message
        Alert Should Be Present		action=ACCEPT

Check Log
    [Arguments]	 ${target_string}  ${error_code}
    ${logfile}  Get File  .dronelauncher.log
    Should match  ${logfile}  *${target_string}*\"*${error_code}*

*** Test Cases ***

Lift Up
	[Documentation]		Clicking the lift up button
	[Tags]			lift_up
     	Given Server Is Up
	When User Clicks Button Lift Up
	Then User Expects The Lift To Increase
	
Lift Down
	[Documentation]		Clicking the lift down button
	[Tags]			lift_down
     	Given Server Is Up
	When User Clicks Button Lift Down
	Then User Expects The Lift To Decrease

Lift Value
	[Documentation]		Change lift value to Max then ok values then Min
	[Tags]			lift_value
     	Given Server Is Up
	When User Enters Value In Field  131
    Then User Expects An Error Message
    User Expects The Lift To Change With Code	400
    When User Enters Value In Field  130
    User Expects The Lift To Change With Code	500
    When User Enters Value In Field  20
    User Expects The Lift To Change With Code	500
    When User Enters Value In Field  -1
    User Expects The Lift To Change With Code	400
    Then User Expects An Error Message