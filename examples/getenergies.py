import actigamma as ag


db = ag.Decay2012Database()

NUCLIDE = "U235"
print(db.getenergies(NUCLIDE, spectype="gamma"))
print(db.getintensities(NUCLIDE, spectype="gamma"))

# can also do
# fulldata = db._raw[NUCLIDE]