#simulation.py
from dice_decision import chooseDice
from dice_utils import rollDice 

def playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    scoreA, scoreB = 0, 0
    gameStates = []  # Enhanced game trace to include state transitions

    while True:
        for playerTurn in ['A', 'B']:
            currentScore, opponentScore = (scoreA, scoreB) if playerTurn == 'A' else (scoreB, scoreA)
            NDiceChosen = chooseDice((currentScore, opponentScore), LoseCount, WinCount, NDice, M)
            rollOutcome = rollDice(NDiceChosen, NSides)
            newScore = currentScore + rollOutcome
            
            # Log the state before the roll, the action taken, and the outcome
            gameStates.append(((currentScore, opponentScore, NDiceChosen), rollOutcome, newScore))

            # Update the current player's score
            if playerTurn == 'A':
                scoreA = newScore
            else:
                scoreB = newScore

            # Check win/loss conditions
            if LTarget <= newScore <= UTarget or newScore > UTarget:
                break
        if LTarget <= newScore <= UTarget or newScore > UTarget:
            finalWinner = playerTurn
            break

    # Update matrices based on game outcome
    for stateInfo in gameStates:
        state, outcome, finalScore = stateInfo
        X, Y, k = state
        
        if (finalWinner == 'A' and playerTurn == 'A') or (finalWinner == 'B' and playerTurn == 'B'):
            if LTarget <= finalScore <= UTarget:
                WinCount[X][Y][k] += 1
            else:  # This captures cases where the game continues past a winnable state
                LoseCount[X][Y][k] += 1
        else:
            LoseCount[X][Y][k] += 1

    return LoseCount, WinCount, gameStates


LTarget, UTarget, NDice, NSides, M = 4, 4, 2, 2, 0.5
LoseCount = [[[0 for _ in range(NDice + 1)] for _ in range(UTarget + 1)] for _ in range(UTarget + 1)]
WinCount = [[[0 for _ in range(NDice + 1)] for _ in range(UTarget + 1)] for _ in range(UTarget + 1)]

# Test run of playGame
def debugPlayGame(result):
    LoseCount, WinCount, game_trace = result
    # Initialize trackers for expected updates
    expected_LoseCount_updates = {}
    expected_WinCount_updates = {}

    # Process game_trace to determine expected updates
    final_score_A, final_score_B = game_trace[-1][-1], game_trace[-2][-1]  # Last two scores are the final scores of A and B
    winner = 'A' if final_score_A >= LTarget and final_score_A <= UTarget else 'B'
    loser = 'B' if winner == 'A' else 'A'

    # Iterate through game_trace to populate expected updates
    for state_info in game_trace:
        pre_state, outcome, post_state = state_info
        pre_score_A, pre_score_B, NDiceChosen = pre_state if state_info[0][0] == 'A' else (pre_state[1], pre_state[0], pre_state[2])

        key = (pre_score_A, pre_score_B, NDiceChosen)
        if winner == 'A' and state_info[0] == 'A':
            expected_WinCount_updates[key] = expected_WinCount_updates.get(key, 0) + 1
        elif loser == 'A' and state_info[0] == 'A':
            expected_LoseCount_updates[key] = expected_LoseCount_updates.get(key, 0) + 1
        elif winner == 'B' and state_info[0] == 'B':
            expected_WinCount_updates[key] = expected_WinCount_updates.get(key, 0) + 1
        elif loser == 'B' and state_info[0] == 'B':
            expected_LoseCount_updates[key] = expected_LoseCount_updates.get(key, 0) + 1

    # Compare expected updates with actual matrices
    discrepancies_found = False
    for key, expected_count in expected_WinCount_updates.items():
        if WinCount[key[0]][key[1]][key[2]] != expected_count:
            discrepancies_found = True
            print(f"Discrepancy found in WinCount at {key}: Expected {expected_count}, Found {WinCount[key[0]][key[1]][key[2]]}")
    
    for key, expected_count in expected_LoseCount_updates.items():
        if LoseCount[key[0]][key[1]][key[2]] != expected_count:
            discrepancies_found = True
            print(f"Discrepancy found in LoseCount at {key}: Expected {expected_count}, Found {LoseCount[key[0]][key[1]][key[2]]}")

    if not discrepancies_found:
        print("No discrepancies found. The game logic and matrix updates are consistent with the game trace.")

# Output the game trace and check updates to LoseCount and WinCount matrices
result = playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)
debugPlayGame(result)