*** Settings ***

Documentation    Global documentation

Library          SeleniumLibrary

Library		./library/getip.py

Library		 Process

Suite Setup       Begin Web Test

Suite Teardown    End Web Test





*** Variables ***

${BROWSER} =		chrome

${URL} =    		http://192.168.1.127:5000

${IP} = 		return_ip

${PORT} =		5000

*** Keywords ***

Begin Web Test

      Open Browser	${URL}  	${BROWSER}

      Maximize Browser Window

User Clicks Minimize Screen Button

    ${width}	${height}=	Get Window Size

    Set Window Size	  800 	600

User Expects The Window To Be Smaller
    ${width}	${height}=	Get Window Size
   Should Be Equal	 ${width} =  '800'
   Should Be Equal  ${height}  =  '600'
End Web Test

	Close Browser



Server Is Up

	Wait Until Page Contains Element	xpath://button[@id="script_reset_encoders"]

	Page Should Contain	  Options

	Click Button		xpath://button[@id="script_reset_encoders"]


*** Test Cases ***



Roatate To The Right

	[Documentation]		Clicking the minimize screen button

	[Tags]			minimize screen

    Given Server Is Up

	When User Clicks Minimize Screen Button

	Then User Expects The Window To Be Smaller

