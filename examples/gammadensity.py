import matplotlib.pyplot as plt
import numpy as np

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

# setup the DB
db = ag.Decay2012Database()

grid = ag.EnergyGrid(bounds=ag.linspace(0.0, 4e6, 1000))

# bin the lines appropriately
lc = BinaryLineAggregator(db, grid)

hist = np.zeros(grid.nrofbins)
bin_edges = grid.bounds
for nuclide in db.allnuclidesoftype(spectype=SPECTYPE):
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

# plt.yscale('log')
plt.show()