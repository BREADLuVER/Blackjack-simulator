#simulation.py
from dice_decision import chooseDice
from dice_utils import rollDice 

def playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    scoreA, scoreB = 0, 0  # Scores for player A and B initially
    currentPlayer = 'A'  # Player A starts
    gameStates = []  # Track the progress and decisions of the game

    while True:
        # Assuming chooseDice function determines the number of dice to roll; simplified here
        nDice = NDice  # Simplification for illustration; should be determined by chooseDice function
        
        # Roll the dice and update score
        rollOutcome = rollDice(nDice, NSides)
        if currentPlayer == 'A':
            scoreA += rollOutcome
            if scoreA > UTarget:  # A loses
                print("A loses")
                for state in gameStates:
                    LoseCount[state['scoreA']][state['scoreB']][state['nDice']] += 1
                LoseCount[scoreA][scoreB][nDice] += 1  # Update for the losing move
                gameStates.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice, 'rollOutcome': rollOutcome})
                break
            elif scoreA >= LTarget:  # A wins
                print("A wins")
                for state in gameStates:
                    WinCount[state['scoreA']][state['scoreB']][state['nDice']] += 1
                WinCount[scoreA][scoreB][nDice] += 1  # Update for the winning move
                gameStates.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice, 'rollOutcome': rollOutcome})
                break
        else:
            scoreB += rollOutcome
            if scoreB > UTarget:  # B loses
                print("B loses")
                for state in gameStates:
                    LoseCount[state['scoreB']][state['scoreA']][state['nDice']] += 1
                LoseCount[scoreB][scoreA][nDice] += 1  # Update for the losing move
                gameStates.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice, 'rollOutcome': rollOutcome})
                break
            elif scoreB >= LTarget:  # B wins
                print("B wins")
                for state in gameStates:
                    WinCount[state['scoreB']][state['scoreA']][state['nDice']] += 1
                WinCount[scoreB][scoreA][nDice] += 1  # Update for the winning move
                gameStates.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice, 'rollOutcome': rollOutcome})
                break

        # Record the current game state before switching players
        gameStates.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice, 'rollOutcome': rollOutcome})
        
        # Switch players
        currentPlayer = 'B' if currentPlayer == 'A' else 'A'

    return LoseCount, WinCount, gameStates


LTarget, UTarget, NDice, NSides, M = 4, 4, 2, 2, 0.5
MaxScore = UTarget + (NDice * NSides)
LoseCount = [[[0 for _ in range(NDice + 1)] for _ in range(MaxScore + 1)] for _ in range(MaxScore + 1)]
WinCount = [[[0 for _ in range(NDice + 1)] for _ in range(MaxScore + 1)] for _ in range(MaxScore + 1)]


# Output the game trace and check updates to LoseCount and WinCount matrices
l, q, gameStates = playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)
print("Game States:")
print(gameStates)
print("LoseCount:")
print(l)
print("WinCount:")
print(q)