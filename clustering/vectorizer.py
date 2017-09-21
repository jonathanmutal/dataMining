import gensim.models.word2vec as w2v

import os

from sklearn.feature_extraction import DictVectorizer

class W2V_wrapper:
    def __init__(self, data, path='~/dataMining/clustering'):
        self.clean_corpus = data
        self.path = path

    def config(self):
        """
        Add some arguments to config
        """
        model = w2v.Word2Vec(
            sg=1,
            seed=1,
            workers=4,
            size=300,
            min_count=100,
            window=7,
            sample=1e-3
        )

        self.model = model

    def train(self):
        self.model.build_vocab(self.clean_corpus)
        self.model.train(self.clean_corpus, total_examples=self.model.corpus_count,
                         epochs=self.model.iter)

    def save(self, name='model.w2v'):
        self.model.save(os.path.join(self.path, name))

    def load(self, name='model.w2v'):
        return w2v.Word2Vec.load(os.path.join(self.path, name))


class Featurize:
    def __init__(self, sents, triples=False):
        self.sents = sents
        self.dictVectorizer = []
        self.words = []
        self.triples = triples # don't forget it about triples

    def __featurize_POS(self):
        sents = self.sents
        for sent in  sents:
            for idx, word in enumerate(sent):
                onex = {'POS':word[1]}

                onex['isupper:'] = word[0].isupper()
                onex['lower:'] = word[0].lower()
                onex['istittle:'] = word[0].istitle()
                prevw,prevp = '<START>', '<START>'
                if idx != 0:
                    prevw = sent[idx - 1][0]
                    prevp = sent[idx - 1][1]

                nextw, nextp = '<END>','<END>'
                if idx != len(sent) - 1:
                    nextw = sent[idx + 1][0]
                    nextp = sent[idx + 1][1]

                onex['word-1:'] = prevw
                onex['pos-1:'] = prevp
                onex['word-1.pos[:2]'] = prevp[:2]
                onex['word-1.isupper'] = prevw.isupper()
                onex['word-1.istitle'] = prevw.istitle()

                onex['word+1:'] = nextw
                onex['pos+1:'] = nextp
                onex['word+1.pos[:2]'] = nextp[:2]
                onex['word+1.isupper'] = nextw.isupper()
                onex['word+1.istitle'] = nextw.istitle()

                # to save word
                yield onex, word[0]

    def __feat2dic(self):
        return zip(*[(dicts, word) for dicts, word in self.__featurize_POS()])

    def dict2matrix(self, sparse=False):
        dicts, words = self.__feat2dic()
        dictV = DictVectorizer(sparse=sparse)
        matrix = dictV.fit_transform(dicts)
        return matrix, words
