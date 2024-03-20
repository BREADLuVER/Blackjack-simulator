#simulation.py
from dice_decision import chooseDice
from dice_utils import rollDice 

def playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    scoreA, scoreB = 0, 0  # Initial scores for both players
    currentPlayer = 'A'  # Start with Player A
    gameStates = []  # Track the progress of the game

    while True:
        # Choose the number of dice to roll based on the strategy (simplified here to always roll NDice)
        nDice = NDice

        # Roll dice and update the current player's score
        rollOutcome = rollDice(nDice, NSides)
        if currentPlayer == 'A':
            scoreA += rollOutcome
        else:
            scoreB += rollOutcome

        # Track the current state
        gameStates.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice, 'rollOutcome': rollOutcome})

        # Check win/loss condition
        if scoreA > UTarget or scoreB > UTarget or scoreA >= LTarget and scoreA <= UTarget or scoreB >= LTarget and scoreB <= UTarget:
            break

        # Alternate the player
        currentPlayer = 'B' if currentPlayer == 'A' else 'A'

    # After the game ends, update WinCount and LoseCount based on the gameStates
    for state in gameStates:
        player = state['player']
        scoreA = state['scoreA']
        scoreB = state['scoreB']
        nDice = state['nDice']

        if (player == 'A' and scoreA >= LTarget and scoreA <= UTarget) or (player == 'B' and scoreB >= LTarget and scoreB <= UTarget):
            # Player won
            WinCount[scoreA][scoreB][nDice] += 1
        else:
            # Player lost
            LoseCount[scoreA][scoreB][nDice] += 1

    return LoseCount, WinCount, gameStates


    LTarget, UTarget, NDice, NSides, M = 4, 4, 2, 2, 0.5
    maxScore = max(UTarget, NDice * NSides)
    LoseCount = [[[0 for _ in range(NDice + 1)] for _ in range(maxScore + 1)] for _ in range(maxScore + 1)]
    WinCount = [[[0 for _ in range(NDice + 1)] for _ in range(maxScore + 1)] for _ in range(maxScore + 1)]


LTarget, UTarget, NDice, NSides, M = 4, 4, 2, 2, 0.5
MaxScore = UTarget + (NDice * NSides)
LoseCount = [[[0 for _ in range(NDice + 1)] for _ in range(MaxScore + 1)] for _ in range(MaxScore + 1)]
WinCount = [[[0 for _ in range(NDice + 1)] for _ in range(MaxScore + 1)] for _ in range(MaxScore + 1)]

# Output the game trace and check updates to LoseCount and WinCount matrices
result = playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)
print(result)