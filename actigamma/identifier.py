"""
    A module for trying to identify nuclides
    from binned lines
"""
import numpy as np


from .database import ReadOnlyDatabase, sortedlines
from .core import EnergyGrid


class BinWiseNuclideIdentifier():
    """
        A very simple nuclide identifier.

        It loops over bins (1d-array like) with a
        corresponding energy grid to see what nuclides
        can be found in that range.

        TODO: Support a tolerance to energies in order
        to cater for uncertainty in measurement of energy.

        Parameters
        ----------
        db: The spectral database

        Attributes
        ----------
        grid: The energy grid
        nuclides: A list containing the nuclides identified in 
        the spectrum per bin

    """
    def __init__(self, db: ReadOnlyDatabase):
        self.db = db
        self.nuclides = []

    def __call__(self, values: np.ndarray, grid: EnergyGrid, *args,
                 excludes: list = None, spectype: str = "gamma", 
                 progress: bool = True, **kwargs):
        """
            Finds the nuclides in the histogram.

            Only supports single spectrum type.

            TODO: Support multi type spectrum i.e. "gamma" + "x-ray"

            Parameters
            ----------
            excludes: ignore a list of nuclides, that we know should not 
            be in the spectrum
        """
        self.nuclides = []

        # make sure that data is matching
        assert len(values) == grid.nrofbins

        if excludes is None or type(excludes) != list:
            excludes = []

        iterable = lambda x: x
        if progress:
            try:
                from tqdm import tqdm
                iterable = lambda x: tqdm(x)
            except:
                print("Progress not possible without tqdm.")

        # get all lines of that type from the database and sort them in ascending energy
        sorteddata = sortedlines(self.db, spectype=spectype, byenergy=True)

        lastindex = 0
        # get lower and upper energy bounds
        # loop through hist
        for ihist, (lb, ub) in iterable(enumerate(zip(grid.bounds[:-1], grid.bounds[1:]))):

            # the potential nuclides in the current bin
            nucs = []

            # only if the value is non zero
            if values[ihist] > 0:
                # loop over database lines
                for iline, (nuc, energy) in enumerate(sorteddata[lastindex:]):

                    # if line energy is greater than hist bound - skip to next bin
                    if energy > ub:
                        break

                    lastindex = iline
                    # found a nuclide
                    if (energy >= lb) and (energy < ub) and (nuc not in excludes):
                        nucs.append((nuc, energy))

            self.nuclides.append(nucs)

        return self.nuclides
