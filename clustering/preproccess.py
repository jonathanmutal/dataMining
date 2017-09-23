from nltk.data import LazyLoader
from nltk.tag.stanford import StanfordPOSTagger
from nltk.corpus import stopwords

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
    def __init__(self, path='/home/jonathan/dataMining/lavoztextodump.txt',
                 word_tokenizer=regex,
                 sent_tokenizer=LazyLoader('tokenizers/punkt/spanish.pickle')):
        self.path = path
        self.__word_tokenizer = word_tokenizer
        self.__sent_tokenizer = sent_tokenizer

        # Should optimaze for big files
        with codecs.open(self.path, 'r', 'utf-8') as f:
            corpus = f.read(6000)

        corpus_sent = self.__sent_tokenizer.tokenize(corpus)
        self.corpus_clean = [re.sub('&#\d+', '', sents) for sents in corpus_sent]

    def dig2num(self, sents):
        ready_sents = []
        for sent in sents:
            ready_sents.append([(re.sub('\d+', 'NUM', word[0]),) + word[1:] for word in sent if word[0].lower() not in stopwords.words('spanish')])
        return ready_sents

    def tokenize(self):
        self.clean_corpus = [self.__word_tokenizer.findall(sent) for sent in self.corpus_clean]

class TAG_norm(Normalization):
    def __init__(self, path='/home/jonathan/dataMining/lavoztextodump.txt', taggerUse='standford'):
        super().__init__(path=path)

        self.taggerUse = taggerUse
        self.tokenize()
        if self.taggerUse != 'standford':
            self.nlp = spacy.load('es_core_web_md')

    def tagger(self):
        if self.taggerUse == 'standford':
            tagger = StanfordPOSTagger('/home/jonathan/dataMining/stanford-postagger-full-2017-06-09/models/spanish-distsim.tagger',
                               '/home/jonathan/dataMining/stanford-postagger-full-2017-06-09/stanford-postagger-3.8.0.jar')
            tagged_sents = tagger.tag_sents(self.clean_corpus)
        else:
            tagged_sents = self.nlp(self.clean_corpus, parse=False, entity=False)
        return self.dig2num(tagged_sents)
