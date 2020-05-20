*** Settings ***
Documentation       Global documentation
Library             SeleniumLibrary
Library             Process
Library             ./library/UrlLibrary.py
Library              OperatingSystem
Resource            ./../../keywords/keywords.robot
Resource            ./../../keywords/SSRS2_keywords.robot
Resource            ./../../keywords/BobiKeywords.robot
Test Setup          Begin Web Test
Test Teardown       End Web Test


*** Variables ***
${BROWSER} =    headlessfirefox

*** Test Cases ***


Roatate To The Right
    [Documentation]		Clicking the Rotation_right button
    [Tags]                                  Rotation_Right
    Given Encoders Reset
    When User Clicks Button Rotation Right
    Then Verify Function Is Called      app_rotation_right

Roatate To The Left
    [Documentation]		Clicking the Rotation_Left button
    [Tags]                                  Rotate_Left
    Given Encoders Reset
    When User Clicks Button Rotation Left
    Then Verify Function Is Called      app_rotation_left

Rotation Value
	[Documentation]		Change Rotation value then press GO!
	[Tags]			Rotation_value
    Given Encoders Reset
    When User Enters Value In Field  23
    Then Verify Function Is Called          app_rotation_position

Rotation Value change manuly up
	[Documentation]		Change Rotation value manualy by pressing upp arrow in textfield then press GO!
	[Tags]			Rotation_value manualy changing
    Given Encoders Reset
    When User presses up arrow in textfeild
    Then Verify Function Is Called          app_rotation_position

Rotation Value change manuly down
	[Documentation]		Change Rotation value manualy by pressing upp arrow in textfield then press GO!
	[Tags]			Rotation_value manualy changing
    Given Encoders Reset
    When User presses down arrow in textfeild
    Then Verify Function Is Called          app_rotation_position

Roatation Value over 180 degrees
	[Documentation]		Change Rotation value to over max value then press GO!
	[Tags]			Rotation over permited value
     Given Encoders Reset
     When User Enters Value Under Min Value In Field     -181
     Then User Expects To Get A Error Messege
     And Verify Function Is Called          app_rotation_position

Roatation Value under -180 degrees
	[Documentation]		Change Rotation value to under min value then press GO!
	[Tags]			Rotation under permited value
    Given Encoders Reset
    When User Enters Value Under Min Value In Field     -181
	Then User Expects To Get A Error Messege
	And Verify Function Is Called          app_rotation_position

Roatation Value 180 degrees
    [Documentation]		Change Rotation value to max exepted value then press GO!
	[Tags]			Rotation_value 180 degrees
    Given Encoders Reset
    When User Enters Value Max Exepted Value In Field   180
    Then Verify Function Is Called          app_rotation_position

Roatation Value -180 degrees
	[Documentation]		Change Rotation value to min exepted value then press GO!
	[Tags]			Rotation_value -180 degrees
	Given Encoders Reset
	When User Enters Value 100 degrees In Field     100
	Then Verify Function Is Called          app_rotation_position

Roatation Value -100 degrees
	[Documentation]		Change Rotation value to -100 degrees then press GO!
	[Tags]			Rotation_value -100 degrees
	Given Encoders Reset
	When User Enters Value -100 Degrees In Field    -100
	Then Verify Function Is Called          app_rotation_position
