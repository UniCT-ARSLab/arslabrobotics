#
#
#

__all__ = [
    "plot_fuzzysets",
    "plot_set"
    ]

import numpy as np
from matplotlib import pylab

STEPS = 100

def plot_set(X, Ya, points = None, labels = None, title = None):
    pylab.figure(1)
    i = 0
    for y in Ya:
        if labels is None:
            lab = str(i+1)
        else:
            lab = labels[i]
        pylab.plot(X, y, label = lab)
        i += 1
    if points is not None:
        for x,y in points:
            pylab.plot([x], [y], "+")
    #pylab.xlabel(self.x_label)
    if title is not None:
        pylab.title(title)
    pylab.legend()
    pylab.show()


def plot_fuzzysets(fuzzysets, title = None):
    lows = []
    highs = []
    for _set in fuzzysets:
        (low, high) = _set.get_limits()
        lows.append(low)
        highs.append(high)

    low = min(lows)
    high = max(highs)

    X = np.arange(low, high, (high - low) / STEPS)
    Y = []
    labels = []
    for _set in fuzzysets:
        Y.append([_set.fuzzify(v) for v in X])
        labels.append(_set.name())
    plot_set(X, Y, labels = labels, title = title)


