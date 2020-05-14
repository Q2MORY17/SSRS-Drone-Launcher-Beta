*** Settings ***
Documentation           Dronelauncher tests regarding options for the automatic use
Library                 SeleniumLibrary
Library                 Process
Library                 OperatingSystem
Library                 ./Library/UrlLibrary.py
Resource                ./../../keywords/keywords.robot
Resource                ./../../keywords/OptionButtons_Keywords.robot
Test Setup              Begin web test
Test Teardown           End web test

*** Variables ***
${BROWSER}  firefox
${APP_HOME}  app_home HTTP
# ${URL} =  http://192.168.2.52:5000/
# ${IP} =  return ip
# ${PORT} =  5000
# ${logfile}  	Get File  .dronelauncher.log

*** Keywords ***
#Begin Web Test
#   ${URL}=                     Get Url
#  Start process               python3 ./python/dronelauncher_python.py 2>log.txt         shell=True
#   Open Browser                about:blank     ${BROWSER}
#   Maximize Browser Window
#   Sleep                       3s
#   Go To                       ${URL}
#   Sleep                       3s

*** Test Cases ***
Home Button
    Given Server Is Up
    When User Clicks Home Button
    ${log}=                                 Get File    log.txt
    log to console  ${log}
    Should contain                          ${log}      POST /${APP_HOME}/1.1


#Home Button
#	[Documentation]		Clicking the Home button
#	[Tags]			Home_Button

#   Given Server Is Up
#	When User Clicks Home Button
#	Then User Expects The Right Function Call