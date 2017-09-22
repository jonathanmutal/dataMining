from nltk.data import LazyLoader
from nltk.tag.stanford import StanfordPOSTagger

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
            corpus = f.read(1000)

        corpus_sent = self.__sent_tokenizer.tokenize(corpus)
        self.corpus_clean = [re.sub('&#\d+', '', sents) for sents in corpus_sent]

    def digit_to_NUM(self, words):
        return [(re.sub('\d+', 'NUM', word[0]), word[1:]) for word in words]

    def tokenize(self):
        clean_corpus = [self.__word_tokenizer.findall(sent) for sent in self.corpus_clean]

        return clean_corpus

class TAG_norm(Normalization):
    def __init_(self, path='~/dataMining/lavoztextodump.txt'):
        super().__init__(path=path)

    def tagger(self):
        corpus_clean = self.tokenize()
        tagger = StanfordPOSTagger('/home/jonathan/dataMining/stanford-postagger-full-2017-06-09/models/spanish-distsim.tagger',
                                   '/home/jonathan/dataMining/stanford-postagger-full-2017-06-09/stanford-postagger-3.8.0.jar')
        tagged_sents = tagger.tag_sents(corpus_clean)
        return tagged_sents
