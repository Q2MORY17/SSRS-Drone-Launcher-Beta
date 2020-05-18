*** Settings ***
Documentation
Library                                     SeleniumLibrary
Library                                     Process
Library                                     ./library/UrlLibrary.py
Resource                                    ./../../keywords/keywords.robot
Test Setup                                  Begin Web Test
Test Teardown                               End Web Test

*** Variables ***
${BROWSER} =                                headlesschrome

*** Keywords ***
#If you want to run the program local and python3 command is not found
#1. Make sure the Python 3 folder is present in the PATH environment variable.
#2. Locate the "python.exe" file in the Python 3 folder.
#3. Copy and Paste the "python.exe" file within the Python 3 folder.
#4. Rename the copied file to "python3" (or whatever you want the command to be).
End Web Test
    Close Browser
    Terminate All Processes

Gui Is Visible
    Wait Until Page Contains Element        id=video

Gui Has Loaded
    Page Should Contain Element             id=script_battery_voltage

Encoders Reset
    Click Button                            id:script_reset_encoders

Press Button Backwards
    Click Button                            id:script_launch_backwards
    Sleep                                   1

Press Button Forwards
    Click Button                            id:script_launch_forwards
    Sleep                                   1

Launch Input
    [Arguments]                             ${number}
    Input Text                              name:launch_position  ${number}

Click Go
    Click Button                            id:script_launch_position
    Sleep                                   1

*** Test Cases ***
Battery Voltage Button Should Be Visible
    Gui Is Visible
    Gui Has Loaded


#Input valid value should be between 0-111
Launch input-box w/ invalid negative input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            -1
    Click Go
    Alert Should Be Present                 text=Value should be between 0 and 111
    Verify Function Is Called               POST /app_launch_position HTTP/1.1


#Input valid value should be between 0-111
Launch input-box w/ invalid positive input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            112
    Click Go
    Alert Should Be Present                 text=Value should be between 0 and 111
    Verify Function Is Called               POST /app_launch_position HTTP/1.1


#Input valid value should be between 0-111
Launch input-box w/ min valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            0
    Click Go
    Verify Function Is Called               POST /app_launch_position HTTP/1.1


#Input valid value should be between 0-111
Launch input-box w/ min+1 valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            1
    Click Go
    Verify Function Is Called               POST /app_launch_position HTTP/1.1


#Input valid value should be between 0-111
Launch input-box w/ max-1 valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            110
    Click Go
    Verify Function Is Called               POST /app_launch_position HTTP/1.1


#Input valid value should be between 0-111
Launch input-box w/ max valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            111
    Click Go
    Verify Function Is Called               POST /app_launch_position HTTP/1.1


Functionable Button Backwards
    [Documentation]                         Since there is no intended visible response after pressing button backwards, this testcase tests button function
    ...                                     by checking whether the action of clicking button backwards calls the targeted method function_launch_backwards()
    ...                                     in dronelauncher_python.py.
    [Tags]                                  ManualButton
    Given Encoders Reset
    When Press Button Backwards
    Then Verify Function Is Called          POST /app_launch_backwards HTTP/1.1


Functionable Button Forwards
    [Documentation]                         Since there is no intended visible response after pressing button forwards, this testcase tests button function
    ...                                     by checking whether the action of clicking button forwards calls the targeted method function_launch_forwards()
    ...                                     in dronelauncher_python.py.
    [Tags]                                  ManualButton
    Given Encoders Reset
    When Press Button Forwards
    Then Verify Function Is Called          POST /app_launch_forwards HTTP/1.1


Launch input-box pressing arrow up
    [Tags]                                  Arrows
    Encoders Reset
    Input Text                              name:launch_position        6
    Press Keys                              name:launch_position        ARROW_UP    ARROW_UP    ARROW_UP
    Textfield Value Should Be               name:launch_position        9
    Click Go
    Verify Function Is Called               POST /app_launch_position HTTP/1.1


Launch input-box pressing arrow up max
    [Tags]                                  Arrows
    Encoders Reset
    Input Text                              name:launch_position        110
    Press Keys                              name:launch_position        ARROW_UP    ARROW_UP    ARROW_UP    ARROW_UP    ARROW_UP
    Textfield Value Should Be               name:launch_position        111
    Click Go
    Verify Function Is Called               POST /app_launch_position HTTP/1.1


Launch input-box pressing arrow down
    [Tags]                                  Arrows
    Encoders Reset
    Input Text                              name:launch_position        4
    Press Keys                              name:launch_position        ARROW_DOWN    ARROW_DOWN    ARROW_DOWN
    Textfield Value Should Be               name:launch_position        1
    Click Go
    Verify Function Is Called               POST /app_launch_position HTTP/1.1


Launch input-box pressing arrow down max
    [Tags]                                  Arrows
    Encoders Reset
    Input Text                              name:launch_position        2
    Press Keys                              name:launch_position        ARROW_DOWN    ARROW_DOWN    ARROW_DOWN    ARROW_DOWN    ARROW_DOWN
    Textfield Value Should Be               name:launch_position        0
    Click Go
    Verify Function Is Called               POST /app_launch_position HTTP/1.1