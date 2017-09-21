from vectorizer import W2V_wrapper, Featurize
from preproccess import Normalization, TAG_norm

def w2v_train_data():
    data = Normalization()
    data.digit_to_NUM()
    corpus = data.tokenize()
    w2v_ = W2V_wrapper(corpus)
    w2v_.config()
    w2v_.train()
    w2v_.save()

# def features_manual():
tagger = TAG_norm()
tagg_data = tagger.tagger()
featurize = Featurize(tagg_data)
matrix, words = featurize.dict2matrix()

