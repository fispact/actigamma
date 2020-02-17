import numpy as np

class EnergyGrid(object):
    def __init__(self, bounds=np.linspace(0.0, 10e6, 10000)):
        """
            Energies in eV

            TODO: use a library to handle units
        """
        self.bounds = bounds
    
    #TODO: implement