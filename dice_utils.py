# Implementing Module 1: chooseFromDist(p) in dice_utils.py

import random

def chooseFromDist(p):
    """
    Selects an index based on the probability distribution provided by the list `p`.
    The index starts at 1 and goes up to the length of `p`.

    Parameters:
    - p (list of float): A list of probabilities associated with each choice. The list should sum up to 1.

    Returns:
    - int: The selected index based on the given probability distribution.
    """
    # Ensure the list sums to 1 for probability distribution
    if not 0.99 <= sum(p) <= 1.01:
        raise ValueError("The probabilities must sum up to 1.")
    
    # The choices are the possible indices, starting from 1 to len(p)
    choices = list(range(1, len(p) + 1))
    
    # Using random.choices() to select based on the distribution
    selected_choice = random.choices(choices, weights=p, k=1)[0]
    
    return selected_choice

# Remember to comment out the function call before integrating into the full program.
# Sample function call (commented out):
print(chooseFromDist([0.1, 0.2, 0.3, 0.4]))
