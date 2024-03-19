# Implementing Module 3: chooseDice(Score, LoseCount, WinCount, NDice, M) in decision_making.py

def chooseDice(X, Y, WinCount, LoseCount, NDice, M):
    """
    Choose the number of dice to roll, given the current scores, WinCount, LoseCount matrices, maximum number of dice, and the hyperparameter M.
    
    Parameters:
    - X (int): Current player's score.
    - Y (int): Opponent's score.
    - WinCount (3D list): Matrix tracking wins.
    - LoseCount (3D list): Matrix tracking losses.
    - NDice (int): Maximum number of dice that can be rolled.
    - M (float): Hyperparameter controlling explore/exploit balance.
    
    Returns:
    - int: Optimal number of dice to roll.
    """
    best_choice = 1
    highest_pk = 0  # Initialize highest probability
    
    for k in range(1, NDice + 1):
        wins = WinCount[X][Y][k]
        losses = LoseCount[X][Y][k]
        total = wins + losses
        
        # Handling the case where no data is available by defaulting fk to a neutral value
        fk = 0.5 if total == 0 else wins / total
        
        # Calculate pk based on the formula provided in the assignment
        pk = (fk + M) / (1 + M * NDice) if total > 0 else 1 / NDice  # Default to even distribution if no data
        
        if pk > highest_pk:
            highest_pk = pk
            best_choice = k
    
    return best_choice


def test_chooseDice_early_game():
    # Objective: Verify the function defaults to an even distribution when lacking data.
    
    # Setup: Minimal data indicating an early stage in the game.
    X, Y = 5, 5  # Current scores
    NDice = 3  # Max number of dice
    M = 100  # High exploration factor due to early game
    WinCount = [[[0 for k in range(NDice + 1)] for j in range(11)] for i in range(11)]
    LoseCount = [[[0 for k in range(NDice + 1)] for j in range(11)] for i in range(11)]
    
    # Expected Result: With no data, the choice should default to 1/NDice, thus evenly distributed but due to implementation, it should choose 1.
    expected_choice = 1
    
    # Call to chooseDice
    actual_choice = chooseDice(X, Y, WinCount, LoseCount, NDice, M)
    
    # Print the result
    print(f"Expected: {expected_choice}, Actual: {actual_choice}")

test_chooseDice_early_game()
