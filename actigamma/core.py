import numpy as np

from .exceptions import UnphysicalValueException

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

    def __getitem__(self, i):
        return self.bounds[i]

    def __str__(self):
        return str(self.bounds)

    @property
    def units(self):
        """
            TODO: support other units
        """
        return "eV"

    @property
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