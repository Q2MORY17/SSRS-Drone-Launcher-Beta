*** Settings ***

Documentation     Global documentation

Library           SeleniumLibrary

Library		  ./library/getip.py

Library		  Process

Suite Setup       Begin Web Test

Suite Teardown    End Web Test





*** Variables ***

${BROWSER} =	firefox

${URL} =	http://192.168.1.155:5000

${IP} =		return_ip

${PORT} =	5000

*** Keywords ***

Begin Web Test

	Open Browser	${URL}  	${BROWSER}

    	Maximize Browser Window

Server Is Up

	Wait Until Page Contains Element	xpath://button[@id="script_reset_encoders"]

	Page Should Contain	  		Options

	Click Button				xpath://button[@id="script_reset_encoders"]

User Sets Resolution To Half

       ${width}    ${height} =         Get Window Size

       ${result} =  Convert To Number   ${width}

       ${width2} =     Evaluate        ${result}/2

       Set Window Size	               ${width2}  	${height}

       ${width}    ${height2} =        Get Window Size

       Should Be Equal  ${width}    ${width2}
       Should Be Equal  ${height}   ${height2}

       Sleep  3

User Expects Window To Set To Half Size And All Buttons Are Visible

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

Set Screen To Half

       [Documentation]		    Setting the screen size to Half and tying out the buttons so thay are visible and click abell
       [Tags]			    minimize screen

       Given Server Is Up

       When User Sets Resolution To Half

       Then User Expects Window To Set To Half Size And All Buttons Are Visible






