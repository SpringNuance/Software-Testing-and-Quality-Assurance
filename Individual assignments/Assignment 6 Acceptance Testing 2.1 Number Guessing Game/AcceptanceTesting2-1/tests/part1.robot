*** Settings ***
Library    SeleniumLibrary
Resource   helpers.robot

*** Variables ***
${URL}  http://127.0.0.1:5000

*** Test Cases ***
Normal Game Playthrough
    [Documentation]  Write a short description for the test case.
    # Implement your test steps here

Repetitive Incorrect Guesses Leading to Loss
    [Documentation]   Write a short description for the test case.
    # Implement your test steps here

*** Keywords ***
# You can implement your keywords here.