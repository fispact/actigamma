import os
import json


from .decorators import asarray

# hacky but will do, the database is one large JSON file with line data
# we load it into a static data structure which is our database
__RAW_DATABASE_DECAY_2012_FILE__ = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'data', 'lines_decay_2012.min.json')

# potential to add other libraries here

class DatabaseJSONFileLoader(object):
    """
        Context manager to handle JSON datafile
    """
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
    def __init__(self, datasource):
        self._raw = {}
        with datasource as db:
            self._raw = db

    def __contains__(self, nuclide: str) -> bool:
        return nuclide in self._raw

    @property
    @asarray
    def allnuclides(self) -> [str]:
        return [k for k, _ in self._raw.items()]

    def allnuclidesoftype(self, type: str="gamma") -> [str]:
        return [k for k, _ in self._raw.items() if type in self._raw[k].keys()]

    def gettypes(self, nuclide: str) -> [str]:
        """
            Check if it has that particular decay type
        """
        return [k for k, _ in self._raw[nuclide].items() if k not in ["zai", "halflife"] ]

    def hastype(self, nuclide: str, type: str="gamma") -> bool:
        """
            Check if it has that particular decay type
        """
        return type in self._raw[nuclide]

    def getname(self, zai: int) -> str:
        """
            ZAI
        """
        for k, v in self._raw.items():
            if v['zai'] == zai:
                return k
        return None

    def getzai(self, nuclide: str) ->int:
        """
            ZAI
        """
        return self._raw[nuclide]['zai']

    def gethalflife(self, nuclide: str):
        """
            Half-life in seconds
        """
        return self._raw[nuclide]['halflife']

    @asarray
    def getenergies(self, nuclide: str, type: str="gamma"):
        """
            Defaults to gamma lines
        """
        return self._raw[nuclide][type]['lines']['energies']

    @asarray
    def getintensities(self, nuclide: str, type: str="gamma"):
        """
            Defaults to gamma lines

            Also multiplies by normalisation constant
        """
        return [ intensity*self._raw[nuclide][type]['lines']['norms'][i] 
                for i,intensity in enumerate(self._raw[nuclide][type]['lines']['intensities'])]