from flask import Flask, render_template, request, redirect, url_for, session
from game import NumberGuessingGame

app = Flask(__name__)
app.secret_key = 'supersecretkey'

game = NumberGuessingGame()

def check_session(*args):
    for key in args:
        if key not in session:
            return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        name = request.form.get('name', '').strip() 
        if not name:
            error_message = "Name cannot be empty. Please enter a valid name."
            scores = game.scoreboard.get_scores()
            return render_template('index.html', scores=scores, error_message=error_message)

        session['name'] = name
        game.set_name(name)
        game.reset_game()
        session['bet_points'] = game.bet_points
        session['target_number'] = game.target_number
        session['score_saved'] = False
        return redirect(url_for('choose_difficulty'))
    scores = game.scoreboard.get_scores()
    return render_template('index.html', scores=scores)


@app.route('/difficulty', methods=['GET', 'POST'])
def choose_difficulty():
    if not check_session('name'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        if not difficulty:
            error_message = "Please select a difficulty level."
            return render_template('difficulty.html', name=session.get('name'), bet_points=session.get('bet_points'), error_message=error_message)
        session['difficulty'] = difficulty
        game.set_difficulty(difficulty)
        return redirect(url_for('place_bet'))
    return render_template('difficulty.html', name=session.get('name'), bet_points=session.get('bet_points'))

@app.route('/bet', methods=['GET', 'POST'])
def place_bet():
    if not check_session('name', 'difficulty'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            bet = request.form['bet']
            session['current_bet'] = bet
            game.place_bet(bet)
            game.reset_round()
            session['max_guesses'] = game.max_guesses
            session['target_number'] = game.target_number
            return redirect(url_for('guess'))
        except ValueError as e:
            return render_template('bet.html', name=session.get('name'), bet_points=session.get('bet_points'), error_message=str(e))
    return render_template('bet.html', name=session.get('name'), bet_points=session.get('bet_points'))

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if not check_session('name', 'difficulty', 'current_bet', 'max_guesses', 'target_number'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            guess = request.form['guess']
            result = game.guess_number(guess)
            session['max_guesses'] = game.max_guesses
            if result == "correct":
                session['guessed_correctly'] = True 
                return redirect(url_for('correct_guess'))
            elif result == "out_of_guesses":
                return redirect(url_for('out_of_guesses'))
            hint = result
            return render_template('guess.html', hint=hint, guesses_left=session['max_guesses'], name=session.get('name'), bet_points=session.get('bet_points'), difficulty=session.get('difficulty'), current_bet=session.get('current_bet'))
        except ValueError as e:
            return render_template('guess.html', error_message=str(e), guesses_left=session.get('max_guesses'), name=session.get('name'), bet_points=session.get('bet_points'), difficulty=session.get('difficulty'), current_bet=session.get('current_bet'))
    return render_template('guess.html', guesses_left=session.get('max_guesses'), name=session.get('name'), bet_points=session.get('bet_points'), difficulty=session.get('difficulty'), current_bet=session.get('current_bet'))

@app.route('/correct', methods=['GET', 'POST'])
def correct_guess():
    if not check_session('name', 'difficulty', 'current_bet', 'max_guesses', 'target_number'):
        return redirect(url_for('index'))
    
    if not session.get('guessed_correctly'):
        return redirect(url_for('guess'))
    
    if request.method == 'POST':
        if 'double_prize' not in request.form:
            error_message = "Invalid choice. Please enter 'yes' or 'no'."
            return render_template('correct.html', name=session.get('name'), bet_points=session.get('bet_points'), difficulty=session.get('difficulty'), current_bet=session.get('current_bet'), next_round=False, error_message=error_message)
        
        double_prize = request.form['double_prize']
        won, message = game.double_prize(double_prize)
        session['bet_points'] = game.bet_points
        goal_check = game.check_goal()
        if goal_check == "lose":
            return redirect(url_for('end_game', result="lose"))
        return render_template('correct.html', message=message, name=session.get('name'), bet_points=session.get('bet_points'), difficulty=session.get('difficulty'), current_bet=session.get('current_bet'), next_round=True)
    return render_template('correct.html', name=session.get('name'), bet_points=session.get('bet_points'), difficulty=session.get('difficulty'), current_bet=session.get('current_bet'), next_round=False)

@app.route('/out_of_guesses', methods=['GET', 'POST'])
def out_of_guesses():
    if not check_session('name', 'difficulty', 'current_bet', 'max_guesses', 'target_number'):
        return redirect(url_for('index'))
    if request.method == 'POST':

        if 'save_bet' not in request.form:
            error_message = "Invalid choice. Please enter 'yes' or 'no'."
            return render_template('out_of_guesses.html', name=session.get('name'), bet_points=session.get('bet_points'), difficulty=session.get('difficulty'), next_round=False, error_message=error_message)
        
        save_bet = request.form['save_bet']
        saved, message = game.save_bet(save_bet)
        session['bet_points'] = game.bet_points
        goal_check = game.check_goal()
        if goal_check == "lose":
            return redirect(url_for('end_game', result="lose"))
        return render_template('out_of_guesses.html', message=message, name=session.get('name'), bet_points=session.get('bet_points'), difficulty=session.get('difficulty'), next_round=True)
    return render_template('out_of_guesses.html', name=session.get('name'), bet_points=session.get('bet_points'), difficulty=session.get('difficulty'), next_round=False)

@app.route('/end', methods=['GET', 'POST'])
def end_game():
    if not check_session('name', 'bet_points', 'difficulty'):
        return redirect(url_for('index'))
    if 'name' not in session or 'bet_points' not in session or 'difficulty' not in session:
        return redirect(url_for('index')) 
    if not session.get('score_saved', False) and session.get('bet_points') > 0:
        game.scoreboard.add_score(session.get('name'), session.get('bet_points'), session.get('difficulty'))
        session['score_saved'] = True 
    scores = game.scoreboard.get_scores()
    result = request.args.get("result")
    if result == "lose":
        message = f"Game over. You have {session.get('bet_points')} bet points left."
    else:
        message = f"Congratulations {session.get('name')}! You've completed the game with {session.get('bet_points')} bet points."
    return render_template('end.html', message=message, scores=scores)

@app.route('/new_game')
def new_game():
    game.reset_game()
    session.clear()
    return redirect(url_for('index'))

@app.route('/set_state', methods=['POST'])
def set_state():
    # Get the state data from the request
    state = request.json
    
    def convert_to_int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return value
    
    try:
        # Convert possible integers
        state['max_guesses'] = convert_to_int(state.get('max_guesses'))
        state['bet_points'] = convert_to_int(state.get('bet_points'))
        state['target_number'] = convert_to_int(state.get('target_number'))
        state['current_bet'] = convert_to_int(state.get('current_bet'))

        # Set the game state using the _set_state method
        game._set_state(
            name=state.get('name'),
            difficulty=state.get('difficulty'),
            max_guesses=state.get('max_guesses'),
            bet_points=state.get('bet_points'),
            target_number=state.get('target_number'),
            current_bet=state.get('current_bet')
        )
        
        # Update session variables to reflect the new state
        session['name'] = game.name
        session['difficulty'] = game.difficulty
        session['max_guesses'] = game.max_guesses
        session['bet_points'] = game.bet_points
        session['target_number'] = game.target_number
        session['current_bet'] = game.current_bet
        session['score_saved'] = False  # Reset score saved state
        
        # Log session data for debugging
        app.logger.info(f"Session set: {session}")

        # Return the updated state
        return {
            'name': game.name,
            'difficulty': game.difficulty,
            'max_guesses': game.max_guesses,
            'bet_points': game.bet_points,
            'target_number': game.target_number,
            'current_bet': game.current_bet
        }, 200
    except AttributeError as e:
        # Return an error message if an invalid attribute is provided
        return str(e), 400

@app.route('/get_session_state', methods=['GET'])
def get_session_state():
    if not session:
        return "Session is empty", 400
    # Log session data for debugging
    app.logger.info(f"Session retrieved: {session}")
    return {key: session[key] for key in session}, 200

def create_app():
    return app
