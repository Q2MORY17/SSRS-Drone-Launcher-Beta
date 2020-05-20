#
#	Change all references of error code 500 to 200 when running
#	test on a real system. Response code 500 is used as the development
#	server can't find the resources. When connected to a pi the response
#	should be 200 rather than 500.
#
	
*** Settings ***
Documentation	Check functionality of buttons and input fields.
Library		SeleniumLibrary
Library		Process
Library         OperatingSystem	
Library         ./library/UrlLibrary.py
#Resource        ./../../keywords/keywords.robot
#Resource        ./../../keywords/SSRS2_keywords.robot
#Resource        ./../../keywords/BobiKeywords.robot
Test Setup	Begin Web Test
Test Teardown	End Web Test


*** Variables ***
${BROWSER} =	firefox
#${URL} =   	http://192.168.0.4:5000
#${PORT} =	5000
#${logfile}  	Get File  .dronelauncher.log


*** Keywords ***
# Begin Web Test
#     Open Browser  ${URL}  ${BROWSER}
#     Maximize Browser Window

# End Web Test
#     Close Browser

#################################################################################
	
End Web Test
    Close Browser
    Terminate All Processes

Encoders Reset
    Click Button                            id:script_reset_encoders

Verify Function Is Called
    [Arguments]                             ${function}
    ${result}                               Terminate Process
    Process Should Be Stopped
    Should Match                          ${result.stderr}  *POST /${function} HTTP/1.1*

Begin Web Test
    [Documentation]                         You need to import UrlLibrary.py inside the robot file that you working from
    ${URL}=                                 Get Url
    Start Process                           python3   ./python/dronelauncher_python.py    shell=True
    Open Browser                            about:blank     ${BROWSER}
    Maximize Browser Window
    Go To                                   ${URL}

#################################################################################

Server Is Up 
    Wait Until Page Contains Element  xpath://button[@id="script_pitch_up"]
    Page Should Contain  Pitch
    Click Button  xpath://button[@id="script_reset_encoders"]

User Clicks Button Pitch Up
    Click Button  xpath://button[@id="script_pitch_up"]

User Clicks Button Pitch Down
    Click Button  xpath://button[@id="script_pitch_down"]

User Enters Value In Field
    [Arguments]	${input}
    Click Element  xpath://input[@class="form-2" and @name="pitch_position"]
    Input Text  xpath://input[@class="form-2" and @name="pitch_position"]  ${input}
    Click Button  xpath://button[@id="script_pitch_position"]

Check Function Halts
    [Arguments]  ${function}
    ${response_code} =  Set Variable  500
    Wait Until Keyword Succeeds  6x  200ms  Check Log2  ${function}  ${response_code}

User Expects The Pitch To Increase
    ${function} =	Set Variable  app_pitch_up
    ${response_code} =  Set Variable  500
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${function}  ${response_code}

	
User Expects The Pitch To Decrease
    ${function} =	Set Variable  app_pitch_down
    ${response_code} =  Set Variable  500
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${function}  ${response_code}


User Expects The Pitch To Change With Code
    [Arguments]    ${response_code}
    ${function} =  Set Variable  app_pitch_position
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${function}  ${response_code}

Then User Expects An Error Message
    Alert Should Be Present  action=ACCEPT

Check Log
    [Arguments]	 ${function}  ${response_code}  
    ${output}  Terminate Process
    ${asdf} =  Set Variable  ${output.stderr}
    Process Should Be Stopped
    Should Match  ${output.stderr}  *POST /${function}*\"*${response_code}*
#    Should Match  ${output.stderr}  *POST /app_pitch_stop*\"*${response_code}*
#    LogToConsole  ${asdf}
	


*** Test Cases ***

Pitch Up
    [Documentation]  Clicking the "Pitch up"-button.
    [Tags]  pitch_up
    Given Server Is Up 
    When User Clicks Button Pitch Up
    User Expects The Pitch To Increase
	
Pitch Down
    [Documentation]  Clicking the "pitch down"-button
    [Tags]  pitch_down
    Given Server Is Up
    When User Clicks Button Pitch Down
    Then User Expects The Pitch To Decrease

Pitch Value: Negative1 
    [Documentation]  Change pitch value arbitrarily
    [Tags]  pitch_negative1
    Given Server Is Up
    When User Enters Value In Field  -1
    Then User Expects An Error Message
    And User Expects The Pitch To Change With Code	400
	
Pitch Value: Positive	
    [Documentation]  Change pitch value to positive value
    [Tags]  pitch_positive1
    Given Server Is Up
    When User Enters Value In Field  1
    Then User Expects The Pitch To Change With Code	500
	
Pitch Value: Positive2		
    [Documentation]  Change pitch value to positive value
    [Tags]  pitch_positive2
    Given Server Is Up	
    When User Enters Value In Field  89
    Then User Expects The Pitch To Change With Code	500
	
Pitch Value: Negative2 	
    [Documentation]  Change pitch value to positive value
    [Tags]  pitch_negative2
    Given Server Is Up	
    When User Enters Value In Field  91
    Then User Expects An Error Message
    And User Expects The Pitch To Change With Code	400







