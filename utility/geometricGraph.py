import numpy as np
from scipy.stats import geom
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1)

p = 83890 / 270725
mean, var, skew, kurt = geom.stats(p, moments='mvsk')

x = np.arange(geom.ppf(0.0001, p),
              geom.ppf(0.99, p))
ax.plot(x, geom.pmf(x, p), 'bo', ms=8, label='geom pmf')
ax.vlines(x, 0, geom.pmf(x, p), colors='b', lw=5, alpha=0.5)

rv = geom(p)
ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
        label='frozen pmf')
ax.legend(loc='best', frameon=False)
plt.show()

prob = geom.cdf(x, p)
np.allclose(x, geom.ppf(prob, p))