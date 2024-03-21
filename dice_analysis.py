#analysis.py
def extractAnswer(WinCount, LoseCount, NDice, LTarget):
    """
    Extracts the best move (number of dice to roll) and the win probability for each state in the game.

    Parameters:
    - WinCount: A 3D list containing win counts for each state and dice count.
    - LoseCount: A 3D list containing lose counts for each state and dice count.
    - NDice: The maximum number of dice that can be rolled.
    - LTarget: The lower target score for winning.

    Returns:
    - BestMove: A 2D list indicating the best number of dice to roll for each state.
    - WinProbability: A 2D list indicating the win probability for the best move in each state.
    """
    # Initialize matrices to store the best move and the win probability for each state
    BestMove = [[0 for _ in range(LTarget + 1)] for _ in range(LTarget + 1)]
    WinProbability = [[0 for _ in range(LTarget + 1)] for _ in range(LTarget + 1)]
    
    # Iterate over each possible state
    for X in range(LTarget + 1):
        for Y in range(LTarget + 1):
            # Variables to keep track of the best move and its win probability
            best_prob = 0
            best_dice = 0
            
            # Iterate over each possible number of dice to roll
            for k in range(1, NDice + 1):
                total_games = WinCount[X][Y][k] + LoseCount[X][Y][k]
                win_prob = WinCount[X][Y][k] / total_games if total_games > 0 else 0
                
                # Update the best move if this move has a higher win probability
                if win_prob > best_prob:
                    best_prob = win_prob
                    best_dice = k
            
            # Update the matrices with the best move and its win probability
            BestMove[X][Y] = best_dice
            WinProbability[X][Y] = best_prob
    
    return BestMove, WinProbability

# Since we cannot run this function without the actual WinCount and LoseCount matrices, 
# this code serves as a template for how you would implement the logic based on the provided strategy.

