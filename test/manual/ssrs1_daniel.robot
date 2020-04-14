*** Settings ***
Documentation    Global documentation
#Resource         ./resources/keywords.robot
Library          SeleniumLibrary
Library		 ./library/drone_library.py
Library		 Process
Test Setup       Begin Web Test
Test Teardown    End Web Test

*** Variables ***
${BROWSER} =		firefox
${URL} =    		http://192.168.0.4:5000
${IP} = 		return ip	
${PORT} =		5000
*** Keywords ***
Begin Web Test
#      Run Process ./ssrs1_daniel_start_server.sh  shell=yes   --option  argument
      Start Process  ./ssrs1_daniel_start_server.sh  shell=yes

      Open Browser	${URL}  	${BROWSER}
      Maximize Browser Window

End Web Test
	Terminate Process
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
	Click Element	xpath://input[@class="form-2" and @name="pitch_position"]
	Input Text	xpath://input[@class="form-2" and @name="pitch_position"]  23
	Click Button	xpath://button[@id="script_pitch_position"]

User Expects The Pitch To Increase
	
*** Test Cases ***

Pitch Up
	[Documentation]		Clicking the pitch:up button
	[Tags]			pitch_up
     	Server Is Up
	User Clicks Button Pitch Up 
#	User Expects The Pitch To Increase
	
Pitch Down
	[Documentation]		Clicking The Pitch Down Button
	[Tags]			pitch_down
     	Server Is Up
	User Clicks Button Pitch Down
#	User Expects the pitch to decrease

Pitch Value
	[Documentation]		Clicking The Pitch Value 
	[Tags]			pitch_value
	# Set Selenium Speed	1 seconds		
     	Server Is Up
	User Enters Value In Field
#	User Expects The Pitch To Change

