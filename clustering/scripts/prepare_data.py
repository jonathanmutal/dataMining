from clustering.vectorizer import W2V_wrapper
from clustering.preprocess import Normalization

def w2v_data():
    data = Normalization()
    data.digit_to_NUM()
    corpus = data.tokenize()
    w2v_ = W2V_wrapper(corpus)
    w2v_.config()
    w2v_.train()
    w2v_.save()
    # model = w2v_.load()

def manual_features():
    raise NotImplementedError()
