*** Keywords ***
Verify Function Is Called
    [Arguments]                             ${function}
    ${result}                               Terminate Process
    Process Should Be Stopped
    Should Contain                          ${result.stderr}  ${function}

Begin Web Test
    [Documentation]                         You need to import UrlLibrary.py inside the robot file that you working from
    ${URL}=                                 Get Url
    Start Process                           python3    ./python/dronelauncher_python.py    shell=True
    Open Browser                            about:blank     ${BROWSER}
    Maximize Browser Window
    Go To                                   ${URL}
