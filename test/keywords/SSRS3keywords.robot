*** Keywords ***
Begin Web Test
    ${URL}=                     Get Url
    Start Process               python3    ./python/dronelauncher_python.py    shell=True
    Open Browser                about:blank     ${BROWSER}
    Maximize Browser Window
    Sleep                       3s
    Go To                       ${URL}
    Sleep                       3s
#    Server Is Up
    Click Element               xpath:/html/body/ul/li[4]/a

End Web Test
    Close Browser

Server Is Up
    Wait Until Page Contains Element  xpath://button[@id="script_pitch_up"]
    Page Should Contain  Pitch
    Click Button  xpath://button[@id="script_reset_encoders"]