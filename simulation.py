#simulation.py
from dice_decision import chooseDice
from dice_utils import rollDice

def playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    """
    Simulates a single game of dice, updating WinCount and LoseCount matrices based on the outcome.

    Parameters:
    - NDice (int): Maximum number of dice that can be rolled in one turn.
    - NSides (int): Number of sides on each dice.
    - LTarget, UTarget (int): Lower and upper targets for the game score.
    - LoseCount, WinCount (list): Matrices for tracking loses and wins.
    - M (float): Hyperparameter for exploration/exploitation balance.

    Returns:
    - tuple: Updated LoseCount and WinCount matrices.
    """
    # Initialize scores
    scores = [0, 0]  # [Player1, Player2]
    currentPlayer = 0  # Start with Player 1

    # Game loop
    while True:
        opponent = (currentPlayer + 1) % 2
        X, Y = scores[currentPlayer], scores[opponent]

        # Determine the number of dice to roll
        nDice = chooseDice(X, Y, WinCount, LoseCount, NDice, M)
        
        # Roll dice and update current player's score
        rollResult = rollDice(nDice, NSides)
        scores[currentPlayer] += rollResult

        # Check for win or loss
        if LTarget <= scores[currentPlayer] <= UTarget:
            # Current player wins
            WinCount[X][Y][nDice] += 1
            break
        elif scores[currentPlayer] > UTarget:
            # Current player loses
            LoseCount[X][Y][nDice] += 1
            break

        # Switch players
        currentPlayer = opponent

    return LoseCount, WinCount
