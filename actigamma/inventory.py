"""
    A module for defining inventories of unstable nuclides
"""
import collections

from .exceptions import UnphysicalValueException


class UnstablesInventory():
    """
        A simple data structure to represent inventory data.
        A list of zais and activities (Bq).

        Note that this should only be used for inventories with
        non zero activities i.e. only unstables, since stables have
        no spectrum.

        NOTE: This does not check if ZAI is unstable (TODO: should we do this?).

        An ordered dict is used to preserve the
        order to which items where added.

        Data should be a list of tuples
        with nuclide ZAI and activity
        i.e.
            [(10030, 4.5e8), (20040, 2.2321e4), ...]

        throws UnphysicalValueException if activities are 0 <=
    """

    __slots__ = ['_raw']

    def __init__(self, data=None):
        self._raw = collections.OrderedDict()
        if data:
            for z, a in data:
                if a <= 0:
                    raise UnphysicalValueException(
                        "Only supports unstable nuclides, activity must be positive.")
                self._raw[z] = self._raw.get(z, 0) + a

    def append(self, zai: int, activity: float):
        if isinstance(zai, int) and isinstance(activity, float):
            if activity <= 0:
                raise UnphysicalValueException(
                    "Only supports unstable nuclides, activity must be positive.")
            self._raw[zai] = self._raw.get(zai, 0) + activity
        else:
            raise TypeError("Expects ZAI as integer and activity as float.")

    def reset(self):
        self._raw = collections.OrderedDict()

    def __len__(self):
        return len(self._raw.items())

    def __getitem__(self, index):
        return list(self._raw.items())[index]

    def findactivitybyzai(self, zai):
        """
            Given a ZAI value find the corresponding activity (Bq).
            If zai is not valid or is not in inventory, return 0.0
        """
        return self._raw.get(zai, 0)

    @property
    def zais(self):
        return list(self._raw.keys())

    @property
    def activities(self):
        """
            In Bq
        """
        return list(self._raw.values())
