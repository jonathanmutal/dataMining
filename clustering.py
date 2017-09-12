import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import random
from collections import defaultdict

class K_means:
    """
    This class is an implementation of K-means algorithm.
    """
    def __init__(self, K, num_iter=10):
        """
        K -- how many clusters
        num_iter -- iter to get better clusters
        """
        self.K = K
        self.n = num_iter

    def fit(self, data):
        """
        K-means algorithm
        data -- data to cluster (have to be a numpy array)
        """
        K = self.K
        n = self.n

        # init the centroids randomly
        centroids = {}
        for k, idx in enumerate(np.random.choice(range(len(data)), K, replace=False)):
            centroids[k] = data[idx, :]

        for i in range(n):
            # run k-means. cluster aligment step
            # classifications
            classifications = defaultdict(list)
            for xi in data:
                distances = [np.linalg.norm(xi - centroids[centroid]) for centroid in centroids]
                index_classification = distances.index(min(distances))
                classifications[index_classification].append(xi)

            # move centroids step.
            for classif in classifications:
                centroids[classif] = np.average(classifications[classif], axis=0)

            self.classifications = classifications
            self.centroids = centroids

X = np.array([[1, 2],
              [1.5, 1.8],
              [5, 8 ],
              [8, 8],
              [1, 0.6],
              [9,11]])

plt.scatter(X[:,0], X[:,1], s=150, c='r', alpha=0.7)
plt.subplots()

k_means = K_means(2)
k_means.fit(X)
classif = k_means.classifications
centroids = k_means.centroids

for i in classif[0]:
    plt.scatter(i[0], i[1], s=50, c='r', alpha=0.5)

for i in classif[1]:
    plt.scatter(i[0], i[1], s=50, c='b', alpha=0.5)

print(centroids)
plt.plot(centroids[0][0], centroids[0][1], 'r*')
plt.plot(centroids[1][0], centroids[1][1], 'b*')

plt.show()