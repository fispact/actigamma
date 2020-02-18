import matplotlib.pyplot as plt
import actigamma as ag

# normally gamma but could be something else - "alpha", "SF" if data exists!
SPECTYPE = "gamma"

# setup the DB
db = ag.ReadOnlyDatabase(ag.DatabaseJSONFileLoader())

# define my unstable inventory by activities (Bq)
inv = ag.UnstablesInventory(data=[
    (db.getzai("Co60"), 9.87e13),
    (db.getzai("Pu238"), 4.e3),
    (db.getzai("U235"), 5.4e8)
])

# define an energy grid between 0 and 4 MeV with 10,000 bins
grid = ag.EnergyGrid(bounds=ag.linspace(0.0, 4e6, 10000))

# or we can do logspace between 1e3 eV and 1e7 eV with 10,000 bins
# grid = ag.EnergyGrid(bounds=ag.logspace(3, 7, 10000))
# plt.xscale('log')

# bin the lines appropriately
lc = ag.LineComputor(db, grid)
hist, bin_edges = lc(inv, type=SPECTYPE)

# make a plot
X, Y = ag.getplotvalues(bin_edges, hist)
fig = plt.figure(figsize=(12,7))
plt.plot(X, Y, 'k')
plt.xlabel("Energy ({})".format(grid.units), fontsize=18)
plt.ylabel("{} per unit time (s-1)".format(SPECTYPE), fontsize=18)
plt.yscale('log')
plt.show()