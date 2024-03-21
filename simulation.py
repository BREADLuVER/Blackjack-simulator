#simulation.py
from dice_decision import chooseDice
from dice_utils import rollDice 
# gameStates = [] 
# gameStates.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice, 'rollOutcome': rollOutcome})

def playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    import random

    # Initial scores and starting player
    scoreA, scoreB = 0, 0
    currentPlayer = 'A'

    # Store the game states for trace
    gameStates = []

    # Helper function to simulate dice rolls
    def rollDice(nDice, NSides):
        return sum(random.randint(1, NSides) for _ in range(nDice))

    # Loop until one of the players wins
    while True:
        # Roll dice and update score
        rollOutcome = rollDice(NDice, NSides)
        if currentPlayer == 'A':
            scoreA += rollOutcome
            prevState = [scoreA - rollOutcome, scoreB, NDice]  # Current player's previous score, opponent's score, dice count
        else:
            scoreB += rollOutcome
            prevState = [scoreB - rollOutcome, scoreA, NDice]  # Current player's previous score, opponent's score, dice count

        # Record the game state
        gameStates.append({
            'player': currentPlayer,
            'scoreA': scoreA,
            'scoreB': scoreB,
            'nDice': NDice,
            'rollOutcome': rollOutcome
        })

        print(f'prevState {prevState}')
        # Check win condition or if a player's score goes beyond UTarget
        if LTarget <= scoreA <= UTarget:
            # Iterating through gameStates to update WinCount and LoseCount accordingly
            for state in gameStates:
                player, scoreA, scoreB, nDice = state['player'], state['scoreA'], state['scoreB'], state['nDice']
                print(f'win middleA: player {player} scoreA {scoreA} scoreB {scoreB} nDice {nDice}')
                if player == 'A':
                    if scoreA > scoreB:
                        WinCount[scoreA-nDice][scoreB][nDice] += 1
                    else:
                        LoseCount[scoreA-nDice][scoreB][nDice] += 1
                else:
                    if scoreB > scoreA:
                        WinCount[scoreB-nDice][scoreA][nDice] += 1
                    else:
                        LoseCount[scoreB-nDice][scoreA][nDice] += 1
            break
        elif LTarget <= scoreB <= UTarget:
            # Similar iteration for player B
            for state in gameStates:
                player, scoreA, scoreB, nDice = state['player'], state['scoreA'], state['scoreB'], state['nDice']
                print(f'win middleB: player {player} scoreA {scoreA} scoreB {scoreB} nDice {nDice}')
                if player == 'B':
                    if scoreB > scoreA:
                        WinCount[scoreB-nDice][scoreA][nDice] += 1
                    else:
                        LoseCount[scoreB-nDice][scoreA][nDice] += 1
                else:
                    if scoreA > scoreB:
                        WinCount[scoreA-nDice][scoreB][nDice] += 1
                    else:
                        LoseCount[scoreA-nDice][scoreB][nDice] += 1
            break
        elif scoreA > UTarget:
            for state in gameStates:
                player, scoreA, scoreB, nDice = state['player'], state['scoreA'], state['scoreB'], state['nDice']
                print(f'lose upperA: player {player} scoreA {scoreA} scoreB {scoreB} nDice {nDice}')
                if player == 'B':
                    WinCount[scoreB-nDice][scoreA][nDice] += 1
                else:
                    LoseCount[scoreA-nDice][scoreB][nDice] += 1
            break
        
        elif scoreB > UTarget:
            for state in gameStates:
                player, scoreA, scoreB, nDice = state['player'], state['scoreA'], state['scoreB'], state['nDice']
                print(f'lose upperA: player {player} scoreA {scoreA} scoreB {scoreB} nDice {nDice}')
                if player == 'A':
                    WinCount[scoreA-nDice][scoreB][nDice] += 1
                else:
                    LoseCount[scoreB-nDice][scoreA][nDice] += 1
            break

        # Switch player
        currentPlayer = 'B' if currentPlayer == 'A' else 'A'
        # Adjust NDice based on M
        NDice = 1 if random.random() < M else 2

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
for i in l:
    print(i)
print("WinCount:")
for i in q:
    print(i)