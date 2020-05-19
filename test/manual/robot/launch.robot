*** Settings ***
Documentation
Library                                     SeleniumLibrary
Library                                     Process
Library                                     ./library/UrlLibrary.py
Resource                                    ./../../keywords/keywords.robot
Resource                                    ./../../keywords/SSRS2_keywords.robot
Test Setup                                  Begin Web Test
Test Teardown                               End Web Test

#If you want to run the program local and python3 command is not found
#1. Make sure the Python 3 folder is present in the PATH environment variable.
#2. Locate the "python.exe" file in the Python 3 folder.
#3. Copy and Paste the "python.exe" file within the Python 3 folder.
#4. Rename the copied file to "python3" (or whatever you want the command to be).

*** Variables ***
${BROWSER} =                                headlesschrome

*** Test Cases ***
Battery Voltage Button Should Be Visible
    Gui Is Visible
    Gui Has Loaded


#Input valid value should be between 0-111
Launch input-box w/ invalid negative input
    [Tags]                                  INPUT
    Given Encoders Reset
    When Launch Input & Press Go            -1
    Then Alert Should Be Present            text=Value should be between 0 and 111
         Verify Function Is Called          app_launch_position


#Input valid value should be between 0-111
Launch input-box w/ invalid positive input
    [Tags]                                  INPUT
    Given Encoders Reset
    When Launch Input & Press Go            112
    Then Alert Should Be Present            text=Value should be between 0 and 111
         Verify Function Is Called          app_launch_position


#Input valid value should be between 0-111
Launch input-box w/ min valid input
    [Tags]                                  INPUT
    Given Encoders Reset
    When Launch Input & Press Go            0
    Then Verify Function Is Called          app_launch_position


#Input valid value should be between 0-111
Launch input-box w/ min+1 valid input
    [Tags]                                  INPUT
    Given Encoders Reset
    When Launch Input & Press Go            1
    Then Verify Function Is Called          app_launch_position


#Input valid value should be between 0-111
Launch input-box w/ max-1 valid input
    [Tags]                                  INPUT
    Given Encoders Reset
    When Launch Input & Press Go            110
    Then Verify Function Is Called          app_launch_position


#Input valid value should be between 0-111
Launch input-box w/ max valid input
    [Tags]                                  INPUT
    Given Encoders Reset
    When Launch Input & Press Go            111
    Then Verify Function Is Called          app_launch_position


Functionable Button Backwards
    [Documentation]                         Since there is no intended visible response after pressing button backwards, this testcase tests button function
    ...                                     by checking whether the action of clicking button backwards calls the targeted method function_launch_backwards()
    ...                                     in dronelauncher_python.py.
    [Tags]                                  ManualButton
    Given Encoders Reset
    When Press Button Backwards
    Then Verify Function Is Called          app_launch_backwards


Functionable Button Forwards
    [Documentation]                         Since there is no intended visible response after pressing button forwards, this testcase tests button function
    ...                                     by checking whether the action of clicking button forwards calls the targeted method function_launch_forwards()
    ...                                     in dronelauncher_python.py.
    [Tags]                                  ManualButton
    Given Encoders Reset
    When Press Button Forwards
    Then Verify Function Is Called          app_launch_forwards


Launch input-box pressing arrow up
    [Tags]                                  Arrows
    Given Encoders Reset
    When Arrow Key Input & Press Go         6      ARROW_UP+ARROW_UP+ARROW_UP    9
    Then Verify Function Is Called          app_launch_position


Launch input-box pressing arrow up max
    [Tags]                                  Arrows
    Given Encoders Reset
    When Arrow Key Input & Press Go         110    ARROW_UP+ARROW_UP+ARROW_UP+ARROW_UP+ARROW_UP    111
    Then Verify Function Is Called          app_launch_position


Launch input-box pressing arrow down
    [Tags]                                  Arrows
    Given Encoders Reset
    When Arrow Key Input & Press Go         4    ARROW_DOWN+ARROW_DOWN+ARROW_DOWN     1
    Then Verify Function Is Called          app_launch_position


Launch input-box pressing arrow down max
    [Tags]                                  Arrows
    Given Encoders Reset
    When Arrow Key Input & Press Go         2    ARROW_DOWN+ARROW_DOWN+ARROW_DOWN+ARROW_DOWN+ARROW_DOWN     0
    Then Verify Function Is Called          app_launch_position