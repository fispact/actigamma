import os
import json


from .decorators import asarray, constant

# hacky but will do, the database is one large JSON file with line data
# we load it into a static data structure which is our database
__RAW_DATABASE_DECAY_2012_FILE__ = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'data', 'lines_decay_2012.min.json')

# potential to add other libraries here

class DatabaseJSONFileLoader(object):
    """
        Context manager to handle JSON datafile
    """

    __slots__ = [ 'filename' ]

    def __init__(self, datafile=__RAW_DATABASE_DECAY_2012_FILE__):
        self.filename = datafile

    def __enter__(self):
        with open(self.filename, 'rt') as fjson:
            return json.loads(fjson.read())

    def __exit__(self, *args):
        pass

# a facade layer to interact with database
class ReadOnlyDatabase(object):
    """
        TODO: handle uncertainties too
    """
    __slots__ = [ '__raw' ]

    def __init__(self, datasource=DatabaseJSONFileLoader()):
        self.__raw = {}
        with datasource as db:
            self.__raw = db

    def __contains__(self, nuclide: str) -> bool:
        return nuclide in self.__raw

    @constant
    def raw(self):
        return self.__raw

    @property
    def alltypes(self) -> [str]:
        types = []
        for _, v in self.__raw.items():
            for key in v.keys():
                if key not in ["zai", "halflife"] and key not in types:
                    types.append(key)
        return types

    def haslines(self, nuclide: str, type: str="gamma") -> bool:
        return 'lines' in self.__raw[nuclide][type]

    @property
    @asarray
    def allnuclides(self) -> [str]:
        return [k for k, _ in self.__raw.items()]

    def allnuclidesoftype(self, type: str="gamma") -> [str]:
        return [k for k, _ in self.__raw.items() if type in self.__raw[k].keys()]

    def gettypes(self, nuclide: str) -> [str]:
        """
            Check if it has that particular decay type
        """
        return [k for k, _ in self.__raw[nuclide].items() if k not in ["zai", "halflife"] ]

    def hastype(self, nuclide: str, type: str="gamma") -> bool:
        """
            Check if it has that particular decay type
        """
        return type in self.__raw[nuclide]

    def getname(self, zai: int) -> str:
        """
            ZAI
        """
        for k, v in self.__raw.items():
            if v['zai'] == zai:
                return k
        return None

    def getzai(self, nuclide: str) ->int:
        """
            ZAI
        """
        return self.__raw[nuclide]['zai']

    def gethalflife(self, nuclide: str):
        """
            Half-life in seconds
        """
        return self.__raw[nuclide]['halflife']

    @asarray
    def getenergies(self, nuclide: str, type: str="gamma"):
        """
            Defaults to gamma lines
        """
        if self.haslines(nuclide, type=type):
            return self.__raw[nuclide][type]['lines']['energies']
        return []

    @asarray
    def getintensities(self, nuclide: str, type: str="gamma"):
        """
            Defaults to gamma lines

            Also multiplies by normalisation constant
        """
        if self.haslines(nuclide, type=type):
            return [ intensity*self.__raw[nuclide][type]['lines']['norms'][i] 
                    for i,intensity in enumerate(self.__raw[nuclide][type]['lines']['intensities'])]
        return []