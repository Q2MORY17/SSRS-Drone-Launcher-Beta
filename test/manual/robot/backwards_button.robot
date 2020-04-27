*** Settings ***
Documentation     A test case of button backwards in the Launch part of SSRS Launcher Website
Library     SeleniumLibrary
Library                 Process
Library       ./library/ip.py
Test Teardown       Close All The Browsers

*** Variables ***
${browser}    chrome

*** Test Cases ***
Functionable Button Backwards
    [Documentation]       Since there is no intended visible response after pressing button backwards, this testcase tests button function
    ...                   by checking whether the action of clicking button backwards calls the targeted method function_launch_backwards()
    ...                   in dronelauncher_python.py.
    [tags]      ButtonBackwards
    Given Website Is Open    ${browser}
    When Press Button Backwards
    Then Verify Clicking Button Backwards Calls Relevant Function In Python File


*** Keywords ***
Generate Ip
    ${result}       return ip
    [return]        ${result}

Website Is Open
    [Arguments]     ${browser}
    ${ssrs launcher url}=        Generate Ip
    Start Process       python   ./python/dronelauncher_python.py   shell=True
    Open Browser    ${ssrs launcher url}     ${browser}
    Maximize Browser Window

Press Button Backwards
    Click Button    id:script_launch_backwards
    Sleep  100

Verify Clicking Button Backwards Calls Relevant Function In Python File
    ${result}       Terminate Process
    Process Should Be Stopped
    Log To Console        ${result.stderr}
    Should Contain         ${result.stderr}     in function_launch_backwards

Close All The Browsers
    Close All Browsers