from collections import defaultdict
from sklearn.cluster import KMeans


import numpy as np
import sys

def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    # \b backspace
    print('\b' * (width + 1) + msg, end='')
    sys.stdout.flush()

class Kmeans:
    """
    This class is an implementation of K-means algorithm.
    """
    def __init__(self, data, k, num_iter=100, tol=0.001):
        """
        K -- how many clusters
        num_iter -- iter to get better clusters
        data -- data to cluster (have to be a numpy array)
        tol -- tolerance (to optimaze k-means)
        """
        self.k = k
        self.n = num_iter
        self.data = data
        self.tol = tol

    def euclidean_distance(self, xi, centroid):
        """
        Euclidean distance ||xi-centroid||
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
            sumatory += sum(self.euclidean_distance(xi, centroids[i]) for xi in
                            set_xi)

        return sumatory / m

    def __fit(self):
        """
        K-means algorithm
        """
        k = self.k
        n = self.n
        data = self.data

        # init the centroids randomly
        centroids = {}
        for k, idx in enumerate(np.random.choice(range(len(data)), k,
                                replace=False)):
            centroids[k] = data[idx, :]

        for i in range(n):
            # run k-means. cluster aligment step
            # classifications
            classifications = defaultdict(list)
            i_classifications = defaultdict(list)
            for idx, xi in enumerate(data):
                distances = [self.euclidean_distance(xi, centroids[centroid]) for centroid in centroids]
                index_classification = distances.index(min(distances))
                classifications[index_classification].append(xi)
                i_classifications[index_classification].append(idx)

            # to optimaze
            prev_centroids = dict(centroids)

            # move centroids step.
            for classif in classifications:
                centroids[classif] = np.average(classifications[classif],
                                                axis=0)

            # optimaze with tol of tolerance
            optimaze = True
            for k, c in centroids.items():
                prev_centr = prev_centroids[k]
                actual_centr = c
                if abs(np.sum(actual_centr - prev_centr)) > self.tol:
                    optimaze = False

            if optimaze:
                break
            progress('{:2.2f}%'.format(i / n * 100))
        self.__classifications = classifications
        self.__centroids = centroids
        self.__i_classifications = i_classifications

    def get_best_fit(self, max_iter=10):
        """
        Heuristic to improve fitting
        iter -- number of iterations
        return the 'best' classification, centroids
        """
        best_classif = {}
        best_centroid = {}

        best_j = float('inf')
        for _ in range(max_iter):
            self.__fit()
            j = self.J(self.__classifications, self.__centroids)
            if j < best_j:
                best_j = j
                best_classif = self.__classifications
                best_i_classif = self.__i_classifications
                best_centroid = self.__centroids

        return best_i_classif, best_centroid


class Kmeans_WR:
    def __init__(self, K, data, words):
        self.K = K
        self.data = data
        self.words = words
        self.Km = KMeans(n_clusters=self.K, n_init=15)

    def euclidean_distance(self, xi, centroid):
        """
        Euclidean distance ||xi-centroid||
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
        for idx, label in enumerate(classifications):
            sumatory += self.euclidean_distance(self.data[idx], centroids[label])

        return sumatory / m


    def fit(self):
        self.Km.fit(self.data)

        clusters = defaultdict(set)
        for i, label in enumerate(self.Km.labels_):
            clusters[label].add(self.words[i])

        return clusters

    def get_best_K(self, init=5, end=60, jump=5):
        best_K = []
        for k in np.arange(init, end+1, jump):
            Km = KMeans(n_clusters=k, n_init=20).fit(self.data)
            best_K.append((k, self.J(Km.labels_, Km.cluster_centers_)))

        return best_K
