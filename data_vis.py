import itertools
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def visualize3d(filename):
	#read data and divide into features and labels
	data_all = pd.read_csv(filename)
	x = data_all.ix[:,: - 1].values
	labels = data_all.iloc[:,-1].values
	
	#scale data
	x_std = preprocessing.StandardScaler().fit_transform(x)
	
	#reduce dimensions
	tsne = TSNE(n_components = 3, random_state = 0)
	x_3d = tsne.fit_transform(x_std)
	
	marker_map = {0: 's', 1: 'd'}
	color_map = {0: 'red', 1: 'blue'}

	#plot data
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for i in range(len(x_3d)):
		ax.scatter(x_3d[i][0], x_3d[i][1], x_3d[i][2], s = 10, linewidth='0', c = color_map[labels[i]], marker = '.')

	plt.show()
	return

def show_confusion_matrix(test_labels, predictions, title = 'confusion matrix'):
	#Compute confusion matrix
	cnf_matrix = confusion_matrix(test_labels, predictions)
	np.set_printoptions(precision=2)

	#Plot confusion matrix
	plt.figure()
	plot_confusion_matrix(cnf_matrix, classes=['0', '1'],
                      title=title)

	plt.show()

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color= "black")#"white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


