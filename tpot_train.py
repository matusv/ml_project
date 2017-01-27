from tpot import TPOTClassifier 
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import pandas as pd
import numpy as np
from read_features import readFeaturesStd

train_features, train_labels = readFeaturesStd('data/train_features.csv')
test_features, test_labels = readFeaturesStd('data/test_features.csv')

#tpot uses genetic algorithm to find the optimal pipeline of ml models
#train tpot and export the pipeline it found
tpot = TPOTClassifier(generations=5, verbosity=2)  
tpot.fit(train_features, train_labels)  
print(tpot.score(test_features, test_labels))
tpot.export('pipeline2.py')

print('done')