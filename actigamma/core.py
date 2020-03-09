"""
    The module that includes all core calculation

    Includes binning lines into histograms.
"""
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


class EnergyGrid:
    """
        This represents a simple energy grid to define
        the bins for the gamma spec.

        It is basically a numpy array with some units
        and some protection on negative values.
    """

    __slots__ = ['bounds']

    def __init__(self, bounds: np.ndarray = linspace(0.0, 10e6, 10000)):
        """
            Energies in eV

            TODO: use a library to handle units

            :param bounds: a numpy array defining the binning
        """

        if np.any(bounds < 0):
            raise UnphysicalValueException("Energies cannot be negative.")

        self.bounds = bounds

    def __len__(self) -> int:
        """
            The number of energy bounds

            :return: the number of energy bounds in the grid
        """
        return len(self.bounds)

    def __getitem__(self, i: int) -> float:
        """
            Get the i'th item in the data (energy bounds)

            Does no bound checking on index

            :param i: the index in the grid to access
            :returns: the value at the given index
        """
        return self.bounds[i]

    def __str__(self) -> str:
        """
            A string representation of the energy bounds

            :returns: a string representing the energy bounds
        """
        return str(self.bounds)

    @property
    def nrofbins(self) -> int:
        """
            The number of energy bins, equal to the
            number of energy bounds - 1

            :returns: the number of bins
        """
        return len(self) - 1

    @property
    def units(self) -> str:
        """
            Return the unit type as a string
            TODO: support other units

            :returns: a string representing the units of energy
        """
        return "eV"

    @property
    @asarray
    def midpoints(self) -> np.array:
        """
            Return a numpy array of the midpoint values, in eV

            :returns: a numpy array of the midpoint values in eV
        """
        return (self.bounds[:-1] + self.bounds[1:]) / 2

    @property
    def minEnergy(self) -> float:
        """
            Return the minimum energy, in eV, of the energy grid

            :returns: the minimum energy, in eV, of the energy grid
        """
        return np.min(self.bounds)

    @property
    def maxEnergy(self) -> float:
        """
            Return the maximum energy, in eV, of the energy grid

            :returns: the maximum energy, in eV, of the energy grid
        """
        return np.max(self.bounds)


class LineAggregator:
    """
        A simple class for reading lines of a single decay type
        i.e. "gamma" and binning them in appropriate bins
        according to the energy grid definition.
    """

    __slots__ = ['db', 'grid', 'lines', 'values']

    def __init__(self, db: ReadOnlyDatabase, grid: EnergyGrid):
        self.db = db

        self.grid = grid

        # here we just store lines and intensities
        self.lines = []

        # NOTE: values are intensities multiplied by the activity of each
        # nuclide here
        self.values = []

    def _sortlines(self):
        # sort the lines in ascending energy to make it easier to bin in a
        # histogram
        sorteddata = sorted(zip(self.lines, self.values),
                            key=lambda pair: pair[0])
        self.lines = [x for x, _ in sorteddata]
        self.values = [y for _, y in sorteddata]

    def _findlines(
            self,
            inventory: UnstablesInventory,
            *args,
            spectype: str = "gamma",
            **kwargs):
        lines = []
        values = []

        for zai, activity in inventory:
            name = self.db.getname(zai)
            # check it exists in database
            if name not in self.db:
                raise UnknownOrUnstableNuclideException(
                    "{} not in database - maybe too exotic or is it stable?".format(zai))

            # check that data exists for that decay type
            if spectype not in self.db.gettypes(name):
                raise NoDataException(
                    "{} does not have {} decay mode".format(name, spectype))

            lines.extend(self.db.getenergies(name, spectype=spectype))
            values.extend(
                self.db.getintensities(
                    name,
                    spectype=spectype) *
                activity)

        return lines, values

    def _makehist(self, *args, **kwargs):
        hist = np.zeros(self.grid.nrofbins)

        if len(self.lines) > 0:
            # sort the lines in ascending energy to make it easier to bin in a
            # histogram
            self._sortlines()

            # loop over lines to find appropriate bin
            ibin = 0
            for i, line in enumerate(self.lines):
                # loop over bounds from the last found bin
                for j in range(ibin, len(self.grid) - 1):
                    if line >= self.grid[j] and line < self.grid[j + 1]:
                        hist[j] += self.values[i]
                        ibin = j
                        # once we've found the line break the inner loop
                        break

        return hist, self.grid.bounds

    def __call__(
            self,
            inventory: UnstablesInventory,
            *args,
            spectype: str = "gamma",
            **kwargs):
        """
            Gets the lines from the full inventory

            throws an exception if nuclide is stable or is not in database
        """
        self.lines, self.values = self._findlines(
            inventory, *args, spectype=spectype, **kwargs)

        return self._makehist(*args, **kwargs)


