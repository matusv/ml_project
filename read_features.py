from sklearn import preprocessing
import pandas as pd
import numpy as np

def readFeaturesStd(filename):
	"""reads features and scales them"""
	data = pd.read_csv(filename)
	features = data.ix[:,: - 1].values
	labels = data.iloc[:,-1].values
	features_std = preprocessing.StandardScaler().fit_transform(features)
	return features_std, labels