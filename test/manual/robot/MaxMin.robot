*** Settings ***
Documentation     Maximizing and Minimizing the Drone Positions
Library           SeleniumLibrary
Library	          ./library/getip.py
Library            Process
Library            OperatingSystem
Suite Setup         Begain Web Test
Suite Teardown       End Web Test

*** Variables ***
${BROWSER} =        chrome
${URL} =            http://192.168.1.172:5000
${IP}=              return ip
${PORT} =           5000
${logfile}  	    Get File  .dronelauncher.log
*** Keywords ***
Begain Web Test
    Open Browser       ${URL}        ${BROWSER}
    Maximize Browser Window
End Web Test
    Close Browser

Display Page
       Wait Until Page Contains      Positions
	   Click Button	  xpath://button[@id="script_reset_encoders"]

User Click Button Max pitch     #To maximize the pitch position
	    Start Process        echo Resetting log... > .dronelauncher.log  shell=yes
        Click Button        //*[@id="script_max_pitch"]
		${target_string} =	Set Variable  POST /app_max_pitch HTTP/1.1
		Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

User Click Button Min pitch   #to minimize the pitch position
        Start Process            echo Resetting log... > .dronelauncher.log  shell=yes
        Click Button             //*[@id="script_min_pitch"]
		${target_string} =	Set Variable  POST /app_min_pitch HTTP/1.1
		Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

User Click Button Max lift      #to maximize the lift position
       	Start Process            echo Resetting log... > .dronelauncher.log  shell=yes
        Click Button            //*[@id="script_max_lift"]
		${target_string} =	Set Variable  POST /app_max_lift HTTP/1.1
		Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

User Click Button Min lift         #to minimize the lift position
        Start Process           echo Resetting log... > .dronelauncher.log  shell=yes
        Click Button            //*[@id="script_min_lift"]
		${target_string} =	Set Variable  POST /app_min_lift HTTP/1.1
		Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
Check Log
     [Arguments]	 ${target_string}  ${error_code}
    ${logfile}  Get File  .dronelauncher.log
    Should match  ${logfile}  *${target_string}*\"*${error_code}*

*** Test Cases ***
Max pitch                   #test case for the Max position
    [Documentation]     Clicking the Positions Max pitch
    [Tags]              max_pitch
    Display Page
    User Click Button Max pitch
Min pitch                         #test case for the Min position
    [Documentation]        Clicking the Positions Min pitch
    [Tags]                  min_pitch
    Display Page
    User Click Button Min pitch

Max lift                      #test case for the  Max lift position
    [Documentation]     Clicking the Positions Max pitch
    [Tags]              max_lift
    Display Page
    User Click Button Max lift
Min lift                      #test case for the Min lift position
    [Documentation]         Clicking the Positions Min pitch
    [Tags]                  min_lift
    Display Page
    User Click Button Min lift