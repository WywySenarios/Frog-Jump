import math

def calculate_margin_of_error(z, n, p):
    """
    Calculate the margin of error for a given z-score, sample size, and probability.

    Parameters:
        z (float): Z-score corresponding to the confidence level.
        n (int): Sample size.
        p (float): Probability of the event occurring.

    Returns:
        float: Margin of error.
    """
    return z * math.sqrt((p * (1 - p)) / n)

# Input parameters
z = 5.1993  # Z-score for the given confidence level
n = 1_000_000_000  # Sample size (1 billion)
p = 0.217667844381  # Probability of the event occurring

# Calculate margin of error
margin_of_error = calculate_margin_of_error(z, n, p)

margin_of_error = 1 - margin_of_error

# Output the result
print(f"Given:")
print(f"  Z-score: {z}")
print(f"  Sample size (n): {n}")
print(f"  Probability (p): {p}")
print(f"The expected error (margin of error) is approximately {margin_of_error:.10f}")