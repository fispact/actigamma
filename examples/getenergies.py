import actigamma as ag


db = ag.ReadOnlyDatabase(ag.DatabaseJSONFileLoader())
print(db.getenergies("Co60"))
print(db.getintensities("Co60"))
