import actigamma as ag


db = ag.ReadOnlyDatabase(ag.DatabaseJSONFileLoader())

NUCLIDE = "U235"
print(db.getenergies(NUCLIDE, type="gamma"))
print(db.getintensities(NUCLIDE, type="gamma"))

# can also do
# fulldata = db._raw[NUCLIDE]