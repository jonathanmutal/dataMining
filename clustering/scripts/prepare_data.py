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

def save_dict_cluster1(filename):
    tagger = TAG_norm()
    tagg_data = tagger.tagger()
    featurize = Featurize(tagg_data)
    featurize.feat2dic()
    featurize.class2pickle(filename)

def save_dict_cluster2(filename):
    tagger = TAG_norm(taggerUse='spacy')
    tagg_data = tagger.tagger()
    featurize = Featurize(tagg_data, triples=True)
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

def cluster1():
    save_dict_cluster1('test_cl1.pickle')
    v = load_dict('test_cl1.pickle')
    matrix, words = v.dict2matrix(sparse=True)
    Km = KMeans(n_clusters=30).fit(matrix)

    clusters = defaultdict(set)
    for i, label in enumerate(Km.labels_):
        clusters[label].add(words[i])

    for i, clus in enumerate(clusters):
        print(i, clusters[clus])

def cluster2():
    save_dict_cluster2('test_cl2.pickle')
    print('Cluster2 save it')
    v = load_dict('test_cl2.pickle')
    print('Cluster2 load')
    v.feat2dic()
    matrix, words = v.dict2matrix(sparse=True)
    Km = KMeans(n_clusters=30).fit(matrix)

    clusters = defaultdict(set)
    for i, label in enumerate(Km.labels_):
        clusters[label].add(words[i])

    for i, clus in enumerate(clusters):
        print(i, clusters[clus])

if __name__ == '__main__':
    cluster2()

    # clusters, centroids = Kmeans(matrix, 20).get_best_fit()
    # for cluster in clusters:
    #     cl = set(map(lambda x: words[x], clusters[cluster]))
    #     print(cluster, cl)
