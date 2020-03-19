"""
    Make a plot to show how dense the gamma lines are.

    Showing the maximum number of nuclides across the
    0 - 4 MeV range which all share the same bin (similar energies).

    We take advantage of the Line Aggregator to iterate over
    all lines per nuclide, only logging a nuclide once in each bin at most.

    Obviously if we only have 1 bin then this should be all (~1709) nuclides
    with gamma lines.

    If looping to high number of bins (script goes upto 1 million) it can take
    some time, but uses multiprocessing to speed things up.

    This has been precomputed with high number of bins, and you can simply plot
    these or run the script yourself. 
"""

import matplotlib.pyplot as plt
import math
import numpy as np
import multiprocessing
from tqdm import tqdm

import actigamma as ag


# we want to look at the density 
# (the number of of nuclides with gamma lines
# within a certain energy range)
class BinaryLineAggregator(ag.LineAggregator):
    """
        We just want to know if a line exists or not.
        We don't care about activities.
    """
    def _makehist(self, *args, **kwargs):
        hist = np.zeros(self.grid.nrofbins)

        include_same_nuclide = False
        if 'include_same_nuclide' in kwargs and kwargs['include_same_nuclide']:
            include_same_nuclide = True

        if len(self.lines) > 0:
            self._sortlines()

            average_energies = self.grid.midpoints

            # loop over lines to find appropriate bin
            ibin = 0
            for i, line in enumerate(self.lines):
                # loop over bounds from the last found bin
                for j in range(ibin, len(self.grid) - 1):
                    if line >= self.grid[j] and line < self.grid[j + 1]:
                        if include_same_nuclide:
                            hist[j] += (1 if self.values[i] > 0 else 0)
                        else:
                            hist[j] = (1 if self.values[i] > 0 else hist[j])
                        ibin = j
                        break

        return hist, self.grid.bounds

SPECTYPE = "gamma"
MIN_ENERGY = 0.0
MAX_ENERGY = 4e6

# setup the DB
db = ag.Decay2012Database()

# loop through possible different binning
bins = ag.logspace(0, 6, 20)
    
def getmaxcount(nrofbins):
    grid = ag.EnergyGrid(bounds=ag.linspace(MIN_ENERGY, MAX_ENERGY, math.floor(nrofbins)+1))

    # bin the lines appropriately
    lc = BinaryLineAggregator(db, grid)

    hist = np.zeros(grid.nrofbins)
    bin_edges = grid.bounds
    for nuclide in tqdm(db.allnuclidesoftype(spectype=SPECTYPE)):
        inv = ag.UnstablesInventory(data=[(db.getzai(nuclide), 1)])
        h, _ = lc(inv, spectype=SPECTYPE)
        hist += h

    return np.max(hist)

# # Get the lines
# pool = multiprocessing.Pool(processes = 4)
# y = pool.map(getmaxcount, bins)
# print(bins)
# print(y)

# Or simply plot
# previously ran results
bins = ag.logspace(0, 7, 30)
y = [1707.0, 1707.0, 1680.0, 1625.0, 1499.0, 1300.0, 
    1116.0, 954.0, 780.0, 611.0, 448.0, 316.0, 214.0, 
    143.0, 101.0, 64.0, 44.0, 31.0, 26.0, 15.0, 14.0, 
    13.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0]

plt.plot(bins, y, 'ko')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of bins', fontsize=18)
plt.ylabel('Max nr. unique nuclides', fontsize=18)

# look at the lines for one type of binning.
# bin the lines appropriately
grid = ag.EnergyGrid(bounds=ag.linspace(MIN_ENERGY, MAX_ENERGY, 1000))
lc = BinaryLineAggregator(db, grid)

hist = np.zeros(grid.nrofbins)
bin_edges = grid.bounds
for nuclide in tqdm(db.allnuclidesoftype(spectype=SPECTYPE)):
    inv = ag.UnstablesInventory(data=[(db.getzai(nuclide), 1)])
    h, _ = lc(inv, spectype=SPECTYPE)
    hist += h

# make a plot of cumulative 
cumsum_hist = np.cumsum(hist)
X, Y = ag.getplotvalues(bin_edges, cumsum_hist)
fig = plt.figure(figsize=(12,7))
plt.plot(X, Y, 'k')
plt.xlabel("Energy ({})".format(grid.units), fontsize=18)
plt.ylabel("Cumulative number of lines per bin".format(SPECTYPE), fontsize=18)

# normal hist
X, Y = ag.getplotvalues(bin_edges, hist)
fig = plt.figure(figsize=(12,7))
plt.plot(X, Y, 'k')
plt.xlabel("Energy ({})".format(grid.units), fontsize=18)
plt.ylabel("Number of lines per bin".format(SPECTYPE), fontsize=18)

plt.show()