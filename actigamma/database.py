"""
    The database definition and facades.

    Includes a precooked JSON loader for the in built decay 2012 data and
    allows extension for other database types.
"""
import os
import json

from .decorators import asarray, constant, sortresult
from .exceptions import AbstractClassException

# hacky but will do, the database is one large JSON file with line data
# we load it into a static data structure which is our database
__RAW_DATABASE_DECAY_2012_FILE__ = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'data', 'lines_decay_2012.min.json')


class DatabaseJSONFileLoader():
    """
        Context manager to handle JSON datafile loader

        Reads in data as a JSON file into a dictionary

        Expects data in schema as:
        {
            'H3': {
                'halflife': 389105000.0,
                'zai': 10030,
                'beta': {
                    'lines': {
                        'energies': [18571.0],
                        'energies_unc': [6.0],
                        'intensities': [1.0],
                        'intensities_unc': [0.0],
                        'norms': [1.0],
                        'norms_unc': [0.0]
                    },
                    'mean_energy': 5707.4,
                    'mean_energy_unc': 1.84397,
                    'mean_normalisation': 1.0,
                    'mean_normalisation_unc': 0.0,
                    'number': 1
                },
            }
        }

        Keys are nuclide name, and each nuclide has a halflife and a zai.
        Following keys are then decay mode type: 'gamma', 'x-ray', ...
        with spectral data
    """
    __slots__ = ['filename']

    def __init__(self, datafile: str = __RAW_DATABASE_DECAY_2012_FILE__):
        """
            Construct the object given a filename to a raw JSON file

            :param datafile: The filename of the raw JSON file
            containing the spectral data
        """
        self.filename = datafile

    def __enter__(self):
        """
            Opens the file and returns the data as a dictionary
        """
        with open(self.filename, 'rt') as fjson:
            return json.loads(fjson.read())

    def __exit__(self, *args):
        """
            Does nothing
        """


ABSTRACT_STR_ERROR = \
    "ReadOnlyDatabase should not be instantiated - please extend with your own database."


