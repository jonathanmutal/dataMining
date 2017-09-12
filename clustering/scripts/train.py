from clustering.clustering import Kmeans

import matplotlib.pyplot as plt

import numpy as np


X = np.array([[1, 2],
              [1.5, 1.8],
              [5, 8],
              [8, 8],
              [1, 0.6],
              [9, 11],
              [1, 3],
              [8, 9],
              [0, 3],
              [5, 4],
              [6, 4]])

colors = 10 * ["g", "r", "c", "b", "k"]
clf = Kmeans(X, 3)
classifications, centroids = clf.get_best_fit()

for centroid in centroids:
    plt.scatter(centroids[centroid][0], centroids[centroid][1],
                marker="o", color="k", linewidths=5)

for classification in classifications:
    color = colors[classification]
    for featureset in classifications[classification]:
        plt.scatter(featureset[0], featureset[1], marker="x",
                    color=color, linewidths=5)
plt.show()
