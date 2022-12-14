# ActiGamma
### Trivial gamma spec from activities

[![GitHub Actions](https://github.com/fispact/actigamma/workflows/Python%20package/badge.svg?branch=master)](https://github.com/fispact/actigamma/actions/workflows/python-package.yml)
[![Build Status](https://travis-ci.org/fispact/actigamma.svg?branch=master)](https://travis-ci.org/fispact/actigamma)
[![Code Coverage](https://codecov.io/gh/fispact/actigamma/branch/master/graph/badge.svg)](https://codecov.io/gh/fispact/actigamma)

[![PyPI](https://img.shields.io/pypi/v/actigamma.svg)](https://pypi.python.org/pypi/actigamma)
[![PyPI](https://img.shields.io/pypi/wheel/actigamma.svg)](https://pypi.python.org/pypi/actigamma)
[![PyPI](https://img.shields.io/pypi/format/actigamma.svg)](https://pypi.python.org/pypi/actigamma)
[![License](https://img.shields.io/pypi/l/actigamma.svg)](https://github.com/fispact/actigamma/blob/master/LICENSE)

[![HitCount](http://hits.dwyl.com/fispact/actigamma.svg)](http://hits.dwyl.com/fispact/actigamma)
[![GitHub issues](https://img.shields.io/github/issues/fispact/actigamma)](https://github.com/fispact/actigamma/issues)
[![GitHub stars](https://img.shields.io/github/stars/fispact/actigamma)](https://github.com/fispact/actigamma/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/fispact/actigamma)](https://github.com/fispact/actigamma/network)

![ChartOfNuclides](https://github.com/fispact/actigamma/blob/master/examples/figures/chartofnuclides.png)

![GammaLinesAnimation](https://github.com/fispact/actigamma/blob/master/examples/figures/halflifelines.gif)


__ActiGamma__ - Converts nuclide activities to gamma spec. Nothing more, nothing less.

- [Design goals](#design-goals)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
  - [Single type plot](#single-type-plot)
  - [Multi type plot](#multi-type-plot)

#### <a name="design-goals"></a>Design goals
FISPACT-II can produce the gamma spectrum at each irradiation time interval, but this is largely overkill if you just want the gamma (or x-ray, beta, etc...) lines/spectrum given a set of radionuclides and corresponding activities. If you already have performed your activation and inventory simulation and want a gamma spec, then ActiGamma will do just that.

No dependencies. Doesn't require FISPACT-II. Pip install.

Even the decay data is included in the package in minified JSON format, you don't need to worry about reading it either.

#### <a name="installation"></a>Installation
The package is hosted on PyPi and is therefore available with pip3 directly.

A note on the nature of ActiGamma, it is written in Python3 and does not support Python2, therefore in order to use the package, you must have a version of Python3 installed along with pip3.

To install simply do
```bash
pip3 install actigamma
```

#### <a name="usage"></a>Usage
Simply import the package as below.
```python
import actigamma as ag
```

Load the database (by default uses decay_2012 library but easy to extend to add others).
```python
db = ag.Decay2012Database()

# get halflife of Co60
print(db.gethalflife("Co60"))

# get gamma lines of Co60
print(db.getenergies("Co60", spectype="gamma"))
```

Define an energy grid (binning). This can be anything (linspace, logspace, custom bounds).
```python
# define an energy grid between 1 and 4 MeV with 5,000 bins
grid = ag.EnergyGrid(bounds=ag.linspace(1e6, 4e6, 5000))
```

Define a line aggregator, single-type (LineAggregator) or multi-type (MultiTypeLineAggregator) to combine mulitple nuclides and handle the binning.
```python
# bin the lines appropriately using single type aggregator
lc = ag.LineAggregator(db, grid)
```

Define the inventory via activities (or convert from atoms if need be).
```python
# define my unstable inventory by activities (Bq)
inv = ag.UnstablesInventory(data=[
    (db.getzai("Co60"), 9.87e13),
    (db.getzai("Pu238"), 4.e3),
    (db.getzai("U235"), 5.4e8)
])
```

To create an inventory from a list of atoms (instead of activities) use the following.
```python
inv = ag.UnstablesInventory(data=[
    (db.getzai("Co60"), ag.activity_from_atoms(db, "Co60", 2.36853908671135e+22)),
    (db.getzai("Pu238"), ag.activity_from_atoms(db, "Pu238", 15970864933847.367)),
    (db.getzai("U235"), ag.activity_from_atoms(db, "U235", 1.730297451446211e+25))
])
```

Get the histogram and do what you want with it.
```python
hist, bin_edges = lc(inv, spectype=SPECTYPE)

# plot here
...
```

#### <a name="examples"></a>Examples
##### <a name="single-type-plot"></a>Single type plot
Gamma lines from Co60 + U235 + Pu238 at different activities.

![Lines](https://github.com/fispact/actigamma/blob/master/examples/figures/plotlines.png)

Is produced with the following code
```python
import actigamma as ag

# normally gamma but could be something else - "alpha", "SF" if data exists!
SPECTYPE = "gamma"

# setup the DB - currently only decay 2012 exists
db = ag.Decay2012Database()

# define my unstable inventory by activities (Bq)
inv = ag.UnstablesInventory(data=[
    (db.getzai("Co60"), 9.87e13),
    (db.getzai("Pu238"), 4.e3),
    (db.getzai("U235"), 5.4e8)
])

# define an energy grid between 0 and 4 MeV with 10,000 bins
grid = ag.EnergyGrid(bounds=ag.linspace(0.0, 4e6, 1000))

# bin the lines appropriately
lc = ag.LineAggregator(db, grid)
hist, bin_edges = lc(inv, spectype=SPECTYPE)

# plot ...
```

##### <a name="multi-type-plot"></a>Multi type plot
Gamma + x-ray lines from Co60 + U235 + Pu238 at different activities.

Is produced with the following code
```python
import actigamma as ag

# normally gamma but could be something else - "alpha", "SF" if data exists!
SPECTYPES = [
    "gamma",
    "x-ray"
]

# setup the DB - currently only decay 2012 exists
db = ag.Decay2012Database()

# define my unstable inventory by activities (Bq)
inv = ag.UnstablesInventory(data=[
    (db.getzai("Co60"), 9.87e13),
    (db.getzai("Pu238"), 4.e3),
    (db.getzai("U235"), 5.4e8)
])

# define an energy grid between 0 and 4 MeV with 10,000 bins
grid = ag.EnergyGrid(bounds=ag.linspace(0.0, 4e6, 1000))

# bin the lines appropriately
lc = ag.MultiTypeLineAggregator(db, grid)
hist, bin_edges = lc(inv, spectype=SPECTYPES)

# plot ...
```
