

def extractAnswer(WinCount, LoseCount, NDice):
    """
    Extracts the best move and winning probability for each game state.

    Parameters:
    - WinCount: 3D list of win counts.
    - LoseCount: 3D list of lose counts.
    - NDice: Maximum number of dice that can be rolled.

    Returns:
    - A tuple of two 2D lists: (BestMoveMatrix, WinProbMatrix)
      - BestMoveMatrix[X][Y] contains the best move for state (X, Y).
      - WinProbMatrix[X][Y] contains the probability of winning for the best move in state (X, Y).
    """
    LTarget = len(WinCount)  # Assuming square matrices for simplicity
    BestMoveMatrix = [[0 for _ in range(LTarget)] for _ in range(LTarget)]
    WinProbMatrix = [[0.0 for _ in range(LTarget)] for _ in range(LTarget)]

    for X in range(LTarget):
        for Y in range(LTarget):
            best_fk = -1
            best_k = 0
            for k in range(1, NDice + 1):  # Assuming k starts at 1
                wins = WinCount[X][Y][k]
                losses = LoseCount[X][Y][k]
                total = wins + losses
                fk = 0.5 if total == 0 else wins / total

                if fk > best_fk:
                    best_fk = fk
                    best_k = k

            BestMoveMatrix[X][Y] = best_k
            WinProbMatrix[X][Y] = best_fk if total > 0 else 0.0  # Adjust based on game rules for undefined states

    return (BestMoveMatrix, WinProbMatrix)