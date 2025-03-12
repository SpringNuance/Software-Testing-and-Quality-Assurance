*** Settings ***
Library    SeleniumLibrary
Library    RequestsLibrary
Library    String
Library    Collections

*** Variables ***
${URL}    http://127.0.0.1:5000
${SET_STATE_URL}    ${URL}/set_state
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

Binary Guess Number
    [Documentation]  Perform a binary search to guess the number between min_value and max_value.
    ${guess} =    Evaluate    (${MIN_GUESS} + ${MAX_GUESS}) // 2
    FOR    ${i}    IN RANGE    10
        Input Text    id:guess    ${guess}
        Click Button    xpath=//button[text()='Submit Guess']
        ${text} =    Get Text    xpath=//body
        ${is_higher} =    Run Keyword And Return Status    Should Contain    ${text}    Try a higher number!
        ${is_lower} =    Run Keyword And Return Status    Should Contain    ${text}    Try a lower number!

        Run Keyword If    '${is_higher}' == 'True'    Set Test Variable    ${MIN_GUESS}    ${guess + 1}
        Run Keyword If    '${is_lower}' == 'True'     Set Test Variable    ${MAX_GUESS}    ${guess - 1}
        ${guess} =    Evaluate    (${MIN_GUESS} + ${MAX_GUESS}) // 2
        ${is_correct} =    Evaluate    'Congratulations!' in '''${text}'''
        Run Keyword If    '${is_correct}' == 'True'    Exit For Loop
        Wait Until Page Contains    Guess the Number
    END

Get Session Cookie
    [Arguments]    ${response}
    ${cookie}=    Get From Dictionary    ${response.cookies.get_dict()}    session
    [Return]    ${cookie}

Set Browser Session Cookie
    ${domain}=    Set Variable    127.0.0.1
    ${path}=    Set Variable    /
    Add Cookie    name=session    value=${session_cookie}    domain=${domain}    path=${path}
    Go To    ${URL}
