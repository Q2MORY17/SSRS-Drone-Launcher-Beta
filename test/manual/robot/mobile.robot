
*** Settings ***
Documentation	Global documentation
Library		./library/getip.py
Library		Process
Library         OperatingSystem	
Library         AppiumLibrary


*** Variables ***
${BROWSER} =		firefox
${URL} =   		http://192.168.0.4:5000
${PORT} =		5000
${logfile}  		Get File	.dronelauncher.log

${APPIUM_URL}           http://localhost:4723/wd/hub
${PLATFORM_NAME}        Android
${PLATFORM_VERSION}     10
${DEVICE_NAME}          emulator-5554
${APP_LOCATION}         
${AUTOMATION_NAME}	UiAutomator2
${APP_PKG}		com.android.chrome
${APP_ACT}		com.google.android.apps.chrome.Main

*** Keywords ***

Server Is Up 
	Go To Url	${URL}
	Wait Until Page Contains      Pitch
	Click Element		//android.widget.Button[contains(@resource-id,'script_reset_encoders')]

User Clicks Button Pitch Up
     	Wait Until Element Is Visible  //android.widget.Button[contains(@resource-id,'script_pitch_up')]  timeout=5	
	Click Element		//android.widget.Button[contains(@resource-id,'script_pitch_up')]

User Clicks Button Pitch Down
     	Wait Until Element Is Visible  //android.widget.Button[contains(@resource-id,'script_pitch_down')]  timeout=5		
	Click Element		//android.widget.Button[contains(@resource-id,'script_pitch_down')]
	
User Enters Value In Field
	[Arguments]	${input}
     	Wait Until Element Is Visible  //android.widget.Button[contains(@resource-id,'script_pitch_position')]  timeout=5		
	Input Text	//android.widget.EditText[contains(@index,'0')]  ${input}	
	Click Element	//android.widget.Button[contains(@resource-id,'script_pitch_position')]

User Expects The Pitch To Increase
     	${target_string} =	Set Variable	POST /app_pitch_up HTTP/1.1
	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
    	${target_string} =	Set Variable  POST /app_pitch_stop HTTP/1.1
    	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

User Expects The Pitch To Decrease
     	${target_string} =	Set Variable	POST /app_pitch_down HTTP/1.1
	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500	
    	${target_string} =	Set Variable  POST /app_pitch_stop HTTP/1.1
    	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

User Expects The Pitch To Change With Code
        [Arguments]    ${error_code}
    	${target_string} =  Set Variable  POST /app_pitch_position HTTP/1.1
    	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  ${error_code}

Then User Expects An Error Message
	Wait Until Element Is Visible  //android.widget.TextView[contains(@resource-id,'id/message')]  timeout=20
	Click Element		//android.widget.Button[contains(@resource-id,'id/button1')]

Check Log
	[Arguments]	${target_string}  ${error_code}
        ${logfile}	Get File	.dronelauncher.log
	Should Match   ${logfile}	*${target_string}*\"*${error_code}*

Mobile Chrome Settings
	Open Application  ${APPIUM_URL}  platformName=${PLATFORM_NAME}  platformVersion=${PLATFORM_VERSION}  deviceName=${DEVICE_NAME}  app=${APP_LOCATION}  automationName=${AUTOMATION_NAME}  appPackage=${APP_PKG}  appActivity=${APP_ACT}

Mobile Firefox Settings
	${APP_PKG} =	  Set variable  	org.mozilla.firefox
	${APP_ACT} =  	  Set Variable		org.mozilla.gecko.BrowserApp
	Open Application  ${APPIUM_URL}  platformName=${PLATFORM_NAME}  platformVersion=${PLATFORM_VERSION}  deviceName=${DEVICE_NAME}  app=${APP_LOCATION}  automationName=${AUTOMATION_NAME}  appPackage=${APP_PKG}  appActivity=${APP_ACT}
	
	
*** Test Cases ***

Mobile Pitch Up
	[Documentation]		Clicking "pitch up"-button
	[Tags]			pitch_up
	Mobile Firefox Settings
	Given Server Is Up
	When User Clicks Button Pitch Up
	Then User Expects The Pitch To Increase

Mobile Pitch Down
	[Documentation]		Clicking "pitch down"-button
	[Tags]			pitch_down
	Mobile Firefox Settings
	Given Server Is Up
	When User Clicks Button Pitch Down
	Then User Expects The Pitch To Decrease

Mobile Pitch Value
	[Documentation]		Change pitch value arbitrarily
	[Tags]			pitch_value
	Mobile Firefox Settings
     	Given Server Is Up
	When User Enters Value In Field  -1
	Then User Expects An Error Message
	User Expects The Pitch To Change With Code	400
	When User Enters Value In Field  1
	User Expects The Pitch To Change With Code	500	
	When User Enters Value In Field  89
	User Expects The Pitch To Change With Code	500	
	When User Enters Value In Field  91
	Then User Expects An Error Message
	User Expects The Pitch To Change With Code	400
	