class ReadOnlyDatabase():
    """
        A base level read only database for interacting with data

        This assumes the datasource is a JSON file loader, but as long
        as it is a context manager it can be anything.

        ```
        with datasource as source:
            # do something with source here
            ...
        ```
    """
    __slots__ = ['__raw']

    def __init__(self, datasource=DatabaseJSONFileLoader()):
        """
            Construct the database given a datasource

            ```
            with datasource as source:
                # do something with source here
                ...
            ```

            :param datasource: context manager to load data into database
        """
        self.__raw = {}
        if datasource:
            with datasource as db:
                self.__raw = db

    def __contains__(self, nuclide: str) -> bool:
        """
            Check if nuclide exists in database
            Abstract method - must be extended.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :returns: boolean - true if in database, false otherwise
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    @constant
    def raw(self):
        """
            Get the underlying datastructure - read only.
            Allows users to perform own custom queries, but protected to be read only.
            No setting permitted.

            :returns: a dictionary object representing the underlying data
        """
        return self.__raw

    @property
    def alltypes(self) -> [str]:
        """
            Return all possible unique decay mode types for the whole database
            Abstract method - must be extended.

            :returns: a list of strings representing the list of decay types
            in the database
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    def haslines(self, nuclide: str, spectype: str = "gamma") -> bool:
        """
            Return true if nuclide has spectral information, false otherwise
            Abstract method - must be extended.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: boolean based on if spectral data for type exists
            and has data in database
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    @property
    def allnuclides(self) -> [str]:
        """
            Return all unique nuclides for the whole database.
            Returns data as numpy array.
            Abstract method - must be extended.

            :returns: a list of strings representing the list of unique
            nuclides in the database
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    def allnuclidesoftype(self, spectype: str = "gamma") -> [str]:
        """
            Return all unique nuclides for the whole database matching a specific
            decay type, default is "gamma".
            Returns data as numpy array.
            Abstract method - must be extended.

            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: a list of strings representing the list of
            unique nuclides in the database
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    def gettypes(self, nuclide: str) -> [str]:
        """
            Return all unique spectral types for a given radionuclide in the database.
            Abstract method - must be extended.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :returns: a list of strings representing the list of unique spcetral
            types for that nuclide
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    def hastype(self, nuclide: str, spectype: str = "gamma") -> bool:
        """
            Check if it has that particular decay type
            Abstract method - must be extended.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: boolean - true if in database, false otherwise
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    def getname(self, zai: int) -> str:
        """
            Get the name of a nuclide, given a ZAI.
            ZAI = Z (charge), A (mass number), I (isomeric state)
            Abstract method - must be extended.

            for example.
            ```
                getname(10030) = 'H3'
                getname(922351) = 'U235m'
            ```

            :param zai: the ZAI number (integer) for the nuclide
            :returns: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    def getzai(self, nuclide: str) -> int:
        """
            Get the ZAI of a nuclide, given a nuclide name.
            ZAI = Z (charge), A (mass number), I (isomeric state)
            Abstract method - must be extended.

            for example.
            ```
                getzai('H3') = 10030
                getzai('U235m') = 922351
            ```

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :returns: the ZAI number (integer) for the nuclide
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    def gethalflife(self, nuclide: str) -> float:
        """
            Get the halflife of a given nuclide in seconds
            Abstract method - must be extended.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :returns: the half life in seconds
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    @asarray
    def getenergies(self, nuclide: str, spectype: str = "gamma"):
        """
            Get the line energies of a given nuclide in eV.
            Default spectral type is "gamma"
            Only provides discrete lines.
            If nuclide has no spectral data then returns an empty array.
            Abstract method - must be extended.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: a numpy array of energies (eV) for the given nuclide
            and decay type.
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)

    @asarray
    def getintensities(self, nuclide: str, spectype: str = "gamma"):
        """
            Get the corresponding intensity values for each line energy of a
            given nuclide.
            Default spectral type is "gamma".
            Intensity values will be between 0 and 1.
            Only provides intensities (probabilities) for discrete lines.
            Also multiplies by normalisation constant.
            If nuclide has no spectral data then returns an empty array.
            Abstract method - must be extended.

            This array will be of the same size as getenergies

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: a numpy array of normalised intensities for the given
            nuclide and decay type.
            :raises AbstractClassException: raises an exception if called
        """
        raise AbstractClassException(ABSTRACT_STR_ERROR)


# a facade layer to interact with database
class DefaultDatabase(ReadOnlyDatabase):
    """
        A simple read only database for interacting with data

        This assumes the datasource is a JSON file loader, conforming
        to the correct schema

        ```
        {
            'H3': {
                'halflife': 389105000.0,
                'zai': 10030,
                'beta': {
                    'lines': {
                        'energies': [18571.0],
                        'energies_unc': [6.0],
                        'intensities': [1.0],
                        'intensities_unc': [0.0],
                        'norms': [1.0],
                        'norms_unc': [0.0]
                    },
                    'mean_energy': 5707.4,
                    'mean_energy_unc': 1.84397,
                    'mean_normalisation': 1.0,
                    'mean_normalisation_unc': 0.0,
                    'number': 1
                },
            }
        }
        ```
    """

    IGNORE_KEYS = ["zai", "halflife"]

    def __init__(self, *args, **kwargs):
        """
            Construct the database given a datasource

            ```
            with datasource as source:
                # do something with source here
                ...
            ```

            :param datasource: context manager to load data into database
        """
        ReadOnlyDatabase.__init__(self, *args, **kwargs)

    def __contains__(self, nuclide: str) -> bool:
        """
            Check if nuclide exists in database

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :returns: boolean - true if in database, false otherwise
        """
        return nuclide in self.raw

    @property
    @sortresult
    def alltypes(self) -> [str]:
        """
            Return all possible unique decay mode types for the whole database

            :returns: a list of strings representing the list of decay types
            in the database
        """
        spectypes = []
        for _, v in self.raw.items():
            for key in v.keys():
                if key not in self.IGNORE_KEYS and key not in spectypes:
                    spectypes.append(key)
        return spectypes

    def haslines(self, nuclide: str, spectype: str = "gamma") -> bool:
        """
            Return true if nuclide has spectral information, false otherwise

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: boolean based on if spectral data for type exists and
            has data in database
            :raises KeyError: raises an exception if nuclide and spectype not in database
        """
        return 'lines' in self.raw[nuclide][spectype]

    @property
    def allnuclides(self) -> [str]:
        """
            Return all unique nuclides for the whole database.
            Returns data as numpy array.

            :returns: a list of strings representing the list of unique nuclides
            in the database
        """
        return [k for k, _ in self.raw.items()]

    def allnuclidesoftype(self, spectype: str = "gamma") -> [str]:
        """
            Return all unique nuclides for the whole database matching a specific
            decay type, default is "gamma".
            Returns data as numpy array.

            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: a list of strings representing the list of unique nuclides
            in the database
            :raises KeyError: raises an exception if spectype not in database
        """
        return [k for k, _ in self.raw.items() if spectype in self.raw[k].keys()]

    @sortresult
    def gettypes(self, nuclide: str) -> [str]:
        """
            Return all unique spectral types for a given radionuclide in the database.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :returns: a list of strings representing the list of unique spcetral
            types for that nuclide
            :raises KeyError: raises an exception if nuclide not in database
        """
        return sorted([k for k, _ in self.raw[nuclide].items()
            if k not in self.IGNORE_KEYS])

    def hastype(self, nuclide: str, spectype: str = "gamma") -> bool:
        """
            Check if it has that particular decay type
            Abstract method - must be extended.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: boolean - true if in database, false otherwise
            :raises KeyError: raises an exception if nuclide not in database
        """
        return spectype in self.raw[nuclide]

    def getname(self, zai: int) -> str:
        """
            Get the name of a nuclide, given a ZAI.
            ZAI = Z (charge), A (mass number), I (isomeric state)

            for example.
            ```
                getname(10030) = 'H3'
                getname(922351) = 'U235m'
            ```

            :param zai: the ZAI number (integer) for the nuclide
            :returns: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
        """
        for k, v in self.raw.items():
            if v['zai'] == zai:
                return k
        return None

    def getzai(self, nuclide: str) -> int:
        """
            Get the ZAI of a nuclide, given a nuclide name.
            ZAI = Z (charge), A (mass number), I (isomeric state)
            Abstract method - must be extended.

            for example.
            ```
                getzai('H3') = 10030
                getzai('U235m') = 922351
            ```

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :returns: the ZAI number (integer) for the nuclide
            :raises KeyError: raises an exception if nuclide key not in database
        """
        return self.raw[nuclide]['zai']

    def gethalflife(self, nuclide: str) -> float:
        """
            Get the halflife of a given nuclide in seconds
            Abstract method - must be extended.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :returns: the half life in seconds
            :raises KeyError: raises an exception if nuclide key not in database
        """
        return self.raw[nuclide]['halflife']

    @asarray
    def getenergies(self, nuclide: str, spectype: str = "gamma"):
        """
            Get the line energies of a given nuclide in eV.
            Default spectral type is "gamma"
            Only provides discrete lines.

            If nuclide has no spectral data then returns an empty array.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: a numpy array of energies (eV) for the given nuclide
            and decay type.
            :raises KeyError: raises an exception if nuclide and spectype not
            in database
        """
        if self.haslines(nuclide, spectype=spectype):
            return self.raw[nuclide][spectype]['lines']['energies']
        return []

    @asarray
    def getenergiesunc(self, nuclide: str, spectype: str = "gamma"):
        """
            Get the line energies uncertainties of a given nuclide in eV.
            Default spectral type is "gamma"
            Only provides discrete lines.

            If nuclide has no spectral data then returns an empty array.

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: a numpy array of energies (eV) for the given nuclide
            and decay type.
            :raises KeyError: raises an exception if nuclide and spectype not
            in database
        """
        if self.haslines(nuclide, spectype=spectype):
            return self.raw[nuclide][spectype]['lines']['energies_unc']
        return []

    @asarray
    def getintensities(self, nuclide: str, spectype: str = "gamma"):
        """
            Get the corresponding intensity values for each line energy of a
            given nuclide.
            Default spectral type is "gamma".
            Intensity values will be between 0 and 1.
            Only provides intensities (probabilities) for discrete lines.
            Also multiplies by normalisation constant.

            If nuclide has no spectral data then returns an empty array.

            This array will be of the same size as getenergies

            :param nuclide: the radionuclide as a string i.e 'H3' or 'U235m'.
            No spaces and case sensitive!
            :param spectype: a string representing the type of decay mode.
            Gamma is default.
            :returns: a numpy array of normalised intensities for the given
            nuclide and decay type.
            :raises KeyError: raises an exception if nuclide and spectype
            not in database
        """
        if self.haslines(nuclide, spectype=spectype):
            return [
                intensity *
                self.raw[nuclide][spectype]['lines']['norms'][i] for i,
                intensity in enumerate(
                    self.raw[nuclide][spectype]['lines']['intensities'])]
        return []


# some aliases for decay data
def Decay2012Database():
    """
        Alias/factory for decay 2012 data
    """
    return DefaultDatabase(
        datasource=DatabaseJSONFileLoader(
            datafile=__RAW_DATABASE_DECAY_2012_FILE__))


def sortedlines(db: ReadOnlyDatabase, spectype: str = "gamma", 
                byenergy: bool = True) -> [(str, float)]:
    """
        Get a sorted list (by increasing line energy) of nuclides 
        with energies.

        :param db: the database holding line energies
        :param spectype: a string representing the type of decay mode.
        Gamma is default.
        :param byenergy: by default always sort by energy, otherwise sort
        alphabetically on nuclide name.
        :returns: a list of str,float pairs with the first representing the
        nuclide name, and the second representing the energy of the line

        ```
            db = ag.Decay2012Database()
            gammalines = sortedlines(db, spectype="gamma")

            # gammalines
            >>> [('U235m', 76.8), ('Es254', 1100.0), ('Ag110m', 1160.0), 
                ('Tl201', 1580.0), ('Pt193m', 1642.0), ...]
        ```
    """

    # get all nuclides of type spectype
    allnuclides = db.allnuclidesoftype(spectype=spectype)

    # all lines 
    alllines = []
    for nuc in allnuclides:
        lines = db.getenergies(nuc, spectype=spectype)
        nuclides = [nuc]*len(lines)
        alllines.extend(zip(nuclides, lines))

    # sort by energy
    key = (1 if byenergy else 0)
    return sorted(alllines, key=lambda x: x[key])