class LineAverageEnergyAggregator(LineAggregator):
    """
        Instead of LineAggregator which just bins the intensities
        times the activity, the LineAverageEnergyAggregator first
        scales the result by line_energy/midpoint_bin_energy which
        is what FISPACT-II does and is done so to conserve energy.
        This is important for dose calculations.

        For very fine energy grids (high number of bins) this will
        have little effect and should produce results similar to
        LineAggregator
    """

    def _makehist(self, *args, **kwargs):
        hist = np.zeros(self.grid.nrofbins)

        if len(self.lines) > 0:
            self._sortlines()

            average_energies = self.grid.midpoints

            # loop over lines to find appropriate bin
            ibin = 0
            for i, line in enumerate(self.lines):
                # loop over bounds from the last found bin
                for j in range(ibin, len(self.grid) - 1):
                    if line >= self.grid[j] and line < self.grid[j + 1]:
                        # how to handle zero average energy?
                        # we scale the values by the line energy/average bin energy
                        # in order to conserve energy for dose calculations
                        hist[j] += self.values[i] * line / average_energies[j]
                        ibin = j
                        break

        return hist, self.grid.bounds


class MultiTypeLineAggregator(LineAggregator):
    """
        A simple class for reading lines of multiple decay type
        i.e. ["gamma", "x-ray"] and binning them in appropriate bins
        according to the energy grid definition.

        Same as LineAggregator but supports multiple types
        of spectra - gamma + x-ray +beta for example.
    """

    def __call__(
            self,
            inventory: UnstablesInventory,
            *args,
            types: [str] = [
                "gamma",
                "x-ray"],
            **kwargs):
        """
            Gets the lines from the full inventory

            throws an exception if nuclide is stable or is not in database
        """
        for spectype in types:
            lines, values = self._findlines(
                inventory, *args, spectype=spectype, **kwargs)
            self.lines.extend(lines)
            self.values.extend(values)

        return self._makehist(*args, **kwargs)



def get_zai_props(db: ReadOnlyDatabase, nuc: str) -> (int, int, int):
    # Z, A, I
    """
        Returns the charge (Z), atomic mass number (A) and the isomeric state (I).

        Nuclide must exist in data and must be unstable.

        :param db: The database to access halflife data used in the conversion
        :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
        No spaces and case sensitive!
        :returns: the (Z, A, I) tuple
    """
    zai = db.getzai(nuc)
    return math.floor(zai/10000), math.floor(zai/10) % 1000, zai % 10


def activity_from_atoms(
        db: ReadOnlyDatabase,
        nuclide: str,
        atoms: float) -> float:
    """
        Returns activity (Bq) given a number of atoms (typical in FISPACT-II or alike).

        Nuclide must exist in data and must be unstable.

        :param db: The database to access halflife data used in the conversion
        :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
        No spaces and case sensitive!
        :param atoms: the number of atoms for the given nuclide
        :returns: the activity (Bq) for the given radionuclide
    """
    return LOG_TWO_BASE_E * atoms / db.gethalflife(nuclide)


def atoms_from_activity(
        db: ReadOnlyDatabase,
        nuclide: str,
        activity: float) -> float:
    """
        Returns the number of atoms given an activity (Bq).

        Nuclide must exist in data and must be unstable.

        :param db: The database to access halflife data used in the conversion
        :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
        No spaces and case sensitive!
        :param activity: the activity (Bq) for the given radionuclide
        :returns: the number of atoms for the given radionuclide
    """
    return db.gethalflife(nuclide) * activity / LOG_TWO_BASE_E
