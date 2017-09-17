from nltk.data import LazyLoader

import spacy

import codecs
import re

pattern = r'''(?ix)    # set flag to allow verbose regexps
    (?:sr\.|sra\.|mr\.|mrs\.)
    | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
    | \w+(?:-\w+)*        # words with optional internal hyphens
    '''

regex = re.compile(pattern)

class Normalization:
    def __init__(self, path='../lavoztextodump.txt',
                 word_tokenizer=regex,
                 sent_tokenizer=LazyLoader('tokenizers/punkt/spanish.pickle')):
        self.path = path
        self.__word_tokenizer = word_tokenizer
        self.__sent_tokenizer = sent_tokenizer

        # Should optimaze for big files
        with codecs.open(self.path, 'r', 'utf-8') as f:
            corpus = f.read()

        corpus_sent = self.__sent_tokenizer.tokenize(corpus)
        self.corpus_clean = [re.sub('&#\d+', '', sents) for sents in corpus_sent]

    def digit_to_NUM(self):
        self.corpus_clean = [re.sub('\d+', 'NUM', sent) for sent in self.corpus_clean]

    def tokenize(self):
        clean_corpus = [self.__word_tokenizer.findall(sents) for sents in self.corpus_clean]

        return clean_corpus

class Procc:
    def __init_(self, path='~/dataMining/lavoztextodump.txt'):
        with codecs.open(self.path, 'r', 'utf-8') as f:
            corpus = f.read()

        nlp = spacy.load('es_core_web_md')
        doc = nlp(corpus)
        self.doc = doc
