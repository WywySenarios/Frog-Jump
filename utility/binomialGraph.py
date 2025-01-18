import math
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats import norm

n = 100000
p = 0.21772

mu = n * p
sd = math.sqrt(n * p * (1 - p))

x = np.linspace(mu - 3 * sd, mu + 3 * sd, n)

plt.plot(x, norm.pdf(x, mu, sd))
plt.title("Theoeretical Winrate Starting from pad 1")
plt.xlabel("Winrate")
plt.ylabel("Density")
plt.savefig("utility\\binomialGraph.png", transparent=True)
plt.show()