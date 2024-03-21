#dice_decision.py

import random
from dice_utils import chooseFromDist

def calculate_fk(Score, LoseCount, WinCount, k):
    X, Y = Score
    wins = WinCount[X][Y][k]
    losses = LoseCount[X][Y][k]

    # If both wins and losses are zero, return 0.5
    if wins == 0 and losses == 0:
        return 0.5

    # If wins are not zero but losses are, avoid division by zero by returning 0
    # This is a special case where you might expect to return 1 (since wins occurred without loss)
    # But as per your instruction, if there's a potential division by zero, return 0.
    if wins == 0:
        return 0

    # Otherwise, calculate fk as normal
    total = wins + losses
    return wins / total


def identify_best_action(f):
    """
    Identify the best action (k^) based on the highest fk value.
    
    Parameters:
    - f (list): List of fk values for each possible action.
    
    Returns:
    - int: The action (k) with the highest fk value.
    """
    return f.index(max(f)) + 1  # Adding 1 because actions (k) start from 1

def calculate_probabilities(Score, LoseCount, WinCount, NDice, M):
    X, Y = Score
    T = round(sum(WinCount[X][Y][k] + LoseCount[X][Y][k] for k in range(1, NDice + 1)), 2)
    f = [round(calculate_fk(Score, LoseCount, WinCount, k), 2) for k in range(1, NDice + 1)]

    max_fk = max(f)
    # Find all k values that have the highest fk
    best_actions = [k for k, fk in enumerate(f, start=1) if fk == max_fk]
    
    # Randomly choose among the best actions if there are multiple
    k_hat = random.choice(best_actions)
    # Finding the best action based on the highest fk value

    fk_hat = round(f[k_hat - 1], 2)
    s = round(sum(f[k - 1] for k in range(1, NDice + 1) if k != k_hat), 2)

    pk_hat = round((T * fk_hat + M) / (T * fk_hat + NDice * M), 2)
    
    probabilities = [0] * NDice
    for k in range(1, NDice + 1):
        if k == k_hat:
            probabilities[k - 1] = pk_hat
        else:
            pk = round((1 - pk_hat) * (T * f[k - 1] + M) / (s * T + (NDice - 1) * M), 2)
            probabilities[k - 1] = pk


        print(f'For dice {k}:')
        print(f'  WinCount[{X},{Y},{k}]: {WinCount[X][Y][k]}')
        print(f'  LoseCount[{X},{Y},{k}]: {LoseCount[X][Y][k]}')
        print(f'  fk for this dice: {f[k - 1]} (calculated as {WinCount[X][Y][k]} / ({WinCount[X][Y][k]} + {LoseCount[X][Y][k]}))')
        if k == k_hat:
            print(f'  pk for this dice: {probabilities[k - 1]} (calculated as ({T} * {fk_hat} + {M}) / ({T} * {fk_hat} + {NDice} * {M}) = {T * fk_hat + M} / {T * fk_hat + NDice * M})')
        else:
            print(f'  pk for this dice: {probabilities[k - 1]} (calculated as (1 - {pk_hat}) * ({T} * {f[k - 1]} + {M}) / ({s} * {T} + ({NDice} - 1) * {M}) = {(1 - pk_hat) * (T * f[k - 1] + M)} / {s * T + (NDice - 1) * M})')
    
    print(f'k_hat (best action): {k_hat}')
    print(f'fk_hat (value of best action): {fk_hat}')
    print(f'T: {T}')
    print(f's: {s}')
    print(f'pk_hat: {pk_hat}')
    print()
    
    return probabilities

def chooseDice(Score, LoseCount, WinCount, NDice, M):
    """
    Choose the number of dice to roll based on the current state and historical data.
    
    Parameters:
    - Score (tuple): Current score of the player and opponent (X, Y).
    - LoseCount (3D array): Tracks the number of losses.
    - WinCount (3D array): Tracks the number of wins.
    - NDice (int): Maximum number of dice a player can roll.
    - M (float): Hyperparameter controlling the explore/exploit trade-off.
    
    Returns:
    - int: The chosen number of dice to roll.
    """
    f = [calculate_fk(Score, LoseCount, WinCount, k) for k in range(1, NDice + 1)]
    k_hat = identify_best_action(f)
    probabilities = calculate_probabilities(Score, LoseCount, WinCount, NDice, M)
    #print("Probabilities:", probabilities)
    # Using the provided chooseFromDist function to select the number of dice based on the calculated probabilities
    chosen_dice = chooseFromDist(probabilities)
    print
    return chosen_dice

def test_chooseDice(NDice, NSides, LTarget, UTarget, M, test_runs=1000):
    """
    Test the chooseDice function by simulating a simple game environment and observing the distribution of chosen actions.
    
    Parameters:
    - NDice (int): Maximum number of dice a player can roll.
    - NSides (int): Number of sides on the dice.
    - LTarget (int): Lowest winning value.
    - UTarget (int): Highest winning value.
    - M (float): Hyperparameter for explore/exploit trade-off.
    - test_runs (int): Number of test runs to perform.
    
    Returns:
    - dict: Distribution of chosen actions (number of dice rolled) across the test runs.
    """
    # Initialize WinCount and LoseCount matrices with arbitrary values for testing
    WinCount = [[[0 for _ in range(NDice + 1)] for _ in range(UTarget + 1)] for _ in range(UTarget + 1)]
    LoseCount = [[[0 for _ in range(NDice + 1)] for _ in range(UTarget + 1)] for _ in range(UTarget + 1)]
    
    # Populate some values to simulate a game history
    for x in range(LTarget, UTarget + 1):
        for y in range(LTarget, UTarget + 1):
            for k in range(1, NDice + 1):
                WinCount[x][y][k] = random.randint(0, 10)
                LoseCount[x][y][k] = random.randint(0, 10)
    
    # Run the test and track the distribution of chosen dice
    chosen_dice_distribution = {k: 0 for k in range(1, NDice + 1)}
    for _ in range(test_runs):
        # Randomly select a current score within the target range for testing
        Score = (random.randint(LTarget, UTarget), random.randint(LTarget, UTarget))
        chosen_dice = chooseDice(Score, LoseCount, WinCount, NDice, M)
        chosen_dice_distribution[chosen_dice] += 1
    
    return chosen_dice_distribution

# Assuming the definitions of chooseFromDist and rollDice are provided and correct,
# let's perform a test run with some example parameters.
# Note: This test assumes chooseFromDist is defined within the chooseDice function or globally accessible.

# test_distribution = test_chooseDice(NDice=2, NSides=6, LTarget=15, UTarget=17, M=4, test_runs=20)
# print("Chosen Dice Distribution:")
# for k, count in test_distribution.items():
#     print(f"Dice {k}: {count} times ({(count / 1000) * 100:.2f}%)")