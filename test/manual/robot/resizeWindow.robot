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



User Sets Resolution To 1920*1200

    Set Window Size	  1920 	1200

User Sets Resolution To 1920*1080

    Set Window Size	  1920 	1080


User Sets Resolution To 1600*900

    Set Window Size     1600  900


User Sets Resolution To 1280*1024

    Set Window Size     1280  1024


User Sets Resolution To 1280*800

    Set Window Size     1280  800


User Sets Resolution To 1024*768

    Set Window Size     1024  768


User Sets Resolution To 800*600

    Set Window Size     800   600


User Sets Resolution To 640*480

    Set Window Size      640  480

User Sets Resolution To 2650*1440

    Set Window Size	  2650 	1440

User Sets Resolution To 3840*2160

    Set Window Size	  3840	2160

User Sets Resolution To 4096*2160

    Set Window Size	  4096 	2160


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


Server Is Up

	Wait Until Page Contains Element	xpath://button[@id="script_reset_encoders"]

	Page Should Contain	  Options

	Click Button		xpath://button[@id="script_reset_encoders"]


*** Test Cases ***

Set Screen To 1920*1200

	[Documentation]		Setting the screen size to 1920*1200 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 1920*1200

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible



Set Screen To 1600*900

	[Documentation]		Setting the screen size to 1600*900 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 1600*900

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible



Set Screen To 1280*1024

	[Documentation]		Setting the screen size to 1280*1024 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 1280*1024

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible



Set Screen To 1280*800

	[Documentation]		Setting the screen size to 1280*800 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 1280*800

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible



Set Screen To 1024*768

	[Documentation]		Setting the screen size to 1024*768 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 1024*768

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible



Set Screen To 800*600

	[Documentation]		Setting the screen size to 800*600 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 800*600

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible



Set Screen To 640*480

	[Documentation]		Setting the screen size to 640*480 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 640*480

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible


Set Screen To 2650*1440

	[Documentation]		Setting the screen size to 2650*1440 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 2650*1440

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible


Set Screen To 3840*2160

	[Documentation]		Setting the screen size to 3840*2160 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 3840*2160

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible


Set Screen To 4096*2160

	[Documentation]		Setting the screen size to 4096*2160 and tying out the buttons so thay are visible and clickabell

	[Tags]			minimize screen

    Given Server Is Up

	When User Sets Resolution To 4096*2160

	Then User Expects Window To Set The Wanted Size And All Buttons Are Visible
