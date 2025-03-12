*** Settings ***
Library    SeleniumLibrary
Library    RequestsLibrary
Library    String
Library    Collections
Library    OperatingSystem

*** Variables ***
${URL}  http://127.0.0.1:5000
${SET_STATE_URL}  ${URL}/set_state
${MIN_GUESS}    1
${MAX_GUESS}    100

*** Keywords ***
Set Session Parameters
    [Arguments]    ${name}    ${difficulty}    ${max_guesses}    ${bet_points}    ${target_number}    ${current_bet}
    [Documentation]  Set session parameters to jump to a specific game state.
    ${payload}=    Create Dictionary    name=${name}    difficulty=${difficulty}    max_guesses=${max_guesses}    bet_points=${bet_points}    target_number=${target_number}    current_bet=${current_bet}
    Create Session    session    ${URL}
    ${response}=    POST On Session    session    /set_state    json=${payload}
    Should Be Equal As Numbers    ${response.status_code}    200
    ${cookie}=    Get Session Cookie    ${response}
    Set Test Variable    ${session_cookie}    ${cookie}
    Set Browser Session Cookie

Backup Original Scoreboard File
    [Arguments]    ${score_file}    ${backup_file}
    [Documentation]  Back up the original scoreboard file before modifying it.
    Copy File    ${score_file}    ${backup_file}

Overwrite Scoreboard File With Custom Data
    [Arguments]    ${score_file}    ${custom_content}
    [Documentation]  Overwrite the scoreboard with custom data for testing.
    Create File    ${score_file}    ${custom_content}

Restore Original Scoreboard File
    [Arguments]    ${backup_file}    ${score_file}
    [Documentation]  Restore the original scoreboard file after testing.
    Copy File    ${backup_file}    ${score_file}
    Remove File    ${backup_file}

Get Session Cookie
    [Arguments]    ${response}
    ${cookie}=    Get From Dictionary    ${response.cookies.get_dict()}    session
    [Return]    ${cookie}

Set Browser Session Cookie
    ${domain}=    Set Variable    127.0.0.1
    ${path}=    Set Variable    /
    Add Cookie    name=session    value=${session_cookie}    domain=${domain}    path=${path}
    Go To    ${URL}
