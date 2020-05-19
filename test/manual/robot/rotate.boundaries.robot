*** Settings ***
Documentation   Global documentation
Library     SeleniumLibrary
Library     ./library/getip.py
Library     Process
Library     OperatingSystem
Suite Setup  Begin Web Test
Suite Teardown   End Web Test


*** Variables ***
${BROWSER} =    chrome
${URL} =    http://192.168.1.126:5000
${PORT} =   5000
${logfile}  	Get File    .dronelauncher.log


*** Keywords ***
Begin Web Test
      Open Browser      ${URL}  	${BROWSER}
      Maximize Browser Window


End Web Test
	Close Browser


Server Is Up
	Wait Until Page Contains Element	//*[@id="script_rotation_right"]
	Page Should Contain	Rotation
	Click Button		xpath://button[@id="script_reset_encoders"]


User Enters Value Over Max Value In Field
    [Arguments]	${input}
	Click Element	//*[@id="manual_rotation_buttons"]/div/input
	Input Text      //*[@id="manual_rotation_buttons"]/div/input    ${input}
	Click Button	//*[@id="script_rotation_position"]


User Enters Value Under Min Value In Field
    [Arguments]	${input}
	Click Element	//*[@id="manual_rotation_buttons"]/div/input
	Input Text      //*[@id="manual_rotation_buttons"]/div/input    ${input}
	Click Button	//*[@id="script_rotation_position"]


User Enters Value Max Expected Value In Field
    [Arguments]	${input}
    Click Element	//*[@id="manual_rotation_buttons"]/div/input
	Input Text      //*[@id="manual_rotation_buttons"]/div/input    ${input}
	Click Button	//*[@id="script_rotation_position"]


User Enters Value Min Expected Value In Field
    [Arguments]	${input}
    Click Element	//*[@id="manual_rotation_buttons"]/div/input
	Input Text      //*[@id="manual_rotation_buttons"]/div/input    ${input}
	Click Button	//*[@id="script_rotation_position"]


User Enters Value 100 Degrees In Field
    [Arguments]	${input}
    Click Element	//*[@id="manual_rotation_buttons"]/div/input
	Input Text      //*[@id="manual_rotation_buttons"]/div/input    ${input}
	Click Button	//*[@id="script_rotation_position"]


User Enters Value -100 Degrees In Field
    [Arguments]	${input}
    Click Element	//*[@id="manual_rotation_buttons"]/div/input
	Input Text      //*[@id="manual_rotation_buttons"]/div/input    ${input}
	Click Button	//*[@id="script_rotation_position"]


User Expects To Get A Error Messege
   Alert Should Be Present	action=ACCEPT


Check Log
    [Arguments]	 ${target_string}  ${error_code}
    ${logfile}  Get File  .dronelauncher.log
    Should Match  ${logfile}  *${target_string}*\"*${error_code}*


User Expects The Rotation To Change With Code
	[Arguments]    ${error_code}
    ${target_string} =  Set Variable  POST /app_rotation_position HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  ${error_code}


*** Test Cases ***
Rotation Value Over 180 Degrees
	[Documentation]		Change Roatation value to over max value then press GO!
	[Tags]			Roatateion over permited value
    Given Server Is Up
	When User Enters Value Over Max Value In Field  181
	Then User Expects To Get A Error Messege
    And User Expects The Rotation To Change With Code   400


Rotation Value Under -180 Degrees
	[Documentation]		Change Roatation value to under min value then press GO!
	[Tags]			Roatateion under permited value
    Given Server Is Up
	When User Enters Value Under Min Value In Field     -181
	Then User Expects To Get A Error Messege
    And User Expects The Rotation To Change With Code   400


Roatation Value 180 Degrees
	[Documentation]		Change Roatation value to max expected value then press GO!
	[Tags]			Rotation_value 180 degrees
    Given Server Is Up
	When User Enters Value Max Expected Value In Field   180
	Then User Expects The Rotation To Change With Code   500


Rotation Value -180 Degrees
	[Documentation]		Change Rotation value to min expected value then press GO!
	[Tags]			Rotation_value -180 degrees
    Given Server Is Up
	When User Enters Value Min Expected Value In Field   -180
	Then User Expects The Rotation To Change With Code   500


Rotation Value 100 degrees
	[Documentation]		Change Roatation value to 100 degrees then press GO!
	[Tags]			Rotation_value 100 degrees
    Given Server Is Up
	When User Enters Value 100 Degrees In Field     100
	Then User Expects The Rotation To Change With Code   500


Rotation Value -100 degrees
	[Documentation]		Change Rotation value to -100 degrees then press GO!
	[Tags]			Rotation_value -100 degrees
    Given Server Is Up
	When User Enters Value -100 Degrees In Field    -100
	Then User Expects The Rotation To Change With Code   500
    
