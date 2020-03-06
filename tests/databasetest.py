import unittest
import actigamma as ag


# Mock the database using a dummy loader
class MockLoader(object):

    def __enter__(self):
        """
            Some dummy data
        """
        return {
            'H3':{'beta': {'lines': {'energies': [18571.0, 45213.2],
                    'energies_unc': [6.0, 5.0],
                    'intensities': [1.0, 0.8],
                    'intensities_unc': [0.0, 0.0],
                    'norms': [1.0, 1.0],
                    'norms_unc': [0.0, 0.0]},
                    'mean_energy': 5707.4,
                    'mean_energy_unc': 1.84397,
                    'mean_normalisation': 1.0,
                    'mean_normalisation_unc': 0.0,
                    'number': 2},
                'gamma': {'lines': {'energies': [3571.0],
                    'energies_unc': [2.0],
                    'intensities': [1.0],
                    'intensities_unc': [0.0],
                    'norms': [1.0],
                    'norms_unc': [0.0]},
                    'mean_energy': 307.4,
                    'mean_energy_unc': 1.84397,
                    'mean_normalisation': 1.0,
                    'mean_normalisation_unc': 0.0,
                    'number': 1},
                'SF': {},
            'halflife': 389105000.0,
            'zai': 10030
            },
            'Li8':{
                'alpha': {'lines': {'energies': [1566000.0],
                            'energies_unc': [30000.0],
                            'intensities': [1.0],
                            'intensities_unc': [0.0],
                            'norms': [1.0],
                            'norms_unc': [0.0001]},
                'mean_energy': 3125250.0,
                'mean_energy_unc': 30000.4,
                'mean_normalisation': 1.0,
                'mean_normalisation_unc': 0.0001,
                'number': 1},
                'beta': {'lines': {'energies': [28571.0],
                                    'energies_unc': [30000.0],
                                    'intensities': [1.0],
                                    'intensities_unc': [0.0],
                                    'norms': [1.0],
                                    'norms_unc': [0.0001]},
                        'mean_energy': 6204620.0,
                        'mean_energy_unc': 14446.8,
                        'mean_normalisation': 1.0,
                        'mean_normalisation_unc': 0.0001,
                        'number': 1},
                'halflife': 0.838,
                'zai': 30080}
        } 

    def __exit__(self, *args):
        """
            Does nothing
        """
        pass


class DatabaseInventoryUnitTest(unittest.TestCase):

    def setUp(self):
        self.db = ag.DefaultDatabase(datasource=MockLoader())

    def test_nuclides(self):
        self.assertEqual(['H3', 'Li8'], sorted(self.db.allnuclides), "Assert all nuclides")
        self.assertEqual(['H3'], self.db.allnuclidesoftype(spectype='gamma'), "Assert all nuclides of gamma type")
        self.assertEqual(['Li8'], self.db.allnuclidesoftype(spectype='alpha'), "Assert all nuclides of alpha type")
        self.assertEqual(['H3', 'Li8'], sorted(self.db.allnuclidesoftype(spectype='beta')), "Assert all nuclides of beta type")
        self.assertEqual(True, 'H3' in self.db, "Assert H3 in database")
        self.assertEqual(True, 'Li8' in self.db, "Assert Li8 in database")
        self.assertEqual(False, 'h3' in self.db, "Assert h3 not in database")
        self.assertEqual(False, 'h 3' in self.db, "Assert h 3 not in database")
        self.assertEqual(False, 'U235' in self.db, "Assert U235 not in database")

    def test_types(self):
        self.assertEqual(sorted(['gamma', 'alpha', 'beta', 'SF']), self.db.alltypes, "Assert all types")
        self.assertEqual(sorted(['gamma', 'beta', 'SF']), self.db.gettypes('H3'), "Assert all types")

    def test_zai(self):
        self.assertEqual(10030, self.db.getzai('H3'), "Assert ZAI H3")
        self.assertEqual(30080, self.db.getzai('Li8'), "Assert ZAI Li8")

    def test_name(self):
        self.assertEqual('H3', self.db.getname(10030), "Assert name H3")
        self.assertEqual('Li8', self.db.getname(30080), "Assert name Li8")

    def test_halflife(self):
        self.assertEqual(389105000.0, self.db.gethalflife('H3'), "Assert halflife H3")
        self.assertEqual(0.838, self.db.gethalflife('Li8'), "Assert halflife Li8")

    def test_linedata(self):
        self.assertEqual([3571.0], self.db.getenergies('H3').tolist(), "Assert gamma energies H3")
        self.assertEqual([1.0], self.db.getintensities('H3').tolist(), "Assert gamma intensities H3")
        self.assertEqual([18571.0, 45213.2], self.db.getenergies('H3', spectype='beta').tolist(), "Assert beta energies H3")
        self.assertEqual([1.0, 0.8], self.db.getintensities('H3', spectype='beta').tolist(), "Assert beta intensities H3")
        self.assertEqual([28571], self.db.getenergies('Li8', spectype='beta').tolist(), "Assert beta energies Li8")
        self.assertEqual([1.0], self.db.getintensities('Li8', spectype='beta').tolist(), "Assert beta intensities Li8")

    def test_sortedlines(self):
        alphas = ag.sortedlines(self.db, spectype="alpha")
        betas = ag.sortedlines(self.db, spectype="beta")
        gammas = ag.sortedlines(self.db, spectype="gamma")
        nonsense = ag.sortedlines(self.db, spectype="dsad")

        self.assertEqual(alphas, [("Li8", 1566000.0)], "Assert sorted alphas")
        self.assertEqual(betas, [("H3", 18571.0), ("Li8", 28571.0), ("H3", 45213.2)], "Assert sorted betas")
        self.assertEqual(gammas, [("H3", 3571.0)], "Assert sorted gammas")
        self.assertEqual(nonsense, [], "Assert sorted nonsense")