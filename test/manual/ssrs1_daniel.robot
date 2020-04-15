
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
${IP} = 		return_ip	
${PORT} =		5000

	
*** Keywords ***
Begin Web Test
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
	Page Should Contain	Pitch	# Placeholder for Gherkin

User Expects The Pitch To Decrease
	Page Should Contain	Pitch	# Placeholder for Gherkin

User Expects The Pitch To Change
	Page Should Contain	Pitch	# Placeholder for Gherkin



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
	[Documentation]		Change pitch value then press GO!
	[Tags]			pitch_value
     	Given Server Is Up
	When User Enters Value In Field
	Then User Expects The Pitch To Change

Another Test
	[Documentation]		Nonsens!
	[Tags]			nonsens
	${URL} =  return_ip
	hello	world
	${VARIABLE}=  return_ip
