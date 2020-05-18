*** Keywords ***
Go to Settings
    Click Element               xpath:/html/body/ul/li[4]/a

Server Is Up
    Wait Until Page Contains Element  xpath://button[@id="script_pitch_up"]
    Page Should Contain  Pitch
    Click Button  xpath://button[@id="script_reset_encoders"]

End Web Test
    Close Browser
    Terminate All Processes

User Clicks Home Button
	Click Button	//*[@id="script_home"]
    Sleep           1

User Clicks Reset Encoders Button
    Click Button    //*[@id="script_reset_encoders"]
    Sleep           3

Change Pitch Text Input
        [Arguments]                 ${input}
        Input Text                  xpath://*[@id="settings_launch"]/div[1]/input  ${input}

Click Change Pitch
        Click Button                xpath://*[@id="script_change_pitch"]

Change Pitch Alert
        Alert Should be Present         Value should be between 0 and 90

Change Lift Text Input
        [Arguments]                 ${input}
        Input Text                  xpath://*[@id="settings_launch"]/div[2]/input  ${input}

Click Change Lift
        Click Button                xpath://*[@id="script_change_lift"]

Change Lift Alert
        Alert Should be Present         Value should be between 0 and 130

Change Rotation Text Input
        [Arguments]                 ${input}
        Input Text                 xpath://html/body/div/div[1]/div[8]/div[3]/input  ${input}

Click Change Rotation
        Click Button                xpath://*[@id="script_change_rotation"]

Change Rotation Alert
        Alert Should be Present         Value should be between -180 and 180

Change Speed Text Input
        [Arguments]                 ${input}
        Input Text                  xpath://html/body/div/div[1]/div[8]/div[4]/input  ${input}

Click Change Speed
        Click Button                xpath://*[@id="script_change_speed"]

Change Speed Alert
        Alert Should be Present         Value should be between 1 and 10

Change Acceleration Text Input
        [Arguments]                 ${input}
        Input Text                  xpath://*[@id="settings_launch"]/div[5]/input  ${input}

Click Change Acceleration
        Click Button                xpath://*[@id="script_change_acceleration"]

Change Acceleration Alert
        Alert Should be Present         Value should be between 1 and 48
