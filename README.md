# actigamma

Converts nuclide activities to gamma spec

##### Example - plotlines.py
Lines from Co60 + U235 + Pu238 at different activities.


![Lines](https://github.com/fispact/actigamma/blob/master/examples/figures/plotlines.png)

```python
import actigamma as ag

# normally gamma but could be something else - "alpha", "SF" if data exists!
SPECTYPE = "gamma"

# setup the DB - currently only decay 2012 exists
db = ag.ReadOnlyDatabase(ag.DatabaseJSONFileLoader())

# define my unstable inventory by activities (Bq)
inv = ag.UnstablesInventory(data=[
    (db.getzai("Co60"), 9.87e13),
    (db.getzai("Pu238"), 4.e3),
    (db.getzai("U235"), 5.4e8)
])

# define an energy grid between 0 and 4 MeV with 10,000 bins
grid = ag.EnergyGrid(bounds=ag.linspace(0.0, 4e6, 1000))

# bin the lines appropriately
lc = ag.LineComputor(db, grid, type=SPECTYPE)
hist, bin_edges = lc(inv)

# plot ...
```