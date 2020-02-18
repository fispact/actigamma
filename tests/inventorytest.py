import unittest
import actigamma as ag


class UnstablesInventoryUnitTest(unittest.TestCase):

    def test_initvaliddefault(self):
        inv = ag.UnstablesInventory()
        self.assertEqual([], inv.zais, "Assert default zais")
        self.assertEqual([], inv.activities, "Assert default activity")

    def test_initvalid(self):
        inv = ag.UnstablesInventory(data=[(10030, 38.321e4), (9202350, 3.2e17)])
        self.assertEqual([10030, 9202350], inv.zais, "Assert zais")
        self.assertEqual([38.321e4, 3.2e17], inv.activities, "Assert activity")

    def test_initinvalid(self):
        with self.assertRaises(TypeError):
            ag.UnstablesInventory(data=[(10010, 1e20), (30040, 3.2e17), 8.9])
        with self.assertRaises(TypeError):
            ag.UnstablesInventory(data=[0.2, 3.5])
        with self.assertRaises(ValueError):
            ag.UnstablesInventory(data=([10010, 30040, 500461], [1e20, 3.2e17, 2.43e18]))

    def test_append(self):
        inv = ag.UnstablesInventory(data=[(10010, 1e20)])
        self.assertEqual([10010], inv.zais, "Assert zais")
        self.assertEqual([1e20], inv.activities, "Assert activity")
        self.assertEqual(1, len(inv), "Assert length")

        inv.append(260561, 3.5e19)
        inv.append(260570, 1.4e19)
        self.assertEqual([10010, 260561, 260570], inv.zais, "Assert zais")
        self.assertEqual([1e20, 3.5e19, 1.4e19], inv.activities, "Assert activity")
        self.assertEqual(3, len(inv), "Assert length")

    def test_appendsamezai(self):
        inv = ag.UnstablesInventory(data=[(10010, 1e20)])
        self.assertEqual([10010], inv.zais, "Assert zais")
        self.assertEqual([1e20], inv.activities, "Assert activities")
        self.assertEqual(1, len(inv), "Assert length")

        inv.append(260561, 3.5e19)
        inv.append(260570, 1.4e19)
        self.assertEqual([10010, 260561, 260570], inv.zais, "Assert zais")
        self.assertEqual([1e20, 3.5e19, 1.4e19], inv.activities, "Assert activities")
        self.assertEqual(3, len(inv), "Assert length")

        # append the same zai - length should not increase
        inv.append(10010, 3.5e19)
        inv.append(260570, 2.4e19)
        self.assertEqual([10010, 260561, 260570], inv.zais, "Assert zais")
        self.assertEqual([1.35e20, 3.5e19, 3.8e19], inv.activities, "Assert activities")
        self.assertEqual(3, len(inv), "Assert length")

    def test_findatoms(self):
        inv = ag.UnstablesInventory(data=[(10010, 1e20), (260571, 3e18), (30040, 1.56e17), (10010, 2e20)])
        self.assertEqual(3e20, inv.findactivitybyzai(10010), "Assert activity for zai 10010")
        self.assertEqual(0.0, inv.findactivitybyzai(-1), "Assert activity for zai invalid zai")
        self.assertEqual(1.56e17, inv.findactivitybyzai(30040), "Assert activity for zai 30040")
        self.assertEqual(3e18, inv.findactivitybyzai(260571), "Assert activity for zai 260571")
        self.assertEqual(0.0, inv.findactivitybyzai(260570), "Assert activity for zai 260570")
        self.assertEqual(3e18, inv.findactivitybyzai(260571), "Assert activity for zai 260571")
        self.assertEqual(3e20, inv.findactivitybyzai(10010), "Assert activity for zai 10010")

    def test_avoiddirectaccess(self):
        inv = ag.UnstablesInventory(data=[(10010, 1e20)])
        
        with self.assertRaises(AttributeError):
            inv.zais = []
        with self.assertRaises(AttributeError):
            inv.activities = []
            
        self.assertEqual([10010], inv.zais, "Assert zais")
        self.assertEqual([1e20], inv.activities, "Assert activities")