import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import random
from collections import defaultdict

class K_means:
    """
    This class is an implementation of K-means algorithm.
    """
    def __init__(self, data, K, num_iter=100):
        """
        K -- how many clusters
        num_iter -- iter to get better clusters
        data -- data to cluster (have to be a numpy array)
        """
        assert K < len(data)
        self.K = K
        self.n = num_iter
        self.data = data

    def euclidean_distance(self, xi, centroid):
        """
        Euclidean distance ||xi-centroid||^2
        xi -- array representing words
        centroid -- array representing the centroid
        """
        return np.linalg.norm(xi - centroid)

    def J(self, classifications, centroids):
        """
        Distortion functions
        classifications -- c^1, ... , c^m
        centroids -- centroids to be evaluated
        """
        m = len(self.data)

        sumatory = 0
        for i, set_xi in classifications.items():
            sumatory += sum(self.euclidean_distance(xi, centroids[i]) for xi in set_xi)

        return sumatory/m

    def __fit(self):
        """
        K-means algorithm
        """
        K = self.K
        n = self.n
        data = self.data

        # init the centroids randomly
        centroids = {}
        for k, idx in enumerate(np.random.choice(range(len(data)), K, replace=False)):
            centroids[k] = data[idx, :]

        for i in range(n):
            # run k-means. cluster aligment step
            # classifications
            classifications = defaultdict(list)
            for xi in data:
                distances = [self.euclidean_distance(xi, centroids[centroid]) for centroid in centroids]
                index_classification = distances.index(min(distances))
                classifications[index_classification].append(xi)

            # move centroids step.
            for classif in classifications:
                centroids[classif] = np.average(classifications[classif], axis=0)

        self.__classifications = classifications
        self.__centroids = centroids

    def get_best_fit(self, max_iter=50):
        """
        Heuristic to improve fitting
        iter -- number of iterations
        return the 'best' classification, centroids
        """
        data = self.data
        best_classif = {}
        best_centroid = {}

        best_J = float('inf')
        for _ in range(max_iter):
            self.__fit()
            J = self.J(self.__classifications, self.__centroids)
            print(J, best_J)
            if J < best_J:
                best_J = J
                best_classif = self.__classifications
                best_centroid = self.__centroids

        return best_classif, best_centroid
