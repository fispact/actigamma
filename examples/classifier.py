import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

import actigamma as ag


classifier = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, max_features='auto', verbose=False))

# generate a dataset based on 100 bins from 0 to 4 MeV
MINENERGY = 0.0
MAXENERGY = 4e6
NBINS = 1000
SPECTYPE = "gamma"

# setup the DB
db = ag.Decay2012Database()
grid = ag.EnergyGrid(bounds=ag.linspace(MINENERGY, MAXENERGY, NBINS+1))
lc = ag.LineAggregator(db, grid)

NSAMPLES = 1000
NNUCLIDES = 10
# randomly generate 100 samples based on 10 radionuclides
radionuclides = db.allnuclidesoftype(spectype=SPECTYPE)[:NNUCLIDES]

# ignore activity - set to 1
ACTIVITY = 1
datasetX, datasetY = [], []
for _ in range(NSAMPLES):
    # randomly pick between 1 and NNUCLIDIES to generate data
    nrofnuclides = random.randrange(1, NNUCLIDES+1)
    # pick nrofnuclides - must be unique 
    nuclides = []
    indices = []
    while len(nuclides) < nrofnuclides:
        indx = random.randrange(NNUCLIDES)
        nuclide = radionuclides[indx]
        if nuclide not in nuclides:
            nuclides.append(nuclide)
            indices.append(indx)

    inv = ag.UnstablesInventory(data=[(db.getzai(n), ACTIVITY) for n in nuclides])
    hist, _ = lc(inv, spectype=SPECTYPE)

    # use any bin > 0 = 1, else = 0
    X = [1 if bin > 0 else 0 for bin in hist ]

    datasetX.append(X)#np.array(X))
    datasetY.append(indices)#np.array(indices).astype('int'))

mlb = MultiLabelBinarizer()#classes=len(radionuclides))
datasetY = mlb.fit_transform(datasetY)

#datasetX = StandardScaler().fit_transform(datasetX)
X_train, X_test, y_train, y_test = \
    train_test_split(datasetX, datasetY, test_size=.4, random_state=42)

#print(y_train)
#print(type(y_train))
#y_train = y_train.astype('int')
#y_test = y_test.astype('int')

#print(X_train)
#print(y_train)

classifier.fit(X_train, y_train)
score = classifier.score(X_test, y_test)
print(score)

# predict
inv = ag.UnstablesInventory(data=[
    (db.getzai(radionuclides[2]), ACTIVITY),
    (db.getzai(radionuclides[0]), ACTIVITY),
    (db.getzai(radionuclides[5]), ACTIVITY),
    (db.getzai(radionuclides[3]), ACTIVITY)
])
hist, _ = lc(inv, spectype=SPECTYPE)
print(classifier.predict([[1 if bin > 0 else 0 for bin in hist ]]))
