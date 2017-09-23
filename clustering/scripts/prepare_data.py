from clustering.vectorizer import W2V_wrapper, Featurize
from clustering.preproccess import Normalization, TAG_norm
from clustering.clustering import Kmeans

from sklearn.cluster import KMeans

from collections import defaultdict

import pickle

def w2v_train_data():
    data = Normalization()
    data.digit_to_NUM()
    corpus = data.tokenize()
    w2v_ = W2V_wrapper(corpus)
    w2v_.config()
    w2v_.train()
    w2v_.save()

def save_dict(filename):
    tagger = TAG_norm()
    tagg_data = tagger.tagger()
    featurize = Featurize(tagg_data)
    featurize.feat2dic()
    featurize.class2pickle(filename)

def load_dict(filename):
    """
    filename -- pickle's file name
    """
    features = []
    with open(filename, 'rb') as f:
        features = pickle.load(f)
    return features

if __name__ == '__main__':
    save_dict('test.pickle')
    v = load_dict('test.pickle')
    matrix, words = v.dict2matrix(sparse=False)
    # Km = KMeans().fit(matrix)

    # clusters = defaultdict(set)
    # for i, label in enumerate(Km.labels_):
    #     clusters[label].add(words[i])

    # for i, clus in enumerate(clusters):
    #     print(i, clusters[clus])

    clusters, centroids = Kmeans(matrix, 15).get_best_fit()
    for cluster in clusters:
        cl = set(map(lambda x: words[matrix.index(x)], clusters[cluster]))
        print(cluster, cl)
