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
      Run Process  ./ssrs1_daniel_start_server.sh  shell=yes

      Open Browser	${URL}  	${BROWSER}
      Maximize Browser Window

End Web Test
	Close Browser

Server Is Up 
	Wait Until Page Contains Element	xpath://button[@id="script_pitch_up"]
	Page Should Contain	Pitch

User Click Button Pitch Up
	Click Button	xpath://button[@id="script_pitch_up"]

User Click Button Pitch Down
	Click Button	xpath://button[@id="script_pitch_down"]


User Expects The Pitch To Increase
	
*** Test Cases ***

Pitch Up
	[Documentation]		Clicking the pitch:up button
	[Tags]			pitch_up
	# Set Selenium Speed	1 seconds		
     	Given Server is up
	When User Clicks Button Pitch Up 
	Then User Expects The Pitch To Increase
	
Pitch Down
	[Documentation]		Clicking the pitch:up button
	[Tags]			pitch_up
	# Set Selenium Speed	1 seconds		
     	Given Server is up
	When User clicks buttin pitch:up 
	Then User Expects the pitch to decrease

Pitch Value
	[Documentation]		Clicking the pitch:up button
	[Tags]			pitch_up
	# Set Selenium Speed	1 seconds		
     	Given Server is up
	When User clicks buttin pitch:up 
	Then User Expects the pitch to increase

