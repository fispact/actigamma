import unittest
import os

from .databasetest import DatabaseInventoryUnitTest
from .inventorytest import UnstablesInventoryUnitTest
from .coretest import EnergyGridUnitTest

def main():
    unittest.TextTestRunner(verbosity=3).run(unittest.TestSuite())

if __name__ == '__main__':
    unittest.main()
