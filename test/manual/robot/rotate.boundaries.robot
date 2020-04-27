*** Settings ***

Documentation   Global documentation

Library     SeleniumLibrary

Library     ./library/getip.py

Library     Process

Suite Setup  Begin Web Test

Suite Teardown   End Web Test





*** Variables ***

${BROWSER} =    chrome

${URL} =    http://192.168.1.12:5000

${IP} =     return_ip

${PORT} =   5000

*** Keywords ***

Begin Web Test

      Open Browser      ${URL}  	${BROWSER}

      Maximize Browser Window



End Web Test

	Close Browser



Server Is Up

	Wait Until Page Contains Element	//*[@id="script_rotation_right"]

	Page Should Contain	Rotation

	Click Button		xpath://button[@id="script_reset_encoders"]


User Enters Value Over Max Value In Field

	Click Element	//*[@id="manual_rotation_buttons"]/div/input

	Input Text      //*[@id="manual_rotation_buttons"]/div/input  181

	Click Button	//*[@id="script_rotation_position"]


User Enters Value Under Min Value In Field

	Click Element	//*[@id="manual_rotation_buttons"]/div/input

	Input Text      //*[@id="manual_rotation_buttons"]/div/input  -181

	Click Button	//*[@id="script_rotation_position"]


User Enters Value Max Exepted Value In Field
    Click Element	//*[@id="manual_rotation_buttons"]/div/input

	Input Text      //*[@id="manual_rotation_buttons"]/div/input  180

	Click Button	//*[@id="script_rotation_position"]


User Enters Value Min Exepted Value In Field
    Click Element	//*[@id="manual_rotation_buttons"]/div/input

	Input Text      //*[@id="manual_rotation_buttons"]/div/input  -180

	Click Button	//*[@id="script_rotation_position"]


User Enters Value 100 degrees In Field
    Click Element	//*[@id="manual_rotation_buttons"]/div/input

	Input Text      //*[@id="manual_rotation_buttons"]/div/input  100

	Click Button	//*[@id="script_rotation_position"]


User Enters Value -100 degrees In Field
    Click Element	//*[@id="manual_rotation_buttons"]/div/input

	Input Text      //*[@id="manual_rotation_buttons"]/div/input  -100

	Click Button	//*[@id="script_rotation_position"]


User Expects To Get A Error Messege

   Alert Should Be Present	action=ACCEPT


User Expects The Rotor To Move Max To The Right

    Page Should Contain	Rotation	# Placeholder for Gherkin


User Expects The Rotor To Move Max To The Left

    Page Should Contain	Rotation	# Placeholder for Gherkin


User Expects The Rotor To Move 100 Degrees To The Rigt

    Page Should Contain	Rotation	# Placeholder for Gherkin

User Expects The Rotor To Move 100 Degrees To The Left

    Page Should Contain	Rotation	# Placeholder for Gherkin



*** Test Cases ***


Roatation Value over 180 degrees

	[Documentation]		Change Roatation value to over max value then press GO!

	[Tags]			Roatateion over permited value

    Given Server Is Up

	When User Enters Value Over Max Value In Field

	Then User Expects To Get A Error Messege


Roatation Value under -180 degrees

	[Documentation]		Change Roatation value to under min value then press GO!

	[Tags]			Roatateion under permited value

    Given Server Is Up

	When User Enters Value Under Min Value In Field

	Then User Expects To Get A Error Messege


Roatation Value 180 degrees

	[Documentation]		Change Roatation value to max exepted value then press GO!

	[Tags]			Roatateion_value 180 degrees

    Given Server Is Up

	When User Enters Value Max Exepted Value In Field

	Then User Expects The Rotor To Move Max To The Right



Roatation Value -180 degrees

	[Documentation]		Change Roatation value to min exepted value then press GO!

	[Tags]			Roatateion_value -180 degrees

    Given Server Is Up

	When User Enters Value Min Exepted Value In Field

	Then User Expects The Rotor To Move Max To The Left



Roatation Value 100 degrees

	[Documentation]		Change Roatation value to 100 degrees then press GO!

	[Tags]			Roatateion_value 100 degrees

    Given Server Is Up

	When User Enters Value 100 degrees In Field

	Then User Expects The Rotor To Move 100 Degrees To The Rigt



Roatation Value -100 degrees

	[Documentation]		Change Roatation value to -100 degrees then press GO!

	[Tags]			Roatateion_value -100 degrees

    Given Server Is Up

	When User Enters Value -100 Degrees In Field

	Then User Expects The Rotor To Move 100 Degrees To The Left
