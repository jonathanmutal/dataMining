from nltk.data import LazyLoader
from nltk.tag.stanford import StanfordPOSTagger
from nltk.corpus import stopwords

from collections import defaultdict

from string import punctuation

import spacy
import codecs
import re

STOPWORDS = stopwords.words('spanish')

pattern = r'''(?ix)    # set flag to allow verbose regexps
    (?:sr\.|sra\.|mr\.|mrs\.)
    | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
    | \w+(?:-\w+)*        # words with optional internal hyphens
    '''

regex = re.compile(pattern)

class Normalization:
    def __init__(self, path='/home/jmutal/dataMining/lavoztextodump.txt',
                 word_tokenizer=regex,
                 sent_tokenizer=LazyLoader('tokenizers/punkt/spanish.pickle')):
        self.path = path
        self.__word_tokenizer = word_tokenizer
        self.__sent_tokenizer = sent_tokenizer

        # Should optimaze for big files
        with codecs.open(self.path, 'r', 'utf-8') as f:
            corpus = f.read()

        corpus_sent = self.__sent_tokenizer.tokenize(corpus)
        self.clean_corpus = [re.sub('&#\d+;', '', sents) for sents in corpus_sent]

    def dig2num(self, sents):
        ready_sents = []
        for sent in sents:
            ready_sents.append([(re.sub('\d+', 'NUM', word[0]),) + word[1:] for word in sent if word[0].lower() not in STOPWORDS])
        return ready_sents

    def tokenize(self, tagg='standford'):
        if tagg == 'standford':
            self.clean_corpus = [self.__word_tokenizer.findall(sent) for sent in self.clean_corpus]
        else:
            self.clean_corpus = [' '.join(self.__word_tokenizer.findall(sent)) for sent in self.clean_corpus]

class TAG_norm(Normalization):
    def __init__(self, path='/home/jmutal/dataMining/lavoztextodump.txt', taggerUse='standford', lemm=False):
        super().__init__(path=path)

        self.taggerUse = taggerUse
        if self.taggerUse == 'spacy':
            self.nlp = spacy.load('es')

        self.lemm = lemm
        if self.lemm:
            self.__load_lemm()

    def __load_lemm(self):
        self.lemma_dict = lemma_dict = defaultdict(str)
        with open('/home/jmutal/dataMining/lemmatization-es.txt') as f:
            for line in f:
                splited_line = line.split('\t')
                lemma_dict[splited_line[1].strip()] = splited_line[0]

    def proccess_spacy(self, sents):
        for sent in sents:
            list_words = []
            for word in sent:
                base_word = word.text
                if self.lemm:
                    if base_word in self.lemma_dict.keys(): base_word = self.lemma_dict[base_word]
                list_words.append((base_word, word.pos_, word.tag_, word.dep_, word.head.orth_))
            yield list_words

    def tagger(self):
        self.tokenize(self.taggerUse)
        if self.taggerUse == 'standford':
            tagger = StanfordPOSTagger('/home/jmutal/dataMining/stanford-postagger-full-2017-06-09/models/spanish-distsim.tagger',
                               '/home/jmutal/dataMining/stanford-postagger-full-2017-06-09/stanford-postagger-3.8.0.jar')
            tagged_sents = tagger.tag_sents(self.clean_corpus)
        else:
            tagged_sents = self.nlp.pipe(self.clean_corpus, n_threads=8)
            tagged_sents = self.proccess_spacy(tagged_sents)

        return self.dig2num(tagged_sents)

class WC_token:
    """
    Tokenize wiki corpus.
    path -- path where the files are
    file -- file you want to tokenize
    """
    def __init__(self, path="/home/jmutal/dataMining/tagged.es",
                 file="spanishEtiquetado1"):
        with open(path + "/" + file) as f:
            raw_data = f.read()

        self.count_words = defaultdict(int)
        self.STOPWORDS = STOPWORDS + ["ENDOFARTICLE"]
        self.STOPWORDS += list(punctuation)
        self.__split_data(raw_data)

    def __split_word(self, word):
        return word.split(" ")
 
    def __split_data(self, raw_data):
        sentences = []
        sent = []
        for word in raw_data.split("\n"):
            if not word:
                if len(sent) >= 2:
                    sentences.append(sent)
                sent = []
                continue
            if word.startswith('<doc') or word.startswith('</doc>'):
                continue
            word_, lemma, tag, synsent = self.__split_word(word)
            if word_ in self.STOPWORDS:
                continue
            sent.append((word_, lemma, tag, synsent))
            self.count_words[lemma] += 1

        self.splited_data = sentences

