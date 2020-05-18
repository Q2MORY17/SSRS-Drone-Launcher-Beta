*** Settings ***

Documentation     Global documentation

Library           SeleniumLibrary

Library		  ./library/getip.py

Library		  Process

Suite Setup       Begin Web Test

Suite Teardown    End Web Test





*** Variables ***

${BROWSER} =	firefox

${URL} =	http://192.168.1.127:5000

${IP} =		return_ip

${PORT} =	5000



*** Keywords ***

Begin Web Test

        Open Browser	${URL}  	${BROWSER}

Server Is Up               

	Wait Until Page Contains Element	xpath://button[@id="script_reset_encoders"]

	Page Should Contain	  		Options

	Click Button		      		xpath://button[@id="script_reset_encoders"]


User Sets Position To 200, 400

    Set Window Position  ${200}     ${400}
    ${x}                 ${y}=    Get Window Position
    Should Be Equal      ${x}     ${200}
    Should Be Equal      ${y}     ${400}



User Sets Position To 600, 400

    Set Window Position  ${600}     ${400}
    ${x}                 ${y}=    Get Window Position
    Should Be Equal      ${x}     ${600}
    Should Be Equal      ${y}     ${400}



User Sets Position To 600, 200

    Set Window Position  ${600}     ${200}
    ${x}                 ${y}=    Get Window Position
    Should Be Equal      ${x}     ${600}
    Should Be Equal      ${y}     ${200}


User Sets Resolution To 800*600

    Set Window Size	  800 	600

User Expects Window To Set The Wanted Size And All Buttons Are Visible

    Page Should Contain     Manual

    Page Should Contain     Launch

    Page Should Contain     Options

    Page Should Contain     Positions

    Page Should Contain Element      //*[@id="video"]

    Page Should Contain Element      //*[@id="script_launch_forwards"]

    Page Should Contain Element      //*[@id="script_battery_voltage"]

    Page Should Contain Element      //*[@id="script_max_pitch"]

    Page Should Contain Element      //*[@id="script_min_pitch"]

    Page Should Contain Element      //*[@id="script_stop"]

    Page Should Contain Element      //*[@id="script_pitch_up"]

    Page Should Contain Element      //*[@id="script_min_lift"]





End Web Test

    Close Browser


*** Test Cases ***

Set Screen To 600*480

    [Documentation]		Setting the screen size to 600*480 and tying out the buttons so thay are visible and clickabell
    
    [Tags]			minimize screen

    Given Server Is Up

    When User Sets Resolution To 800*600

    Then User Expects Window To Set The Wanted Size And All Buttons Are Visible


Move Screen to 200, 400
    
    [Documentation]		Moving the windows to positon x 200 to y 400

    [Tags]			minimize screen

    Given Server Is Up

    When User Sets Position To 200, 400

    Then User Expects Window To Set The Wanted Size And All Buttons Are Visible

Move Screen to 600, 400
    
    [Documentation]		Moving the windows to positon x 600 to y 400

    [Tags]			minimize screen

    Given Server Is Up

    When User Sets Position To 600, 400

    Then User Expects Window To Set The Wanted Size And All Buttons Are Visible


Move Screen to 600, 200
    
     [Documentation]		Moving the windows to positon x 600 to y 200

     [Tags]			minimize screen

     Given Server Is Up

     When User Sets Position To 600, 200

     Then User Expects Window To Set The Wanted Size And All Buttons Are Visible



