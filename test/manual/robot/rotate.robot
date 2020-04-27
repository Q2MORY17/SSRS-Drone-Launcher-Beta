*** Settings ***

Documentation    Global documentation

Library          SeleniumLibrary

Library		./library/getip.py

Library		 Process

Suite Setup       Begin Web Test

Suite Teardown    End Web Test





*** Variables ***

${BROWSER} =		chrome

${URL} =    		http://192.168.1.12:5000

${IP} = 		return_ip

${PORT} =		5000

*** Keywords ***

Begin Web Test

      Open Browser	${URL}  	${BROWSER}

      Maximize Browser Window



End Web Test

	Close Browser



Server Is Up

	Wait Until Page Contains Element	//*[@id="script_rotation_right"]
	Page Should Contain	Rotation

	Click Button		xpath://button[@id="script_reset_encoders"]


User Clicks Button Rotation Right

	Click Button	//*[@id="script_rotation_right"]



User Clicks Button Rotation Left

	Click Button	//*[@id="script_rotation_left"]



User Enters Value In Field

	Click Element	//*[@id="manual_rotation_buttons"]/div/input

	Input Text      //*[@id="manual_rotation_buttons"]/div/input  23




User presses up arrow in textfeild

    Click Element	//*[@id="manual_rotation_buttons"]/div/input

    Press Keys  //*[@id="manual_rotation_buttons"]/div/input     ARROW_UP    ARROW_UP    ARROW_UP

    Click Button	//*[@id="script_rotation_position"]



User presses down arrow in textfeild

    Click Element	//*[@id="manual_rotation_buttons"]/div/input

    Press Keys  //*[@id="manual_rotation_buttons"]/div/input     ARROW_DOWN    ARROW_DOWN    ARROW_DOWN

    Click Button	//*[@id="script_rotation_position"]



User Expects The Rotor To Rotate To The Right

	Page Should Contain	Rotation	# Placeholder for Gherkin



User Expects The Rotor To Rotate To The Left

	Page Should Contain	Rotation	# Placeholder for Gherkin



User Expects The Rotor To Move

	Page Should Contain	Rotation	# Placeholder for Gherkin







*** Test Cases ***



Roatate To The Right

	[Documentation]		Clicking the Roatate to the Right

	[Tags]			Rotation_Right

    Given Server Is Up

	When User Clicks Button Rotation Right

	Then User Expects The Rotor To Rotate To The Right



Roatate To The Left

	[Documentation]		Clicking the Roatation_Left button

	[Tags]			Roatate_Left

    Given Server Is Up

	When User Clicks Button Rotation Left

	Then User Expects The Rotor To Rotate To The Left



Pitch Value

	[Documentation]		Change Roatation value then press GO!

	[Tags]			Roatateion_value

    Given Server Is Up

	When User Enters Value In Field

	Then User Expects The Rotor To Move



Pitch Value change manuly up

	[Documentation]		Change Roatation value manualy by pressing upp arrow in textfield then press GO!

	[Tags]			Roatateion_value manualy changing

    Given Server Is Up

	When User presses up arrow in textfeild

	Then User Expects The Rotor To Move


Pitch Value change manuly down

	[Documentation]		Change Roatation value manualy by pressing upp arrow in textfield then press GO!

	[Tags]			Roatateion_value manualy changing

    Given Server Is Up

	When User presses down arrow in textfeild

	Then User Expects The Rotor To Move