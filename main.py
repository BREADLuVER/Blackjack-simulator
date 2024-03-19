#main.py
from simulation import playGame
from analysis import extractAnswer

def prog3(NDice, NSides, LTarget, UTarget, NGames, M):
    """
    Main function to run the game simulation and extract learned strategies.

    Parameters:
    - NDice (int): Maximum number of dice that can be rolled in one turn.
    - NSides (int): Number of sides on each dice.
    - LTarget (int): Lower target score for winning.
    - UTarget (int): Upper target score for winning.
    - NGames (int): Number of games to simulate.
    - M (float): Exploration/exploitation balance hyperparameter.
    """
    # Initialize matrices
    WinCount = [[[0 for _ in range(NDice + 1)] for _ in range(UTarget + 1)] for _ in range(UTarget + 1)]
    LoseCount = [[[0 for _ in range(NDice + 1)] for _ in range(UTarget + 1)] for _ in range(UTarget + 1)]
    
    # Simulate NGames
    for _ in range(NGames):
        playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)
    
    # Extract and return the learned strategy and probabilities
    BestMove, WinProbability = extractAnswer(WinCount, LoseCount, NDice)
    return BestMove, WinProbability
