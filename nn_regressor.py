from __future__ import absolute_import
from __future__ import division

import tensorflow as tf
import tflearn
import numpy as np
from read_features import readFeaturesStd

train_features, train_labels = readFeaturesStd('data/train_features.csv')
test_features, test_labels = readFeaturesStd('data/test_features.csv')

train_labels_onehot = []
test_labels_onehot = []

for i in range(len(train_labels)):
	if train_labels[i] == 1:
		train_labels_onehot.append([1,0])
	elif train_labels[i] == 0:
		train_labels_onehot.append([0,1])

for i in range(len(test_labels)):
	if test_labels[i] == 1:
		test_labels_onehot.append([1,0])
	elif test_labels[i] == 0:
		test_labels_onehot.append([0,1])

with tf.Graph().as_default():
	input_layer = tflearn.input_data(shape=[None, 5])
	layer1 = tflearn.fully_connected(input_layer, 10, activation='linear')
	layer2 = tflearn.fully_connected(layer1, 10, activation='linear')
	output_layer  = tflearn.fully_connected(layer2, 2, activation='linear')
	regression = tflearn.regression(output_layer, optimizer='adam', 
										   learning_rate=0.001, 
										   metric=tflearn.Accuracy(), 
										   loss='mean_square')

	model = tflearn.DNN(regression)

	model.fit(train_features, train_labels_onehot, n_epoch=20, validation_set=0.2, show_metric=True)

	pred = model.predict(test_features)

	correctly_predicted_n = 0
	for i in range(len(test_labels_onehot)):
		chances = [pred[i][0] / (pred[i][0]+pred[i][1]), pred[i][1] / (pred[i][0]+pred[i][1])]
		if (test_labels_onehot[i][0] > test_labels_onehot[i][1]) & (pred[i][0] > pred[i][1]):
			correctly_predicted_n += 1
		if (test_labels_onehot[i][0] < test_labels_onehot[i][1]) & (pred[i][0] < pred[i][1]):
			correctly_predicted_n += 1
		#print('test: ', test_labels_onehot[i], 'pred: ', pred[i], 'chances: ', chances)

	print ('correctly predicted ratio: ', (correctly_predicted_n / len(test_labels)))

   