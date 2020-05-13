*** Settings ***
Documentation
Library                                     SeleniumLibrary
Library                                     Process
Library                                     ./library/UrlLibrary.py
Library         			    OperatingSystem	
Suite Setup                                 Begin Web Test
Suite Teardown                              End Web Test

*** Variables ***
${BROWSER} =                                headlesschrome

*** Keywords ***
#If you want to run the program local and python3 command is not found
#1. Make sure the Python 3 folder is present in the PATH environment variable.
#2. Locate the "python.exe" file in the Python 3 folder.
#3. Copy and Paste the "python.exe" file within the Python 3 folder.
#4. Rename the copied file to "python3" (or whatever you want the command to be).
Begin Web Test
    ${URL}=                                 Get Url
#    Start Process                           python3    ./python/dronelauncher_python.py    shell=True
    Open Browser                            about:blank     ${BROWSER}
    Maximize Browser Window
    Go To                                   ${URL}

End Web Test
    Close Browser
#    Terminate All Processes

################################################################################
#									       #
#                      Team 1's edited keywords                                #
#									       #
################################################################################
Check Log
    [Arguments]	 ${target_string}  ${error_code}
    ${logfile}  Get File  .dronelauncher.log
    Should match  ${logfile}  *${target_string}*\"*${error_code}*
User Expects Position To Change
    ${target_string} =	Set Variable  POST /app_launch_position HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
User Expects Error
    ${target_string} =	Set Variable  POST /app_launch_position HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  400
User Expects Position Forwards
    ${target_string} =	Set Variable  POST /app_launch_forwards HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500
Then User Expects Position Backwards
    ${target_string} =	Set Variable  POST /app_launch_backwards HTTP/1.1
    Wait Until Keyword Succeeds  6x  200ms  Check Log  ${target_string}  500

################################################################################
#									       #
#                     END of Team 1's edited keywords                          #
#									       #
################################################################################








Gui Is Visible
    Wait Until Page Contains Element        id=video

Gui Has Loaded
    Page Should Contain Element             id=script_battery_voltage

Encoders Reset
    Click Button                            id:script_reset_encoders

Press Button Backwards
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes	
    Click Button                            id:script_launch_backwards
#    Sleep                                   1

Press Button Forwards
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
    Click Button                            id:script_launch_forwards
 #   Sleep                                   1

Verify Function Is Called
    [Arguments]                             ${function}
    ${result}                               Terminate Process
    Process Should Be Stopped
    Should Contain                          ${result.stderr}  ${function}


Launch Input
    [Arguments]                             ${number}
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes
    Input Text                              name:launch_position  ${number}

Click Go
    Start Process  echo Resetting log... > .dronelauncher.log  shell=yes	
    Click Button                            id:script_launch_position
#    Sleep                                   1

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
#    Verify Function Is Called               POST /app_launch_position HTTP/1.1
    User Expects Error
	
#Input valid value should be between 0-111
Launch input-box w/ invalid positive input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            112
    Click Go
    Alert Should Be Present                 text=Value should be between 0 and 111
#    Verify Function Is Called               POST /app_launch_position HTTP/1.1
    User Expects Error

#Input valid value should be between 0-111
Launch input-box w/ min valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            0
    Click Go
#    Verify Function Is Called               POST /app_launch_position HTTP/1.1
    User Expects Position To Change

#Input valid value should be between 0-111
Launch input-box w/ min+1 valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            1
    Click Go
#    Verify Function Is Called               POST /app_launch_position HTTP/1.1
    User Expects Position To Change

#Input valid value should be between 0-111
Launch input-box w/ max-1 valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            110
    Click Go
#    Verify Function Is Called               POST /app_launch_position HTTP/1.1
    User Expects Position To Change

#Input valid value should be between 0-111
Launch input-box w/ max valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            111
    Click Go
#    Verify Function Is Called               POST /app_launch_position HTTP/1.1
    User Expects Position To Change

Functionable Button Backwards
    [Documentation]                         Since there is no intended visible response after pressing button backwards, this testcase tests button function
    ...                                     by checking whether the action of clicking button backwards calls the targeted method function_launch_backwards()
    ...                                     in dronelauncher_python.py.
    [Tags]                                  ManualButton
    Given Encoders Reset
    When Press Button Backwards
#    Then Verify Function Is Called          POST /app_launch_backwards HTTP/1.1
    Then User Expects Position Backwards

Functionable Button Forwards
    [Documentation]                         Since there is no intended visible response after pressing button forwards, this testcase tests button function
    ...                                     by checking whether the action of clicking button forwards calls the targeted method function_launch_forwards()
    ...                                     in dronelauncher_python.py.
    [Tags]                                  ManualButton
    Given Encoders Reset
    When Press Button Forwards
#    Then Verify Function Is Called          POST /app_launch_forwards HTTP/1.1
    User Expects Position Forwards