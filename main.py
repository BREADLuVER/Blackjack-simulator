#main.py
from dice_simulation import playGame
from dice_analysis import extractAnswer

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
        LoseCount, WinCount, gam = playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)
        print("Game States:")
        for row in gam:
            print(row)
        print("LoseCount:")
        for row in LoseCount:
            print(row)
        print("WinCount:")
        for row in WinCount:
            print(row)
        BestMove, WinProbability = extractAnswer(WinCount, LoseCount, NDice, LTarget)
        # print("Best Move:")
        # for row in BestMove:
        #     print(row)
        # print("Win Probability:")
        # for row in WinProbability:
        #     print(row)
    return BestMove, WinProbability

NDice = 2
NSides = 2
LTarget = 4
UTarget = 4
NGames = 5
M = 1
BestMove, WinProbability = prog3(NDice, NSides, LTarget, UTarget, NGames, M)
# print("Best Move:", BestMove)
# print("Win Probability:", WinProbability)