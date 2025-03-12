*** Settings ***
Library    SeleniumLibrary
Resource   helpers.robot

*** Variables ***
${URL}  http://127.0.0.1:5000

*** Test Cases ***
Scoreboard Update With Less Than 10 Scores
    [Documentation]  Write a short description for the test case.
    # Use Scoreboard Modification helper keywords to pre-populate the scoreboard
    # Implement your test steps here.

Scoreboard Update with Exactly 10 Scores
    [Documentation]  Write a short description for the test case.
    # Use Scoreboard Modification helper keywords to set 10 scores
    # Implement your test steps here.

Scoreboard Not Updated with Exactly 10 Scores
    [Documentation]  Write a short description for the test case.
    # Use Scoreboard Modification helper keywords to set 10 scores
    # Implement your test steps here.

*** Keywords ***
# You can implement your keywords here.