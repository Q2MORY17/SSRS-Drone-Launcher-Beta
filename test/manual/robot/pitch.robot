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
Library         ./library/UrlLibrary.py
Resource        ./../../keywords/keywords.robot
Resource        ./../../keywords/SSRS2_keywords.robot
Resource        ./../../keywords/BobiKeywords.robot
Test Setup	Begin Web Test
Test Teardown	End Web Test


*** Variables ***
${BROWSER} =	headlesschrome


*** Keywords ***
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
    Check Log  ${function}  ${response_code}

User Expects The Pitch To Increase
    ${function} =	Set Variable  app_pitch_up
    ${response_code} =  Set Variable  500
    Check Log  ${function}  ${response_code}
	
User Expects The Pitch To Decrease
    ${function} =	Set Variable  app_pitch_down
    ${response_code} =  Set Variable  500
    Check Log  ${function}  ${response_code}

User Expects The Pitch To Change With Code
    [Arguments]    ${response_code}
    ${function} =  Set Variable  app_pitch_position
    Check Log  ${function}  ${response_code}

Then User Expects An Error Message
    Alert Should Be Present  action=ACCEPT

Check Log
    [Arguments]	 ${function}  ${response_code}  
    sleep  1	# Because chrome & headlesschrome fail otherwise
    ${output}  Terminate Process
    ${asdf} =  Set Variable  ${output.stderr}
    Process Should Be Stopped
    Should Match  ${output.stderr}  *POST /${function}*\"*${response_code}*


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

Pitch Value: Below 0 
    [Documentation]  Change pitch to arbitrary value 
    [Tags]  pitch_below_0
    Given Server Is Up
    When User Enters Value In Field  -1
    Then User Expects An Error Message
    And User Expects The Pitch To Change With Code	400
	
Pitch Value: Above 0	
    [Documentation]  Change pitch to arbitrary value 
    [Tags]  pitch_above_0
    Given Server Is Up
    When User Enters Value In Field  1
    Then User Expects The Pitch To Change With Code	500
	
Pitch Value: Below 90		
    [Documentation]  Change pitch to arbitrary value 
    [Tags]  pitch_below_90
    Given Server Is Up	
    When User Enters Value In Field  89
    Then User Expects The Pitch To Change With Code	500
	
Pitch Value: Above 90
    [Documentation]  Change pitch to arbitrary value 
    [Tags]  pitch_above_90
    Given Server Is Up	
    When User Enters Value In Field  91
    Then User Expects An Error Message
    And User Expects The Pitch To Change With Code	400

