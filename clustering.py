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
                centroids[k] = np.average(classifications[classif], axis=0)

k_means = K_means(2)