*** Settings ***
Documentation     A test case of button backwards in the Launch part of SSRS Launcher Website
Library     SeleniumLibrary
Library                 Process
Test Teardown       Close All The Browsers

*** Variables ***
${ssrs launcher url}    http://172.17.47.17:5000/
${browser}    chrome

*** Test Cases ***
Functionable Button Backwards
    [Documentation]       Since there is no intended visible response after pressing button backwards, this testcase tests button function
    ...                   by checking whether the action of clicking button backwards calls the targeted method function_launch_backwards()
    ...                   in dronelauncher_python.py.
    [tags]      ButtonBackwards
    Given Website Is Open   ${ssrs launcher url}    ${browser}
    When Press Button Backwards
    Then Verify Clicking Button Backwards Calls Relevant Function In Python File

Functionable Button Backwards
    [Documentation]       Since there is no intended visible response after pressing button backwards, this testcase tests button function
    ...                   by checking whether the action of clicking button backwards calls the targeted method function_launch_backwards()
    ...                   in dronelauncher_python.py.
    [tags]      ButtonBackwards
    Given Website Is Open   ${ssrs launcher url}    ${browser}
    When Press Button Backwards
    Then Verify Clicking Button Backwards Calls Relevant Function In Python File

*** Keywords ***
Website Is Open
    [Arguments]     ${ssrs launcher url}     ${browser}
    Start Process       python   ./python/dronelauncher_python.py   shell=True
    Open Browser    ${ssrs launcher url}     ${browser}
    Maximize Browser Window

Press Button Backwards
    Click Button    id:script_launch_backwards
    Sleep  30

Verify Clicking Button Backwards Calls Relevant Function In Python File
    ${result}       Terminate Process
    Process Should Be Stopped
    Log To Console        ${result.stderr}
    Should Contain         ${result.stderr}     in function_launch_backwards

Close All The Browsers
    Close All Browsers