import math
import numpy as np
from scipy.stats import geom
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1)

p = 1 - 83890 / 270725

x = []
y = []
for i in range(1, 10):
    datum = math.pow(1 - p, i - 1) * p
    y.append(datum)
    x.append(i)

plt.bar(x, y)
plt.title("Probability of Leaving Lily Pad 2 on Round x")
plt.xlabel("x = leaving liliy pad on round x")
plt.ylabel("P(X = x)")
plt.show()