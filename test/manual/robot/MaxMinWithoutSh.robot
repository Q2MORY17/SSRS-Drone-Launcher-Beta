*** Settings ***
Documentation     Maximizing and Minimizing the Drone Positions
Library             SeleniumLibrary
Library             Process
Library             ./library/UrlLibrary.py
Library              OperatingSystem
Resource            ./../../keywords/keywords.robot
Resource            ./../../keywords/SSRS2_keywords.robot
Resource            ./../../keywords/SabaKeyWords.robot
Test Setup          Begin Web Test
Test Teardown       End Web Test

*** Variables ***
${BROWSER} =        chrome


*** Test Cases ***
Max pitch                   #test case for the Max position
    [Documentation]     Clicking the Positions Max pitch
    [Tags]              max_pitch
    User Click Button Max pitch
Min pitch                         #test case for the Min position
    [Documentation]        Clicking the Positions Min pitch
    [Tags]                  min_pitch
    User Click Button Min pitch

Max lift                      #test case for the  Max lift position
    [Documentation]     Clicking the Positions Max pitch
    [Tags]              max_lift
    User Click Button Max lift
Min lift                      #test case for the Min lift position
    [Documentation]         Clicking the Positions Min pitch
    [Tags]                  min_lift
   User Click Button Min lift