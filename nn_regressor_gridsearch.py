from __future__ import absolute_import
from __future__ import division

import tensorflow as tf
import tflearn
import numpy as np
from read_features import readFeaturesStd

def transformToOneHotLabels(labels):
	labels_onehot = []

	for i in range(len(labels)):
		if labels[i] == 1:
			labels_onehot.append([1,0])
		elif labels[i] == 0:
			labels_onehot.append([0,1])

	return labels_onehot

def createModel(hidden_layers_neurons, activations, optimizer, learning_rate, metric, loss ):
	input_layer = tflearn.input_data(shape=[None, 5])
	layers = []
	layers.append(input_layer)
	for i in range(len(hidden_layers_neurons)):
		layers.append(tflearn.fully_connected( layers[i], hidden_layers_neurons[i], activation = activations[i]))

	output_layer  = tflearn.fully_connected(layers[-1], 2, activation = activations[-1])
	regression = tflearn.regression(output_layer, optimizer = optimizer, 
									   learning_rate = learning_rate, 
									   metric = metric, 
									   loss = loss)
	model = tflearn.DNN(regression)

	return model

train_features, train_labels = readFeaturesStd('data/train_features.csv')
test_features, test_labels = readFeaturesStd('data/test_features.csv')

train_labels_onehot = transformToOneHotLabels(train_labels)
test_labels_onehot = transformToOneHotLabels(test_labels)

hidden_layer_neurons = [10,10]#[[5,5], [10, 10], [20, 20]]
activation_functions = ['linear']#['linear', 'tanh', 'sigmoid', 'softmax', 'relu']
epochs_n = [20]#[20, 50]
learning_rates = [0.001]#[0.001, 0.005, 0.01, 0.05]

max_correctly_predicted_ratio = 0
max_parameters = []

for hln in range(len(hidden_layer_neurons)):
	for af in range(len(activation_functions)):
		activations = []
		for i in range(len(hidden_layer_neurons[hln])):
			activations.append(activation_functions[af])
		activations.append(activation_functions[-1])
		print(activations)

		for lr in range(len(learning_rates)):
			for en in range(len(epochs_n)):
				with tf.Graph().as_default():
					model = createModel(hidden_layer_neurons[hln], activations, 'adam', learning_rates[lr], 'Accuracy', 'mean_square')
					
					x_train = train_features
					y_train = train_labels_onehot

					x_test = test_features
					y_test = test_labels_onehot

					model.fit(x_train, y_train, n_epoch = epochs_n[en], validation_set=0.2, show_metric=True)

					pred = model.predict(x_test)

					correctly_predicted_n = 0
					for i in range(len(y_test)):
						chances = [pred[i][0] / (pred[i][0]+pred[i][1]), pred[i][1] / (pred[i][0]+pred[i][1])]
						if (test_labels_onehot[i][0] > test_labels_onehot[i][1]) & (pred[i][0] > pred[i][1]):
							correctly_predicted_n += 1
						if (test_labels_onehot[i][0] < test_labels_onehot[i][1]) & (pred[i][0] < pred[i][1]):
							correctly_predicted_n += 1
					#print('test: ', test_labels_onehot[i], 'pred: ', pred[i], 'chances: ', chances)

					correctly_predicted_ratio = correctly_predicted_n / len(test_labels)
					print 'parameters: ', [hidden_layer_neurons[hln], activations, learning_rates[lr], epochs_n[en]] 
					print 'correctly predicted ratio: ', correctly_predicted_ratio

					if (correctly_predicted_ratio > max_correctly_predicted_ratio):
						max_correctly_predicted_ratio = correctly_predicted_ratio
						max_parameters = [hidden_layer_neurons[hln], activations,  learning_rates[lr], epochs_n[en]]

					print 'max parameters' , max_parameters
					print 'max correctly predicted ratio: ', max_correctly_predicted_ratio
				

   