from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
from read_features import readFeaturesStd
from data_vis import show_confusion_matrix

#read data
train_features, train_labels = readFeaturesStd('data/train_features.csv')
test_features, test_labels = readFeaturesStd('data/test_features.csv')

tf.logging.set_verbosity(tf.logging.INFO)
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=5)]

#create, train, evaluate neural network
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns, hidden_units=[10, 10], n_classes=2)
classifier.fit(x = train_features, y = train_labels, steps = 4000)
accuracy_score = classifier.evaluate(x=test_features, y=test_labels)["accuracy"]

#make predictions for test set
predictions = list(classifier.predict(test_features, as_iterable=True))
correctly_predicted_n = sum(predictions[:] == test_labels[:])
print ('correctly predicted ratio: ', (correctly_predicted_n / len(test_labels)))

#show confusion matrix
show_confusion_matrix(test_labels, predictions, title='nn_classifier acc:' + str(correctly_predicted_n / len(test_labels)))

