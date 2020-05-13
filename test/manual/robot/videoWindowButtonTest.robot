
*** Settings ***
Documentation    Global documentation

Library   SeleniumLibrary
Library	    ./library/getip.py
Library    Process
Library    OperatingSystem
Suite Setup    Begin Web Test
Suite Teardown    End Web Test

*** Variables ***
${BROWSER} = 		chrome
${URL} =    		http://192.168.1.155:5000
${IP} = 		return_ip
${PORT} =		5000

	
*** Keywords ***

Begin Web Test
    Open Browser	${URL}  	${BROWSER}
    Maximize Browser Window

End Web Test
    Close Browser

Server Is Up
	Wait Until Page Contains Element  id:video
    Click Button		xpath://button[@id="script_reset_encoders"]

User Clicks On Video Window
     Wait Until Page Contains Element    id:div_video
     Click Image                        id:video

User Clicks On Video Button
     Wait Until Page Contains    Video
     Click Element		id:show_video_button


User Expects The Video Window to Be Hiden and Video Button Should Show
     Wait Until Page Does Not Contain   id:div_video


User Expects Video Window to show
     Wait Until Page Contains Element    id:div_video


*** Test Cases ***

Click On Video Window
	[Documentation]		Clicking on The Video Window
	[Tags]
    Given Server Is Up
	When User Clicks On Video Window
	Then User Expects The Video Window to Be Hiden and Video Button Should Show
	
Clicks Video Button
	[Documentation]		Clicking On The Video Button
	[Tags]
    Given Server Is Up
	When User Clicks On Video Button
	Then User Expects Video Window to show

