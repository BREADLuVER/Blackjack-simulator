#dice_decision.py

import random
from dice_utils import chooseFromDist

def calculate_fk(Score, LoseCount, WinCount, k):
    """
    Calculate fk for a given k, where fk is the ratio of wins to total games played for a specific number of dice rolled.
    
    Parameters:
    - Score (tuple): Current score of the player and opponent (X, Y).
    - LoseCount (3D array): Tracks the number of losses for each state and number of dice.
    - WinCount (3D array): Tracks the number of wins for each state and number of dice.
    - k (int): Number of dice rolled.
    
    Returns:
    - float: The calculated fk value.
    """
    X, Y = Score
    wins = WinCount[X][Y][k]
    losses = LoseCount[X][Y][k]
    total = wins + losses
    if total == 0:
        return 0.5
    else:
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

def calculate_probabilities(Score, LoseCount, WinCount, NDice, M, k_hat):
    """
    Calculate the probabilities for choosing each number of dice to roll.
    
    Parameters:
    - Score (tuple): Current score of the player and opponent (X, Y).
    - LoseCount (3D array): Tracks the number of losses.
    - WinCount (3D array): Tracks the number of wins.
    - NDice (int): Maximum number of dice a player can roll.
    - M (float): Hyperparameter controlling the explore/exploit trade-off.
    - k_hat (int): Best action determined by highest fk value.
    
    Returns:
    - list: List of probabilities for choosing each number of dice to roll.
    """
    X, Y = Score
    T = sum(WinCount[X][Y][k] + LoseCount[X][Y][k] for k in range(1, NDice + 1))
    f = [calculate_fk(Score, LoseCount, WinCount, k) for k in range(1, NDice + 1)]
    s = sum(f[k - 1] for k in range(1, NDice + 1) if k != k_hat)
    
    probabilities = []
    for k in range(1, NDice + 1):
        if k == k_hat:
            pk = (T * f[k - 1] + M) / (T * f[k - 1] + NDice * M)
        else:
            pk = ((1 - (T * f[k_hat - 1] + M) / (T * f[k_hat - 1] + NDice * M)) * s * T) / (T * f[k - 1] + M + (NDice - 1) * M)
        probabilities.append(pk)
    
    # Normalizing probabilities to ensure they sum to 1 due to potential rounding errors
    total_prob = sum(probabilities)
    normalized_probabilities = [p / total_prob for p in probabilities]
    
    return normalized_probabilities

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
    probabilities = calculate_probabilities(Score, LoseCount, WinCount, NDice, M, k_hat)
    #print("Probabilities:", probabilities)
    # Using the provided chooseFromDist function to select the number of dice based on the calculated probabilities
    chosen_dice = chooseFromDist(probabilities)
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

test_distribution = test_chooseDice(NDice=2, NSides=6, LTarget=15, UTarget=17, M=4, test_runs=1000)