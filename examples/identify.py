"""
    A rough example of using a brute force
    (search through all database for possible 
    nuclides) approach to try and match spectral 
    histogram with database.

    Uses the simple BinWiseNuclideIdentifer.
"""

import collections

import actigamma as ag


SPECTYPE = "gamma"

# database handle
db = ag.Decay2012Database()

# make a histogram from a dummy inventory
inv = ag.UnstablesInventory(data=[
    (db.getzai("Bi213"), 9.87e13),
    (db.getzai("Pm151"), 1.1e3),
])

# a dummy energy grid - must be fine to get anything reliable out
grid = ag.EnergyGrid(bounds=ag.linspace(0.0, 6e6, 10000))
lc = ag.LineAggregator(db, grid)
hist, _ = lc(inv, spectype=SPECTYPE)

# use the simple bin wise (brute force) identifier to 
# get everything possible from the hist
ider = ag.BinWiseNuclideIdentifier(db)
id_nucs = ider(hist, grid, spectype=SPECTYPE, excludes=[])

# make one big list of all entries to count nuclide
# occurrences
nrofnonzerobins = 0
fulllist = []
for nuc in id_nucs:
    if nuc:
        names, _ = zip(*nuc)
        nrofnonzerobins += 1
        fulllist.extend(names)

# very primitive method
# only show nuclides which match up exactly
# with lines in the grid energy range
counts = collections.Counter(fulllist)
countssorted = collections.OrderedDict(counts.most_common())
for k, v in countssorted.items():
    # get the number of total lines in the range
    # specified to provide a useful metric
    lines = list(sorted(db.getenergies(k, spectype=SPECTYPE)))
    nrlinesinenergy = 0
    for line in lines:
        if line >= grid.minEnergy and line <= grid.maxEnergy:
            nrlinesinenergy += 1

    # only show nuclides which have complete accounting
    if nrlinesinenergy == v:
        print("{:<20}={:5}/{:5}".format(k, v, nrlinesinenergy))
