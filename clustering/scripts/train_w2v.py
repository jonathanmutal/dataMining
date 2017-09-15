from nltk.data import LazyLoader
from nltk.tokenize import word_tokenize

import gensim.models.word2vec as w2v

import re
import codecs


class W2V_wrapper:

    def __init__(self, path='../../lavoztextodump.txt',
                 word_tokenizer=word_tokenize,
                 sent_tokenizer=LazyLoader('tokenizers/punkt/spanish.pickle')):
        self.path = path
        self.word_tokenizer = word_tokenizer
        self.sent_tokenizer = sent_tokenizer

    def __raw_data(self):
        """
        Should optimaze for big files
        """
        with codecs.open(self.path, 'r', 'utf-8') as f:
            corpus = f.read()

        return corpus

    def __tokenize(self):
        corpus = self.__raw_data()
        corpus_sent = self.sent_tokenizer.tokenize(corpus)
        clean_corpus = [regex.findall(re.sub('\d+', 'NUM', re.sub('&#\d+', '', sents))) for sents in corpus_sent]

        return clean_corpus

    def config(self):
        """
        Add some arguments to config
        """
        model = w2v.Word2Vec(
            sg=1,
            seed=1,
            workers=4,
            size=300,
            min_count=3,
            window=7,
            sample=1e-3
        )

        self.model = model

    def train(self):
        clean_corpus = self.__tokenize()
        self.model.build_vocab(clean_corpus)
        print(self.model.iter)
        self.model.train(clean_corpus, total_examples=self.model.corpus_count,
                         epochs=self.model.iter)

    def save(self):
        self.model.save('model.w2v')

pattern = r'''(?ix)    # set flag to allow verbose regexps
        (?:sr\.|sra\.|mr\.|mrs\.)
        | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
        | \w+(?:-\w+)*        # words with optional internal hyphens
        '''
regex = re.compile(pattern)

w2v_ = W2V_wrapper(word_tokenizer=regex)
w2v_.config()
w2v_.train()
w2v_.save()
