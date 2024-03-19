#simulation.py
from dice_decision import chooseDice
from dice_utils import rollDice 

def playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    """
    Simulates playing one game with the given parameters, updating LoseCount and WinCount matrices based on the game's outcome.
    Tracks the game's trace for verification and debugging.
    
    Parameters:
    - NDice: Maximum number of dice a player may roll.
    - NSides: Number of sides on each die.
    - LTarget: The lowest winning score.
    - UTarget: The highest winning score.
    - LoseCount: 3D matrix tracking number of losses for each state and dice count.
    - WinCount: 3D matrix tracking number of wins for each state and dice count.
    - M: Hyperparameter for explore/exploit trade-off.
    
    Returns:
    - Updated LoseCount and WinCount matrices, and the game trace.
    """
    # Initialize player scores and game trace
    scoreA, scoreB = 0, 0
    gameTrace = []
    playerTurn = 'A'  # Starting with player A

    while True:
        # Determine current player and opponent scores
        if playerTurn == 'A':
            currentScore, opponentScore = scoreA, scoreB
        else:
            currentScore, opponentScore = scoreB, scoreA

        # Choose the number of dice to roll
        NDiceChosen = chooseDice((currentScore, opponentScore), LoseCount, WinCount, NDice, M)
        rollOutcome = rollDice(NDiceChosen, NSides)

        # Update current player's score
        currentScore += rollOutcome

        # Record the action in the game trace
        gameTrace.append((playerTurn, currentScore, NDiceChosen, rollOutcome))

        # Check for win/loss condition
        if LTarget <= currentScore <= UTarget:
            # Current player wins
            if playerTurn == 'A':
                WinCount[scoreA][scoreB][NDiceChosen] += 1
                scoreA = currentScore
            else:
                WinCount[scoreB][scoreA][NDiceChosen] += 1
                scoreB = currentScore
            break
        elif currentScore > UTarget:
            # Current player loses
            if playerTurn == 'A':
                LoseCount[scoreA][scoreB][NDiceChosen] += 1
                scoreA = currentScore
            else:
                LoseCount[scoreB][scoreA][NDiceChosen] += 1
                scoreB = currentScore
            break
        
        # Update scores based on current player
        if playerTurn == 'A':
            scoreA = currentScore
        else:
            scoreB = currentScore

        # Switch player turn
        playerTurn = 'B' if playerTurn == 'A' else 'A'

    return LoseCount, WinCount, gameTrace