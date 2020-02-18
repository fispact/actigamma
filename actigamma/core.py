import numpy as np

from .exceptions import UnphysicalValueException, \
    UnknownOrUnstableNuclideException, \
    NoDataException
from .database import ReadOnlyDatabase
from .decorators import asarray
from .inventory import UnstablesInventory

linspace = np.linspace
logspace = np.logspace

class EnergyGrid(object):
    """
        Basically a numpy array with some units
        and some protection on negative values
    """

    __slots__ = [ 'bounds' ]

    def __init__(self, bounds=linspace(0.0, 10e6, 10000)):
        """
            Energies in eV

            TODO: use a library to handle units
        """

        if np.any(bounds < 0):
            raise UnphysicalValueException("Energies cannot be negative.")

        self.bounds = bounds

    def __len__(self):
        return len(self.bounds)

    def __getitem__(self, i: int):
        return self.bounds[i]

    def __str__(self):
        return str(self.bounds)

    @property
    def nrofbins(self):
        return len(self)-1

    @property
    def units(self):
        """
            TODO: support other units
        """
        return "eV"

    @property
    @asarray
    def midpoints(self):
        """
            In eV
        """
        return [ (lower + self.bounds[i+1])*0.5 for i, lower in enumerate(self.bounds[:-1])]

    @property
    def minEnergy(self):
        """
            In eV
        """
        return np.min(self.bounds)

    @property
    def maxEnergy(self):
        """
            In eV
        """
        return np.max(self.bounds)

class LineComputor(object):
    """
        Needs testing!
    """

    __slots__ = [ 'db', 'grid', 'lines', 'values', 'linetype' ]

    def __init__(self, db: ReadOnlyDatabase, grid: EnergyGrid, type: str="gamma"):
        self.db = db

        self.grid = grid

        # here we just store lines and intensities
        # we loose knowledge of original nuclide
        # maybe later we will need this
        # TODO: better datastructure - ordereddict might be better
        self.lines = []

        # NOTE: values are intensities multiplied by the activity of each nuclide here
        self.values = []

        self.linetype = type

    def __call__(self, inventory: UnstablesInventory, *args, **kwargs):
        """
            Gets the lines from the full inventory

            throws an exception if nuclide is stable or is not in database
        """
        for zai, activity in inventory:
            name = self.db.getname(zai)
            # check it exists in database
            if name not in self.db:
                raise UnknownOrUnstableNuclideException(
                    "{} not in database - maybe too exotic or is it stable?".format(zai))

            # check that data exists for that decay type
            if self.linetype not in self.db.gettypes(name):
                raise NoDataException(
                    "{} does not have {} decay mode".format(name, self.linetype))

            self.lines.extend(self.db.getenergies(name, type=self.linetype))
            self.values.extend(self.db.getintensities(name, type=self.linetype)*activity)

        hist = [0.0]*self.grid.nrofbins

        if len(self.lines) > 0:
            # sort the lines in ascending energy to make it easier to bin in a histogram
            sorteddata = sorted(zip(self.lines, self.values), key=lambda pair: pair[0])
            self.lines = [x for x, _ in sorteddata]
            self.values = [y for _, y in sorteddata]

            # loop over lines to find appropriate bin
            ibin = 0
            for i, line in enumerate(self.lines):
                # loop over bounds from the last found bin
                for j in range(ibin, len(self.grid)-1):
                    lowerEnergy = self.grid[j]
                    upperEnergy = self.grid[j+1]
                    if line >= lowerEnergy and line < upperEnergy:
                        hist[j] += self.values[i]
                        ibin = j


        # should be density=False since we can have multiple lines per decay - cannot get numpy histogram to work
        # with the data correctly
        # return np.histogram(self.lines, bins=self.grid.bounds, weights=self.values, density=False)
        return hist, self.grid.bounds