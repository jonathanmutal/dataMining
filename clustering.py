class K_mean:
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
        n = self.num_iter

        for i in range(n):
            # init the centroids randomly
            centroids = {}
            for k, word_vec in enumerate(random.sample(data, K)):
                centroids[k] = word_vec

            # run k-means. cluster aligment step
            # classifications
            classifications = defaultdict(list)
            for xi in data:
                distances = [np.align.norm(xi - centroids[centroid]) for centroid in centroids]
                index_classification = distances.index(min(distances))
                classifications[index_classification].append(xi)