#analysis.py
def extractAnswer(WinCount, LoseCount, NDice, LTarget):
    BestMove = [[0 for _ in range(LTarget)] for _ in range(LTarget)]
    WinProbability = [[0 for _ in range(LTarget)] for _ in range(LTarget)]
    
    for X in range(LTarget):
        for Y in range(LTarget):
            best_k = 1
            highest_win_prob = -1
            for k in range(1, NDice + 1):
                total_games = WinCount[X][Y][k] + LoseCount[X][Y][k]
                if total_games > 0:
                    win_prob = WinCount[X][Y][k] / total_games
                    if win_prob > highest_win_prob:
                        highest_win_prob = win_prob
                        best_k = k
                elif highest_win_prob == -1:  # Case where no games played for this state
                    highest_win_prob = 0.5  # Default to neutral probability if no data
                
            BestMove[X][Y] = best_k
            WinProbability[X][Y] = highest_win_prob

    return BestMove, WinProbability



# Since we cannot run this function without the actual WinCount and LoseCount matrices, 
# this code serves as a template for how you would implement the logic based on the provided strategy.

