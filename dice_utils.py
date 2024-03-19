#dice_utils.py
import random
from collections import Counter

def chooseFromDist(p):
    """
    Selects an index based on the probability distribution provided by the list `p`.
    The index starts at 1 and goes up to the length of `p`.

    Parameters:
    - p (list of float): A list of probabilities associated with each choice. The list should sum up very close to 1.

    Returns:
    - int: The selected index based on the given probability distribution.
    """
    # Ensure the list sums very close to 1 for probability distribution, allowing a tiny margin for floating-point inaccuracies
    if not 0.999 <= sum(p) <= 1.001:
        raise ValueError("The probabilities must sum up very close to 1.")
    
    # The choices are the possible indices, starting from 1 to len(p)
    choices = list(range(1, len(p) + 1))
    
    # Using random.choices() to select based on the distribution
    selected_choice = random.choices(choices, weights=p, k=1)[0]
    
    return selected_choice

def rollDice(NDice, NSides):
    """
    Simulates rolling a specified number of dice, each with a specified number of sides, and returns the total score.

    Parameters:
    - NDice (int): The number of dice to roll.
    - NSides (int): The number of sides on each die.

    Returns:
    - int: The total score from rolling the dice.
    """
    # Simulating the dice rolls using a list comprehension and summing the results
    total_score = sum(random.randint(1, NSides) for _ in range(NDice))
    
    return total_score


# Testing the chooseFromDist function
def test_chooseFromDist(p, trials=1000):
    """
    Test the chooseFromDist function by running it multiple times and tallying the results.

    Parameters:
    - p (list of float): The probability distribution to test.
    - trials (int): The number of trials to run the test.
    """
    results = [chooseFromDist(p) for _ in range(trials)]
    counts = Counter(results)
    
    # Displaying the frequency of each choice
    for choice, count in sorted(counts.items()):
        print(f"Choice {choice}: {count} times ({(count / trials) * 100:.2f}%)")

# Example probability distribution
p = [0.1, 0.2, 0.3, 0.4]
#print(rollDice(2, 6))

# Run the test
#test_chooseFromDist(p)
