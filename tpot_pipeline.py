from __future__ import division
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import FunctionTransformer
from sklearn import preprocessing
from read_features import readFeaturesStd
from data_vis import show_confusion_matrix

train_features, train_labels = readFeaturesStd('data/train_features.csv')
test_features, test_labels = readFeaturesStd('data/test_features.csv')

pipeline = make_pipeline(
    make_union(VotingClassifier([("est", LogisticRegression(C=50.0, dual=False, penalty="l1"))]), FunctionTransformer(lambda X: X)),
    RandomForestClassifier(n_estimators=500)
)

pipeline.fit(train_features, train_labels)
predictions = pipeline.predict(test_features)

correctly_predicted_n = sum(predictions[:] == test_labels[:])
print "correctly predcited: ", correctly_predicted_n
print 'number of test samples: ', len(test_labels)
print 'correctly predicted ratio: ', (correctly_predicted_n / len(test_labels))

show_confusion_matrix(test_labels, predictions, title='tpot_pipeline acc: ' + str(correctly_predicted_n / len(test_labels)))