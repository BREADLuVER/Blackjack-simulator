import unittest
from unittest.mock import patch
from simulation import playGame

class TestPlayGame(unittest.TestCase):
    def setUp(self):
        # Setup basic parameters for testing
        self.NDice = 2
        self.NSides = 6
        self.LTarget = 15
        self.UTarget = 17
        self.M = 100
        # Initialize WinCount and LoseCount matrices
        self.WinCount = [[[0 for _ in range(self.NDice + 1)] for _ in range(self.UTarget + 1)] for _ in range(self.UTarget + 1)]
        self.LoseCount = [[[0 for _ in range(self.NDice + 1)] for _ in range(self.UTarget + 1)] for _ in range(self.UTarget + 1)]
    
    @patch('dice_utils.rollDice')
    @patch('dice_decision.chooseDice')
    def test_win_condition_met(self, mock_chooseDice, mock_rollDice):
        """
        Test if WinCount is updated correctly when the win condition is met.
        """
        # Mocking chooseDice to always choose 1 dice and rollDice to return a specific score leading to a win
        mock_chooseDice.return_value = 1
        mock_rollDice.return_value = 2  # Choose values that would lead to a win based on LTarget and UTarget

        # Simulate a single game
        LoseCount, WinCount = playGame(self.NDice, self.NSides, self.LTarget, self.UTarget, self.LoseCount, self.WinCount, self.M)
        
        # Assert WinCount is updated correctly
        self.assertTrue(any(WinCount[X][Y][1] > 0 for X in range(len(WinCount)) for Y in range(len(WinCount[0]))),
                        "WinCount was not updated correctly.")

    # Additional tests can be defined following a similar pattern, such as testing lose conditions, and other edge cases

if __name__ == '__main__':
    unittest.main()
