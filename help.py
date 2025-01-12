from itertools import permutations

# Define the word
word = "FATE"

# Generate all unique permutations
unique_anagrams = sorted(set("".join(p) for p in permutations(word)))

# Output the sorted anagrams
print(unique_anagrams)