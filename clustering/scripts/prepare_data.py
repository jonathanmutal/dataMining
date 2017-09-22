from vectorizer import W2V_wrapper, Featurize
from preproccess import Normalization, TAG_norm

import pickle

def w2v_train_data():
    data = Normalization()
    data.digit_to_NUM()
    corpus = data.tokenize()
    w2v_ = W2V_wrapper(corpus)
    w2v_.config()
    w2v_.train()
    w2v_.save()

def save_dict():
    tagger = TAG_norm()
    tagg_data = tagger.tagger()
    featurize = Featurize(tagg_data)
    featurize.feat2dic()
    featurize.class2pickle('test.pickle')

def load_dict(filename):
    """
    filename -- filename of pickle
    """
    features = []
    with open(filename, 'rb') as f:
        features = pickle.load(f)
    return features
