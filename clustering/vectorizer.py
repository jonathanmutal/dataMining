import gensim.models.word2vec as w2v

import os

import pickle

from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import normalize
from sklearn.decomposition import TruncatedSVD

from collections import defaultdict

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
    def __init__(self, sents, tagger='standford', triples=False):
        self.features_dicts = []
        self.words = []
        self.sents = sents
        self.triples = triples
        self.tagger = tagger

        if self.triples:
            self.__preproccess_triples()

    def __split_feat(self, feat):
        try:
            return (lambda x: (x.split('=')[0], x.split('=')[1]))(feat)
        except IndexError:
            return (feat, "")

    def __split_tags(self, tag):
        return map(self.__split_feat, tag.split('|'))


    def __preproccess_triples(self):
        """
        Only for dependecies triples.
        """
        sents = self.sents
        self.dict_words = dict_words = defaultdict(dict)
        for sent in sents:
            for idx, word in enumerate(sent):
                base_word = word[0].lower()
                pos = word[1]
                tag = word[2]
                dep = word[3]
                dep_word = word[4].lower()
                if base_word not in dict_words.keys():
                    dict_words[base_word]['n'] = 1
                    dict_words[base_word]['features'] = defaultdict(int)
                else:
                    dict_words[base_word]['n'] += 1

                features = dict_words[base_word]['features']

                # for the word
                features[dep + '.' + dep_word] += 1
                features['POS.' + pos] += 1
                for tag_label, tag_feature in self.__split_tags(tag):
                    features[tag_label + '.' + tag_feature] += 1

                # for previus_word
                prevw, prevp, prevt = '<START>', '<START>', '<START>'
                if idx != 0:
                    prevw = sent[idx - 1][0]
                    prevp = sent[idx - 1][1]
                    prevt = sent[idx - 1][2]

                features['word-1.' + prevw.lower()] += 1
                features['POS-1.' + prevp] += 1
                for tag_label, tag_feature in self.__split_tags(prevt):
                    features[tag_label + '-1.' + tag_feature] += 1

                nextw, nextp, nextt = '<END>', '<END>', '<END>'
                if idx != len(sent) - 1:
                    nextw = sent[idx + 1][0]
                    nextp = sent[idx + 1][1]
                    nextt = sent[idx + 1][2]

                features['word+1.' + nextw] += 1
                features['POS+1.' + nextp] += 1
                for tag_label, tag_feature in self.__split_tags(nextt):
                    features[tag_label + '+1.' + tag_feature] += 1


    def __featurize_triples(self):
        for word in self.dict_words:
            if self.dict_words[word]['n'] <= 3:
                continue
            yield dict(self.dict_words[word]['features']), word

    def __featurize_POS(self):
        sents = self.sents
        for sent in sents:
            for idx, word in enumerate(sent):
                onex = {'POS':word[1]}

                # onex['isupper:'] = word[0].isupper()
                onex['istittle:'] = word[0].istitle()
                prevw,prevp = '<START>', '<START>'
                if idx != 0:
                    prevw = sent[idx - 1][0]
                    prevp = sent[idx - 1][1]

                nextw, nextp = '<END>', '<END>'
                if idx != len(sent) - 1:
                    nextw = sent[idx + 1][0]
                    nextp = sent[idx + 1][1]

                onex['word-1:'] = prevw
                onex['pos-1:'] = prevp
                # onex['word-1.isupper'] = prevw.isupper()
                onex['word-1.istitle'] = prevw.istitle()

                onex['word+1:'] = nextw
                onex['pos+1:'] = nextp
                # onex['word+1.isupper'] = nextw.isupper()
                onex['word+1.istitle'] = nextw.istitle()

                if self.tagger == 'standford':
                    onex['word.pos[:2]'] = word[1][:2]
                    onex['word-1.pos[:2]'] = prevp[:2]
                    onex['word+1.pos[:2]'] = nextp[:2]

                yield onex, word[0].lower()

    def feat2dic(self):
        if self.triples:
            self.features_dicts, self.words = zip(*[(dicts, word) for dicts, word in self.__featurize_triples()])
        else:
            self.features_dicts, self.words =  zip(*[(dicts, word) for dicts, word in self.__featurize_POS()])

    def class2pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def dict2matrix(self, sparse=True):
        """
        first you should run feat2dic
        """
        assert(self.features_dicts != [])

        dictV = DictVectorizer(sparse=sparse)
        self.matrix = dictV.fit_transform(self.features_dicts)

    def normalizate(self):
        self.matrix_normalizate = normalize(self.matrix)

    def reduce(self, n_dim=300):
        pca = TruncatedSVD(n_components=n_dim)
        self.matrix_reduced = pca.fit_transform(self.matrix_normalizate)
