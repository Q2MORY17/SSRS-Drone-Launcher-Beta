
*** Settings ***
Documentation    Global documentation

Library          SeleniumLibrary
Library		 ./library/getip.py
Library		 Process
Suite Setup	 Begin Web Test
Suite Teardown	 End Web Test




*** Variables ***
${BROWSER} = 		firefox
${URL} =    		http://192.168.1.15:5000
${IP} = 		return_ip
${PORT} =		5000

	
*** Keywords ***

Begin Web Test
      ${VAR} =  return_ip
      Start Process  ./resources/start_server.sh  shell=yes
      Open Browser	${URL}  	${BROWSER}
      Maximize Browser Window

End Web Test
#	Terminate Process
	Close Browser



Server Is Up 
	Wait Until Page Contains Element	xpath://button[@id="script_lift_up"]
	Page Should Contain	lift
	Click Button		xpath://button[@id="script_reset_encoders"]

User Clicks Button Lift Up
	Click Button	xpath://button[@id="script_lift_up"]

User Clicks Button Lift Down
	Click Button	xpath://button[@id="script_lift_down"]

User Enters Value In Field
	[Arguments]	${input}				 
	Click Element	xpath://input[@class="form-3" and @name="lift_position"]
	Input Text	xpath://input[@class="form-3" and @name="lift_position"]  ${input}
	Click Button	xpath://button[@id="script_lift_position"]


User Expects The Lift To Increase
	Page Should Contain	Lift	# Placeholder for Gherkin

User Expects The Lift To Decrease
	Page Should Contain	Lift	# Placeholder for Gherkin

User Expects The Lift To Change
	Page Should Contain	Lift	# Placeholder for Gherkin
Then User Expects An Error Message
        Alert Should Be Present		action=ACCEPT

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
	When User Enters Value In Field  130
	When User Enters Value In Field  20
	When User Enters Value In Field  -1
	Then User Expects An Error Message							   
