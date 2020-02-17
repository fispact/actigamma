import os
import json


# hacky but will do, the database is one large JSON file with line data
# we load it into a static data structure which is our database
__RAW_DATABASE_DECAY_2012_FILE__ = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'reference', 'lines_decay_2012.json')

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
        self._db = {}
        with datasource as db:
            self._db = db

    def getenergies(self, nuclide, type="gamma"):
        """
            Defaults to gamma lines
        """
        return self._db[nuclide][type]['lines']["energies"]

    def getintensities(self, nuclide, type="gamma"):
        """
            Defaults to gamma lines

            Also multiplies by normalisation constant
        """
        return[ intensity*self._db[nuclide][type]['lines']["norms"][i] 
                for i,intensity in enumerate(self._db[nuclide][type]['lines']["intensities"])]