

*** Settings ***
Documentation	Global documentation
Library		SeleniumLibrary
Library		./library/getip.py
Library		Process
Library         OperatingSystem	
Suite Setup	Begin Web Test
Suite Teardown	End Web Test


*** Variables ***
${BROWSER} =	firefox
${URL} =   	http://192.168.0.4:5000
${PORT} =	5000
${logfile}  	Get File	.dronelauncher.log

*** Keywords ***
Begin Web Test
#     import library	${CURDIR}/library/getip.py
#      Start Process	./resources/start_server.sh	shell=yes
      Open Browser	${URL}  	${BROWSER}
      Maximize Browser Window


End Web Test
#	Terminate Process
	Close Browser

Server Is Up 
	Wait Until Page Contains Element	xpath://button[@id="script_pitch_up"]
	Page Should Contain	Pitch
	Click Button		xpath://button[@id="script_reset_encoders"]

User Clicks Button Pitch Up
	Click Button	xpath://button[@id="script_pitch_up"]

User Clicks Button Pitch Down
	Click Button	xpath://button[@id="script_pitch_down"]

User Enters Value In Field
	[Arguments]	${input}
	Click Element	xpath://input[@class="form-2" and @name="pitch_position"]
	Input Text	xpath://input[@class="form-2" and @name="pitch_position"]  ${input}
	Click Button	xpath://button[@id="script_pitch_position"]

User Expects The Pitch To Increase
     	${target_string} =	Set Variable	POST /app_pitch_up HTTP/1.1
	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}
	
User Expects The Pitch To Decrease
     	${target_string} =	Set Variable	POST /app_pitch_down HTTP/1.1
	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}

User Expects The Pitch To Change
     	${target_string} =	Set Variable	POST /app_pitch_position HTTP/1.1
	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}

Then User Expects An Error Message
        Alert Should Be Present		action=ACCEPT

Check Log
	[Arguments]	${target_string}
        ${logfile}	Get File	.dronelauncher.log
	Should Contain   ${logfile}	${target_string}
	

*** Test Cases ***

Pitch Up
	[Documentation]		Clicking the pitch up button
	[Tags]			pitch_up
     	Given Server Is Up
	When User Clicks Button Pitch Up 
	Then User Expects The Pitch To Increase
	
Pitch Down
	[Documentation]		Clicking the pitch down button
	[Tags]			pitch_down
     	Given Server Is Up
	When User Clicks Button Pitch Down
	Then User Expects The Pitch To Decrease

Pitch Value
	[Documentation]		Change pitch value arbitrarily
	[Tags]			pitch_value
     	Given Server Is Up
	When User Enters Value In Field  -1
	Then User Expects An Error Message
	When User Enters Value In Field  1
	When User Enters Value In Field  89
	When User Enters Value In Field  91
	Then User Expects An Error Message
