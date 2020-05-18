*** Keywords ***
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

Launch Input & Press Go
    [Arguments]                             ${number}
    Input Text                              name:launch_position  ${number}
    Click Go

Click Go
    Click Button                            id:script_launch_position
    Sleep                                   1

Arrow Key Input & Press Go
    [Arguments]                             ${initial_input}    ${arrow_key}    ${final_value}
    Input Text                              name:launch_position        ${initial_input}
    Press Keys                              name:launch_position        ${arrow_key}
    Textfield Value Should Be               name:launch_position        ${final_value}
    Click Go