
*** Settings ***

Documentation    Global documentation
Library          SeleniumLibrary
Library         OperatingSystem
Library		 Process
Suite Setup       Begin Web Test
Suite Teardown    End Web Test


*** Variables ***
${BROWSER} =		chrome
${URL} =    		http://192.168.1.126:5000
${logfile}  	Get File  .dronelauncher.log
${PORT} =		5000


*** Keywords ***
Begin Web Test
      Open Browser	${URL}  	${BROWSER}
      Maximize Browser Window


End Web Test
	Close Browser


Server Is Up
	Wait Until Page Contains Element	//*[@id="script_rotation_right"]
	Page Should Contain	Rotation
	Click Button		xpath://button[@id="script_reset_encoders"]


User Clicks Button Rotation Right
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
	Click Button	//*[@id="script_rotation_right"]


User Clicks Button Rotation Left
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
	Click Button	//*[@id="script_rotation_left"]


User Enters Value In Field
    [Arguments]	${input}
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
	Click Element	//*[@id="manual_rotation_buttons"]/div/input
	Input Text      //*[@id="manual_rotation_buttons"]/div/input  ${input}
    Click Button    //*[@id="script_rotation_position"]


User presses up arrow in textfeild
    Click Element	//*[@id="manual_rotation_buttons"]/div/input
    Press Keys  //*[@id="manual_rotation_buttons"]/div/input     ARROW_UP    ARROW_UP    ARROW_UP
    Click Button	//*[@id="script_rotation_position"]


User presses down arrow in textfeild
    Click Element	//*[@id="manual_rotation_buttons"]/div/input
    Press Keys  //*[@id="manual_rotation_buttons"]/div/input     ARROW_DOWN    ARROW_DOWN    ARROW_DOWN
    Click Button	//*[@id="script_rotation_position"]


User Expects The Rotor To Rotate To The Right
	${target_string} =	Set Variable  POST /app_rotation_right HTTP/1.1
	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
    ${target_string} =	Set Variable  POST /app_rotation_stop HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500


User Expects The Rotor To Rotate To The Left
	${target_string} =  Set Variable  POST /app_rotation_left HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
    ${target_string} =  Set Variable  POST /app_rotation_stop HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500


User Expects The Pitch To Change With Code
	[Arguments]    ${error_code}
    ${target_string} =  Set Variable  POST /app_rotation_position HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  ${error_code}


Then User Expects An Error Message
    Alert Should Be Present  action=ACCEPT


Check Log
    [Arguments]	 ${target_string}  ${error_code}
    ${logfile}  Get File  .dronelauncher.log
    Should match  ${logfile}  *${target_string}*\"*${error_code}*


*** Test Cases ***


Roatate To The Right
	[Documentation]		Clicking the Roatate to the Right
	[Tags]			Rotation_Right
    Given Server Is Up
	When User Clicks Button Rotation Right
	Then User Expects The Rotor To Rotate To The Right


Roatate To The Left
	[Documentation]		Clicking the Roatation_Left button
	[Tags]			Roatate_Left
    Given Server Is Up
	When User Clicks Button Rotation Left
	Then User Expects The Rotor To Rotate To The Left


Rotation Value
	[Documentation]		Change Roatation value then press GO!
	[Tags]			Roatateion_value
    Given Server Is Up
	When User Enters Value In Field  23
	Then User Expects The Pitch To Change With Code	500


Rotation Value change manuly up
	[Documentation]		Change Roatation value manualy by pressing upp arrow in textfield then press GO!
	[Tags]			Roatateion_value manualy changing
    Given Server Is Up
	When User presses up arrow in textfeild
	Then User Expects The Pitch To Change With Code    500


Rotation Value change manuly down
	[Documentation]		Change Roatation value manualy by pressing upp arrow in textfield then press GO!
	[Tags]			Roatateion_value manualy changing
    Given Server Is Up
	When User presses down arrow in textfeild
	Then User Expects The Pitch To Change With Code  500