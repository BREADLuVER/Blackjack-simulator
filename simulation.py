#simulation.py
import random
from dice_decision import chooseDice
from dice_utils import rollDice 
# gameStates = [] 
# gameStates.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice, 'rollOutcome': rollOutcome})

def playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    scoreA, scoreB = 0, 0  # Initial scores for both players
    currentPlayer = 'A'  # Starting player
    gameStates = []  # Track the sequence of game states
    prev_state=[]
    while True:
        # Determine number of dice to roll - could be enhanced with strategy
        nDice = random.randint(1, NDice)  # Randomly choose the number of dice to roll

        # Record the state before the roll
        if currentPlayer == 'A':
            prevState = (scoreA, scoreB, nDice)
        else: 
            prevState=(scoreB, scoreA, nDice)
        print(prevState)
        prev_state.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice})
        # Roll the dice
        dice = chooseDice((scoreA, scoreB), LoseCount, WinCount, NDice, M)
        rollOutcome = rollDice(dice, NSides)

        # Update scores
        if currentPlayer == 'A':
            scoreA += rollOutcome
        else:
            scoreB += rollOutcome

        # Log the game state
        gameStates.append({'player': currentPlayer, 'scoreA': scoreA, 'scoreB': scoreB, 'nDice': nDice, 'rollOutcome': rollOutcome})

        # Check for win or exceed conditions to break the loop
        if scoreA >= LTarget and scoreA <= UTarget or scoreB > UTarget or scoreB >= LTarget and scoreB <= UTarget or scoreA > UTarget:
            break

        # Switch players
        currentPlayer = 'B' if currentPlayer == 'A' else 'A'

    # Update Win/Lose counts based on game outcome
    winner = 'A' if LTarget <= scoreA <= UTarget else 'B'
    for state in (prev_state):
        if state['player'] == winner:
            if winner == 'A':
                WinCount[state['scoreA']][state['scoreB']][state['nDice']] += 1
            else:
                WinCount[state['scoreB']][state['scoreA']][state['nDice']] += 1
        else:
            if winner == 'A':
                LoseCount[state['scoreA']][state['scoreB']][state['nDice']] += 1
            else:
                LoseCount[state['scoreB']][state['scoreA']][state['nDice']] += 1

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