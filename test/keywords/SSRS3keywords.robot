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

Check Log
        ${log}=                     Get File    log.txt
        log to console              ${log}
        [Return]                    ${log}