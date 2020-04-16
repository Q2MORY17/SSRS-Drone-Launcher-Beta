*** Settings ***
Documentation  Basic info
Library  SeleniumLibrary
Test Setup  Begin web test
Test Teardown  End web test

*** Variables ***
${BROWSER}  =  Chrome
${URL}  =  http://192.168.1.236:5000/
${IP}  =  return ip
${PORT}  =  5000

*** Test Cases ***

[Documentation]
[Tags]      Test 1