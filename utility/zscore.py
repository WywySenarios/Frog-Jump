import scipy.stats as stats


confidence_level = float(input("Enter the confidence level as a percentage (e.g. 95.0): "))
alpha = 1 - confidence_level / 100
cumulative_probability = 1 - (alpha / 2)
z_score = stats.norm.ppf(cumulative_probability)

print(f"The z_score is: {z_score:.4f}")