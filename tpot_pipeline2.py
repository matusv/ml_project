from __future__ import division
import numpy as np
from sklearn.decomposition import FastICA
from sklearn.ensemble import ExtraTreesClassifier, VotingClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.kernel_approximation import RBFSampler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import FunctionTransformer
from read_features import readFeaturesStd
from data_vis import show_confusion_matrix

train_features, train_labels = readFeaturesStd('data/train_features.csv')
test_features, test_labels = readFeaturesStd('data/test_features.csv')

exported_pipeline = make_pipeline(
    make_union(
        SelectFromModel(estimator=ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',
                   max_depth=None, max_features=0.76000000000000001,
                   max_leaf_nodes=None, min_impurity_split=1e-07,
                   min_samples_leaf=1, min_samples_split=2,
                   min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
                   oob_score=False, random_state=None, verbose=0, warm_start=False), threshold=0.33),
        FastICA(tol=0.39)
    ),
    RBFSampler(gamma=0.86),
    ExtraTreesClassifier(criterion="gini", max_features=1.0, n_estimators=500)
)

exported_pipeline.fit(train_features, train_labels)
predictions = exported_pipeline.predict(test_features)

correctly_predicted_n = sum(predictions[:] == test_labels[:])
print "correctly predcited: ", correctly_predicted_n
print 'number of test samples: ', len(test_labels)
print 'correctly predicted ratio: ', (correctly_predicted_n / len(test_labels))

show_confusion_matrix(test_labels, predictions, title='tpot_pipeline2 acc:' + str(correctly_predicted_n / len(test_labels)))
