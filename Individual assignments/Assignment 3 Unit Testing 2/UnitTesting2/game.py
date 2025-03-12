import random
from scoreboard import Scoreboard

class NumberGuessingGame:
    def __init__(self):
        self.name = ""
        self.difficulty = ""
        self.max_guesses = 0
        self.bet_points = 100
        self.target_number = 0
        self.current_bet = 0
        self.scoreboard = Scoreboard()

    def reset_game(self):
        self.name = ""
        self.difficulty = ""
        self.max_guesses = 0
        self.bet_points = 100
        self.target_number = random.randint(1, 100)
        self.current_bet = 0

    def set_name(self, name):
        if not name.strip():
            raise ValueError("Name cannot be empty. Please enter a valid name.")
        self.name = name.strip()
        
    def set_difficulty(self, difficulty):
        if difficulty not in ['easy', 'hard']:
            raise ValueError("Difficulty must be 'easy' or 'hard'")
        self.difficulty = difficulty
        self.max_guesses = 10 if difficulty == 'easy' else 5

    def place_bet(self, bet):
        if isinstance(bet, int) or (isinstance(bet, str) and bet.isdigit()):
            bet = int(bet)
            if 1 <= bet <= self.bet_points:
                self.current_bet = bet
                return
        raise ValueError(f"Invalid bet amount. Enter a value between 1 and {self.bet_points}.")
        

    def reset_round(self):
        self.max_guesses = 10 if self.difficulty == 'easy' else 5
        self.target_number = random.randint(1, 100)

    def guess_number(self, guess):
        if isinstance(guess, int) or (isinstance(guess, str) and guess.isdigit()):
            guess = int(guess)
            if 1 <= guess <= 100:
                self.max_guesses -= 1
                if guess == self.target_number:
                    return "correct"
                elif self.max_guesses == 0:
                    return "out_of_guesses"
                else:
                    if guess < self.target_number:
                        return "higher"
                    else:
                        return "lower"
        raise ValueError("Invalid guess. Please guess a number between 1 and 100.")

    def double_prize(self, choice):
        if choice not in ['yes', 'no']:
            raise ValueError("Invalid choice. Please enter 'yes' or 'no'.")
    
        if choice == 'yes':
            if random.choice([True, False]):
                self.bet_points += self.current_bet * 2
                return True, f"You won! Your bet points are now {self.bet_points}."
            else:
                return False, f"You lost the double or nothing. Your bet points remain {self.bet_points}."
        else:
            self.bet_points += self.current_bet
            return None, f"You chose not to double. Your bet points are now {self.bet_points}."

    def save_bet(self, choice):
        if choice not in ['yes', 'no']:
            raise ValueError("Invalid choice. Please enter 'yes' or 'no'.")
    
        if choice == 'yes':
            if random.choice([True, False]):
                return True, f"You saved your bet points. Your bet points are still {self.bet_points}."
            else:
                self.bet_points -= 2 * self.current_bet
                return False, f"You lost the bet save chance. Your bet points are now {self.bet_points}."
        else:
            self.bet_points -= self.current_bet
            return None, f"You chose not to save. Your bet points are now {self.bet_points}."

    def check_goal(self):
        if self.bet_points <= 0:
            return "lose"
        else:
            return None

    # def _set_state(self, name, difficulty, max_guesses, bet_points, target_number, current_bet):
    #     """
    #     Helper function for testing purposes to set the internal state of the game.
    #     All parameters are required.
    #     """
    #     self.set_name(name)
    #     self.set_difficulty(difficulty)
    #     self.max_guesses = max_guesses
    #     self.bet_points = bet_points
    #     self.target_number = target_number
    #     self.current_bet = current_bet

    def _set_state(self, name=None, difficulty=None, max_guesses=None, bet_points=None, target_number=None, current_bet=None):
        if name is not None:
            self.set_name(name) 
        if difficulty is not None:
            self.set_difficulty(difficulty) 
        if max_guesses is not None:
            self.max_guesses = max_guesses
        if bet_points is not None:
            self.bet_points = bet_points
        if target_number is not None:
            self.target_number = target_number
        if current_bet is not None:
            self.current_bet = current_bet

    # def _set_state(self, **kwargs):
    #     """
    #     Helper function for testing purposes to set the internal state of the game.
    #     Accepts named arguments for each state variable.
    #     """
    #     # Iterate over all the keyword arguments
    #     for key, value in kwargs.items():
    #         # Check if the attribute exists in the instance
    #         if hasattr(self, key):
    #             # Set the attribute to the provided value
    #             setattr(self, key, value)
    #         else:
    #             # Raise an error if the attribute does not exist
    #             raise AttributeError(f"{key} is not a valid attribute of {self.__class__.__name__}")
            
    def play_cli(self):
        while True:
            try :
                name = input("Enter your name: ").strip()
                self.set_name(name)
                break
            except ValueError as e:
                print(e)    
        
        while True:
            try:
                difficulty = input("Choose difficulty (easy/hard): ").lower()
                self.set_difficulty(difficulty)
                break
            except ValueError as e:
                print(e)
        
        while True:
            print(f"\nCurrent bet points: {self.bet_points}")
            while True:
                try:
                    bet = input(f"Place your bet (1 to {self.bet_points}): ")
                    self.place_bet(bet)
                    break
                except ValueError as e:
                    print(e)
            
            self.reset_round()
            
            while self.max_guesses > 0:
                try:
                    guess = input(f"Make a guess (1-100): ")
                    result = self.guess_number(guess)
                    if result == "correct":
                        print("Congratulations! You've guessed the correct number.")
                        break
                    elif result == "out_of_guesses":
                        print("You've run out of guesses.")
                        break
                    else:
                        print(f"The number is {result}.")
                except ValueError as e:
                    print(e)
            
            if result == "correct":
                while True:
                    try:
                        double = input("Do you want to double your prize? (yes/no): ").lower()
                        won, message = self.double_prize(double)
                        print(message)
                        break
                    except ValueError as e:
                        print(e)
            else:
                while True:
                    try:
                        save = input("Do you want to try to save your bet? (yes/no): ").lower()
                        saved, message = self.save_bet(save)
                        print(message)
                        break
                    except ValueError as e:
                        print(e)
            
            goal_check = self.check_goal()
            if goal_check == "lose":
                print(f"Game over. You have {self.bet_points} bet points left.")
                break
            
            while True:
                try:
                    continue_game = input("Do you want to continue playing? (yes/no): ").lower()
                    if continue_game not in ['yes', 'no']:
                        raise ValueError("Invalid choice. Please enter 'yes' or 'no'.")
                    break
                except ValueError as e:
                    print(e)
            
            if continue_game == "no":
                break
        
        self.scoreboard.add_score(self.name, self.bet_points, self.difficulty)
        self.scoreboard.display_scores()

if __name__ == "__main__":
    game = NumberGuessingGame()
    game.play_cli()
