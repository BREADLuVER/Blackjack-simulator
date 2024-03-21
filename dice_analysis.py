#analysis.py
def extractAnswer(WinCount, LoseCount, NDice, LTarget):
    optimal_dice_matrix = [[0 for _ in range(LTarget)] for _ in range(LTarget)]
    win_prob_matrix = [[0 for _ in range(LTarget)] for _ in range(LTarget)]
    
    for X in range(LTarget):
        for Y in range(LTarget):
            max_prob = 0
            optimal_dice = 0
            for k in range(1, NDice + 1):
                total_games = WinCount[X][Y][k] + LoseCount[X][Y][k]
                if total_games > 0:
                    win_prob = WinCount[X][Y][k] / total_games
                    if win_prob > max_prob:
                        max_prob = win_prob
                        optimal_dice = k
                else:
                    win_prob = 0
                
                if k == 1:  # Ensure we have a default value even if all probs are 0
                    optimal_dice = 1
                
            optimal_dice_matrix[X][Y] = optimal_dice
            win_prob_matrix[X][Y] = max_prob
            
    return optimal_dice_matrix, win_prob_matrix
