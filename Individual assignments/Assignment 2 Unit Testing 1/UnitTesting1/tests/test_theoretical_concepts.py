import unittest
from unittest.mock import patch
from game import NumberGuessingGame

class TestTheoreticalConcepts(unittest.TestCase):

    def setUp(self):
        self.game = NumberGuessingGame()

    # Equivalence Partitioning Tests
    def test_valid_guesses(self):
        # TODO: Set the target number and check guesses within the valid range.
        pass

    def test_invalid_guesses(self):
        # TODO: Check guesses outside the valid range and non-numeric inputs.
        pass

    # Boundary Value Analysis Tests
    def test_boundary_values(self):
        # TODO: Set bet points and check bets at boundary values and invalid values in the beginning of the game.
        pass
    
    def test_boundary_values_after_rounds(self):
        # TODO: Set bet points, target number, and current bet, and check bets at boundary values and invalid values after rounds when the player has 320 points.
        pass

    # Robustness Testing
    def test_robustness_difficulty(self):
        # TODO: Check setting difficulty with valid and invalid inputs.
        pass

    # Decision Table Testing
    @patch('game.random.choice', return_value=True)
    def test_decision_table_double_success(self, mock_choice):
        # TODO: Set the current bet and bet points, then test double_prize method with success.
        pass

    @patch('game.random.choice', return_value=False)
    def test_decision_table_double_failure(self, mock_choice):
        # TODO: Set the current bet and bet points, then test double_prize method with failure.
        pass

    def test_decision_table_no_double(self):
        # TODO: Set the current bet and bet points, then test double_prize method when the 'no' option is selected.
        pass
        
    @patch('game.random.choice', return_value=True)
    def test_decision_table_save_success(self, mock_choice):
        # TODO: Set the current bet and bet points, then test save_bet method with success.
        pass

    @patch('game.random.choice', return_value=False)
    def test_decision_table_save_failure(self, mock_choice):
        # TODO: Set the current bet and bet points, then test save_bet method with failure.
        pass

    def test_decision_table_no_save(self):
        # TODO: Set the current bet and bet points, then test save_bet method when the 'no' option is selected.
        pass

if __name__ == "__main__":
    unittest.main()
