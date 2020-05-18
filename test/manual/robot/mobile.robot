

*** Settings ***
Documentation	Global documentation
#Library		SeleniumLibrary
Library		./library/getip.py
Library		Process
Library         OperatingSystem	
Library         AppiumLibrary
#Force Tags      demo
#Suite Setup	Begin Web Test
#Suite Teardown	End Web Test


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
#Begin Web Test

#End Web Test


Server Is Up 
	Go To Url	${URL}
	Wait Until Page Contains      Pitch
#	Click Element		//android.widget.Button[contains(@resource-id,'script_pitch_up')]

User Clicks Button Pitch Up
	Click Element		//android.widget.Button[contains(@resource-id,'script_pitch_up')]

User Clicks Button Pitch Down
	Click Element		//android.widget.Button[contains(@resource-id,'script_pitch_down')]
	
User Enters Value In Field
	[Arguments]	${input}
#	Click Element	xpath://input[@class="form-2" and @name="pitch_position"]
	Input Text	//android.widget.EditText[contains(@index,'0')]  ${input}	
	Click Element	//android.widget.Button[contains(@resource-id,'script_pitch_position')]

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
#        Alert Should Be Present		action=ACCEPT
 	Wait Until Page Contains		Value should be between 0 and 90	timeout=10
	Page Should Contain Text		Value should be between 0 and 90
	Click Element		//android.widget.Button[contains(@resource-id,'android:id/button1')]
	 
Check Log
	[Arguments]	${target_string}
        ${logfile}	Get File	.dronelauncher.log
	Should Contain   ${logfile}	${target_string}

Mobile Chrome Settings
	Open Application  ${APPIUM_URL}  platformName=${PLATFORM_NAME}  platformVersion=${PLATFORM_VERSION}  deviceName=${DEVICE_NAME}  app=${APP_LOCATION}  automationName=${AUTOMATION_NAME}  appPackage=${APP_PKG}  appActivity=${APP_ACT}

Mobile Firefox Settings
	${APP_PKG} =	  Set variable  	org.mozilla.firefox
	${APP_ACT} =  	  Set Variable		org.mozilla.gecko.BrowserApp
	Open Application  ${APPIUM_URL}  platformName=${PLATFORM_NAME}  platformVersion=${PLATFORM_VERSION}  deviceName=${DEVICE_NAME}  app=${APP_LOCATION}  automationName=${AUTOMATION_NAME}  appPackage=${APP_PKG}  appActivity=${APP_ACT}

	
	
*** Test Cases ***

Mobile Pitch Up
	[Documentation]		B
	[Tags]			mobile_pitch_up
	Mobile Firefox Settings
	Server Is Up
	User Clicks Button Pitch Up
	User Expects The Pitch To Increase

Mobile Pitch Down
	[Documentation]		B
	[Tags]			mobile_pitch_down
	Mobile Firefox Settings
	Server Is Up
	User Clicks Button Pitch Up
	User Expects The Pitch To Increase

Mobile Pitch Value
	[Documentation]		Change pitch value arbitrarily
	[Tags]			mobile_pitch_value
	Mobile Firefox Settings
     	Given Server Is Up
	When User Enters Value In Field  -1
	Then User Expects An Error Message
	When User Enters Value In Field  1
	When User Enters Value In Field  89
	When User Enters Value In Field  91
	Then User Expects An Error Message