*** Settings ***
Documentation       Global documentation
Library             SeleniumLibrary
Library             Process
Library             ./library/UrlLibrary.py
Resource            ./../../keywords/keywords.robot
Resource            ./../../keywords/SSRS2_keywords.robot
Resource            ./../../keywords/BobiKeywords.robot
Test Setup          Begin Web Test
Test Teardown       End Web Test

#If you want to run the program local and python3 command is not found
#1. Make sure the Python 3 folder is present in the PATH environment variable.
#2. Locate the "python.exe" file in the Python 3 folder.
#3. Copy and Paste the "python.exe" file within the Python 3 folder.
#4. Rename the copied file to "python3" (or whatever you want the command to be).

*** Variables ***
${BROWSER} =    headlesschrome

*** Test Cases ***


Roatate To The Right
    [Documentation]		Clicking the Roatation_right button
    [Tags]                                  Rotation_Right
    Given Encoders Reset
    When User Clicks Button Rotation Right
    Then Verify Function Is Called      app_rotation_right


Roatate To The Left
    [Documentation]		Clicking the Roatation_Left button
    [Tags]                                  Roatate_Left
    Given Encoders Reset
    When User Clicks Button Rotation Left
    Then Verify Function Is Called      app_rotation_left


Rotation Value##########################
	[Documentation]		Change Roatation value then press GO!
	[Tags]			Roatateion_value
    Given Encoders Reset
    When User Enters Value In Field  23
    Then Verify Function Is Called          app_launch_position


Rotation Value change manuly up
	[Documentation]		Change Roatation value manualy by pressing upp arrow in textfield then press GO!
	[Tags]			Roatateion_value manualy changing
    Given Encoders Reset
    When User presses up arrow in textfeild
    Then Verify Function Is Called          app_launch_position


Rotation Value change manuly down
	[Documentation]		Change Roatation value manualy by pressing upp arrow in textfield then press GO!
	[Tags]			Roatateion_value manualy changing
    Given Encoders Reset
    When User presses down arrow in textfeild
    Then Verify Function Is Called          app_launch_position


