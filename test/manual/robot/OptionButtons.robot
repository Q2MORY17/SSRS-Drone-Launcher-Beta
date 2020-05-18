*** Settings ***
Documentation           Dronelauncher tests regarding options for the automatic use
Library                 SeleniumLibrary
Library                 Process
Library                 OperatingSystem
Library                 ./library/UrlLibrary.py
Resource                ./../../keywords/keywords.robot
Resource                ./../../keywords/SSRS3keywords.robot
Test Setup              Begin web test
Test Teardown           End web test

*** Variables ***
${BROWSER}          headlesschrome
${HOME}             app_home HTTP
${RESET_ENCODERS}   app_reset_encoders HTTP

*** Test Cases ***
Home Button
    Given Server Is Up
    When User Clicks Home Button
    Then Verify Function Is Called        POST /${HOME}/1.1


Reset Enconders Button
    Given Server Is Up
    When User Clicks Reset Encoders Button
    Then Verify Function Is Called        POST /${RESET_ENCODERS}/1.1

