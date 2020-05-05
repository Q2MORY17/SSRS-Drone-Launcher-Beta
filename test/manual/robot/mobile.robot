

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
	BuiltIn.Sleep 	5
#	AppiumLibrary.Wait Until Page Contains Element		driver.findElement(By.xpath('//button[@id="script_pitch_up"]'))
	AppiumLibrary.Wait Until Page Contains Element		xpath://button[@id="script_pitch_up"]
	Page Should Contain	Pitch
#	Click Button		xpath://button[@id="script_reset_encoders"]

User Clicks Button Pitch Up
	AppiumLibrary.Click Button	xpath://*[@id="script_pitch_up"]

User Expects The Pitch To Increase
     	${target_string} =	Set Variable	POST /app_pitch_up HTTP/1.1
	Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}
	
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

Mobile Chrome Test
	[Documentation]		A
	[Tags]			mobile_chrome
	Mobile Chrome Settings
	Go To Url	http://192.168.0.4:5000

Mobile Firefox Test
	[Documentation]		B
	[Tags]			mobile_firefox
	Mobile Firefox Settings
	Given Server Is Up
	When User Clicks Button Pitch Up	
#	Then User Expects The Pitch To Increase

