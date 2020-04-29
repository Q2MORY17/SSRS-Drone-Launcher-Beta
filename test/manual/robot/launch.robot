*** Settings ***
Documentation
Library                                     SeleniumLibrary
Library                                     Process
Library                                     ./library/UrlLibrary.py
Suite Setup                                 Begin Web Test
Suite Teardown                              End Web Test

*** Variables ***
${BROWSER} =                                chrome

*** Keywords ***
#If you want to run the program local and python3 command is not found
#1. Make sure the Python 3 folder is present in the PATH environment variable.
#2. Locate the "python.exe" file in the Python 3 folder.
#3. Copy and Paste the "python.exe" file within the Python 3 folder.
#4. Rename the copied file to "python3" (or whatever you want the command to be).
Begin Web Test
    ${URL}=                                 Get Url
    Start Process                           python3    ./python/dronelauncher_python.py    shell=True
    Open Browser                            about:blank     ${BROWSER}
    Maximize Browser Window
    Go To                                   ${URL}

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
    Sleep                                   150

Verify Button Backwards Clicked
    ${result}                               Terminate Process
    Process Should Be Stopped
    Log To Console                          ${result.stderr}
    Should Contain                          ${result.stderr}  POST /app_launch_backwards HTTP/1.1

Launch Input
    [Arguments]                             ${number}
    Input Text                              name:launch_position  ${number}

Click Go
    Click Button                            id:script_launch_position

*** Test Cases ***
Battery Voltage Button Should Be Visible
    Gui Is Visible
    Gui Has Loaded


Functionable Button Backwards
    [Documentation]                         Since there is no intended visible response after pressing button backwards, this testcase tests button function
    ...                                     by checking whether the action of clicking button backwards calls the targeted method function_launch_backwards()
    ...                                     in dronelauncher_python.py.
    [Tags]                                  ButtonBackwards
    Given Encoders Reset
    When Press Button Backwards
    Then Verify Button Backwards Clicked


#Input valid value should be between 0-111
Launch input-box w/ invalid negative input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            -1
    Click Go
    Alert Should Be Present                 text=Value should be between 0 and 111

#Input valid value should be between 0-111
Launch input-box w/ min valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            0
    Click Go


#Input valid value should be between 0-111
Launch input-box w/ min+1 valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            1
    Click Go

#Input valid value should be between 0-111
Launch input-box w/ max-1 valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            110
    Click Go


#Input valid value should be between 0-111
Launch input-box w/ max valid input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            111
    Click Go

#Input valid value should be between 0-111
Launch input-box w/ invalid positive input
    [Tags]                                  INPUT
    Encoders Reset
    Launch Input                            112
    Click Go
    Alert Should Be Present                 text=Value should be between 0 and 111
