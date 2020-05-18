*** Settings ***
Documentation       Dronelauncher tests regarding settings for the automatic use
Resource            ./../../keywords/SSRS3keywords.robot
Resource            ./../../keywords/keywords.robot
Library             SeleniumLibrary
Library             Process
Library             ./Library/UrlLibrary.py
Test Setup  Begin web test
Test Teardown  End web test

*** Variables ***
${BROWSER}                          headlesschrome

*** Test Cases ***
Change Pitch Test1
    [Documentation]                 Test the "change pitch" function with negative outcome
    [Tags]                          CPtest1
    Go to Settings
    Change Pitch Text Input         -1
    Click Change Pitch
    Change Pitch Alert

Change Pitch Test2
    [Documentation]                 Test the "change pitch" function with negative outcome
    [Tags]                          CPtest2
    Go to Settings
    Change Pitch Text Input         91
    Click Change Pitch
    Change Pitch Alert

Change Pitch Test3
    [Documentation]                 Test the "change pitch" function with no negative outcome
    [Tags]                          CPtest3
    Go to Settings
    Change Pitch Text Input         45
    Click Change Pitch
    Alert Should Not be Present

Change Lift Test1
    [Documentation]                 Test the "change lift" function with negative outcome
    [Tags]                          CLtest1
    Go to Settings
    Change Lift Text Input          131
    Click Change Lift
    Change Lift Alert

Change Lift Test2
    [Documentation]                 Test the "change lift" function with negative outcome
    [Tags]                          CLtest2
    Go to Settings
    Change Lift Text Input          -1
    Click Change Lift
    Change Lift Alert

Change Lift Test3
    [Documentation]                 Test the "change lift" function with no negative outcome
    [Tags]                          CLtest3
    Go to Settings
    Change Lift Text Input          65
    Click Change Lift
    Alert Should Not be Present

Change Rotation Test1
    [Documentation]                 Test the "change rotation" function with negative outcome
    [Tags]                          CRtest1
    Go to Settings
    Change Rotation Text Input      181
    Click Change Rotation
    Change Rotation Alert

Change Rotation Test2
    [Documentation]                 Test the "change rotation" function with negative outcome
    [Tags]                          CRtest2
    Go to Settings
    Change Rotation Text Input      -181
    Click Change Rotation
    Change Rotation Alert

Change Rotation Test3
    [Documentation]                 Test the "change rotation" function with no negative outcome
    [Tags]                          CRtest3
    Go to Settings
    Change Rotation Text Input      80
    Click Change Rotation
    Alert Should Not be Present

Change Speed Test1
    [Documentation]                 Test the "change speed" function with negative outcome
    [Tags]                          CStest1
    Go to Settings
    Change Speed Text Input         -1
    Click Change Speed
    Change Speed Alert

Change Speed Test2
    [Documentation]                 Test the "change speed" function with negative outcome
    [Tags]                          CStest2
    Go to Settings
    Change Speed Text Input         11
    Click Change Speed
    Change Speed Alert

Change Speed Test3
    [Documentation]                 Test the "change speed" function with no negative outcome
    [Tags]                          CStest3
    Go to Settings
    Change Speed Text Input         5
    Click Change Speed
    Alert Should Not be Present

Change Acceleration Test1
    [Documentation]                 Test the "change acceleration" function with negative outcome
    [Tags]                          CAtest1
    Go to Settings
    Change Acceleration Text Input  -1
    Click Change Acceleration
    Change Acceleration Alert

Change Acceleration Test2
    [Documentation]                 Test the "change acceleration" function with negative outcome
    [Tags]                          CAtest2
    Go to Settings
    Change Acceleration Text Input  49
    Click Change Acceleration
    Change Acceleration Alert

Change Acceleration Test3
    [Documentation]                 Test the "change acceleration" function with no negative outcome
    [Tags]                          CAtest3
    Go to Settings
    Change Acceleration Text Input  24
    Click Change Acceleration
    Alert Should Not be Present
