import math
import numpy as np

from .exceptions import UnphysicalValueException, \
    UnknownOrUnstableNuclideException, \
    NoDataException
from .database import ReadOnlyDatabase
from .decorators import asarray
from .inventory import UnstablesInventory

LOG_TWO_BASE_E = math.log(2)

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

class LineAggregator(object):
    """
        Needs testing!
    """

    __slots__ = [ 'db', 'grid', 'lines', 'values' ]

    def __init__(self, db: ReadOnlyDatabase, grid: EnergyGrid):
        self.db = db

        self.grid = grid

        # here we just store lines and intensities
        self.lines = []

        # NOTE: values are intensities multiplied by the activity of each nuclide here
        self.values = []

    def _findlines(self, inventory: UnstablesInventory, *args, type: str="gamma", **kwargs):
        lines = []
        values = []

        for zai, activity in inventory:
            name = self.db.getname(zai)
            # check it exists in database
            if name not in self.db:
                raise UnknownOrUnstableNuclideException(
                    "{} not in database - maybe too exotic or is it stable?".format(zai))

            # check that data exists for that decay type
            if type not in self.db.gettypes(name):
                raise NoDataException(
                    "{} does not have {} decay mode".format(name, type))

            lines.extend(self.db.getenergies(name, type=type))
            values.extend(self.db.getintensities(name, type=type)*activity)

        return lines, values

    def _makehist(self, *args, **kwargs):
        hist = np.zeros(self.grid.nrofbins)

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
                    if line >= self.grid[j] and line < self.grid[j+1]:
                        hist[j] += self.values[i]
                        ibin = j

        return hist, self.grid.bounds

    def __call__(self, inventory: UnstablesInventory, *args, type: str="gamma", **kwargs):
        """
            Gets the lines from the full inventory

            throws an exception if nuclide is stable or is not in database
        """
        self.lines, self.values = self._findlines(inventory, *args, type, **kwargs)
        
        return self._makehist(*args, **kwargs)

class MultiTypeLineAggregator(LineAggregator):
    """
        Supports multiple types of spectra - gamma + x-ray +beta for example
        Needs testing!
    """
    def __call__(self, inventory: UnstablesInventory, *args, types: [str]=["gamma", "x-ray"], **kwargs):
        """
            Gets the lines from the full inventory

            throws an exception if nuclide is stable or is not in database
        """
        for type in types:
            lines, values = self._findlines(inventory, *args, type=type, **kwargs)
            self.lines.extend(lines)
            self.values.extend(values)

        return self._makehist(*args, **kwargs)

def activity_from_atoms(db: ReadOnlyDatabase, nuclide: str, atoms: float) -> float:
    """
        Returns activity (Bq) given a number of atoms (typical in FISPACT-II or alike)

        Nuclide must exist in data and must be unstable
    """
    return LOG_TWO_BASE_E*atoms/db.gethalflife(nuclide)

def atoms_from_activity(db: ReadOnlyDatabase, nuclide: str, activity: float) -> float:
    """
        Returns the number of atoms given an activity (Bq)

        Nuclide must exist in data and must be unstable
    """
    return db.gethalflife(nuclide)*activity/LOG_TWO_BASE_E