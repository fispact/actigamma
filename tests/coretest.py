import unittest
import actigamma as ag


class EnergyGridUnitTest(unittest.TestCase):

    def test_initvaliddefault(self):
        grid = ag.EnergyGrid()
        self.assertEqual(0.0, grid.minEnergy, "Assert default min energy")
        self.assertEqual(10.0e6, grid.maxEnergy, "Assert default max energy")
        self.assertEqual("eV", grid.units, "Assert units")
        self.assertEqual(10000, len(grid), "Assert length")
        self.assertEqual(0.0, grid[0], "Assert first")
        self.assertEqual(10.0e6, grid[-1], "Assert last")
        self.assertEqual(9999, grid.nrofbins, "Assert nrofbins")

    def test_simple(self):
        grid = ag.EnergyGrid(bounds=ag.linspace(1,2,2))
        self.assertEqual(1.0, grid.minEnergy, "Assert default min energy")
        self.assertEqual(2.0, grid.maxEnergy, "Assert default max energy")
        self.assertEqual("eV", grid.units, "Assert units")
        self.assertEqual(2, len(grid), "Assert length")
        self.assertEqual(1.0, grid[0], "Assert first")
        self.assertEqual(2.0, grid[-1], "Assert last")
        self.assertEqual(1, grid.nrofbins, "Assert nrofbins")
        self.assertEqual([1.5], list(grid.midpoints), "Assert mid points")
        self.assertEqual([1.0, 2.0], list(grid.bounds), "Assert bounds")

    def test_simple2(self):
        grid = ag.EnergyGrid(bounds=ag.linspace(1,2,5))
        self.assertEqual(1.0, grid.minEnergy, "Assert default min energy")
        self.assertEqual(2.0, grid.maxEnergy, "Assert default max energy")
        self.assertEqual("eV", grid.units, "Assert units")
        self.assertEqual(5, len(grid), "Assert length")
        self.assertEqual(1.0, grid[0], "Assert first")
        self.assertEqual(2.0, grid[-1], "Assert last")
        self.assertEqual(4, grid.nrofbins, "Assert nrofbins")
        self.assertEqual([1.125, 1.375, 1.625, 1.875], list(grid.midpoints), "Assert mid points")
        self.assertEqual([1.0, 1.25, 1.5, 1.75, 2.0], list(grid.bounds), "Assert bounds")

    # TODO: need to test exceptions!