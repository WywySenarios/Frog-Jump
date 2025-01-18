import json

PROBABILITY_CONSTANTS = json.loads(open("utility/a.json", "r").read())
DECIMAL_PLACES = 5

# all values of a
a = {
    0: 0,
    1: 1,
}

output = open("output.txt", "w+")

def findPConstant(letter: str, i: int):
    return PROBABILITY_CONSTANTS[str(i)][letter + "n"] / PROBABILITY_CONSTANTS[str(i)][letter + "d"]

for i in range(2,6):
    a[i] = (a[i - 1] - findPConstant("b", i - 1) * a[i - 2]) / findPConstant("f", i - 1)
    
    output.write("a_" + str(i) + " = \\frac{a_" + str(i - 1) + " - P_b(" + str(i - 1) + ") \\cdot a_" + str(i - 2) + "}{P_f(" + str(i - 1) + ")}\n")
    output.write("a_" + str(i) + " = \\frac{" + str(round(a[i - 1], DECIMAL_PLACES)) + " - " + str(round(findPConstant("b", i - 1), DECIMAL_PLACES)) + " \\cdot " + str(round(a[i - 2], DECIMAL_PLACES)) + "}{" + str(round(findPConstant("f", i - 1), DECIMAL_PLACES)) + "}\n")
    output.write("a_" + str(i) + " = " + str(round(a[i], DECIMAL_PLACES)) + "\n")

output.close()

print("Final probability: " + str(round(findPConstant("f", 5) / (a[5] - findPConstant("b", 5) * a[4]), DECIMAL_PLACES)))