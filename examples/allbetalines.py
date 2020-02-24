import numpy as np
import matplotlib.pyplot as plt
import actigamma as ag

# normally gamma but could be something else - "alpha", "SF" if data exists!
SPECTYPE = "beta"

# setup the DB
db = ag.Decay2012Database()

# define an energy grid between 0 and 4 MeV with 10,000 bins
grid = ag.EnergyGrid(bounds=ag.linspace(0.0, 4e6, 10000))

# bin the lines appropriately
lc = ag.LineAggregator(db, grid)

hist = np.zeros(grid.nrofbins)
bin_edges = grid.bounds
for betanuclide in db.allnuclidesoftype(spectype=SPECTYPE):
    inv = ag.UnstablesInventory(data=[(db.getzai(betanuclide), 1e10)])
    h, _ = lc(inv, spectype=SPECTYPE)
    hist += h

# make a plot
X, Y = ag.getplotvalues(bin_edges, hist)
fig = plt.figure(figsize=(12,7))
plt.plot(X, Y, 'k')
plt.xlabel("Energy ({})".format(grid.units), fontsize=18)
plt.ylabel("{} per unit time (s-1)".format(SPECTYPE), fontsize=18)
plt.yscale('log')
plt.show()