from nltk.data import LazyLoader
import gensim.models.word2vec as w2v

import re
import codecs

pattern = r'''(?ix)    # set flag to allow verbose regexps
        (?:sr\.|sra\.|mr\.|mrs\.)
        | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
        | \w+(?:-\w+)*        # words with optional internal hyphens
        '''

with codecs.open('../../lavoztextodump.txt', 'r', 'utf-8') as f:
    corpus = f.read()

regex = re.compile(pattern)
sent_tokenizer = LazyLoader('tokenizers/punkt/spanish.pickle')
corpus_sent = sent_tokenizer.tokenize(corpus)
clean_corpus = [' '.join(regex.findall(re.sub('\d+', 'NUM', re.sub('&#\d+', '', sents)))) for sents in corpus_sent]

model = w2v.Word2Vec(clean_corpus, sg=1, size=300, window=5, min_count=5, workers=4, compute_loss=True)
model.save('model.w2v')
# X = np.array([[1, 2],
#               [1.5, 1.8],
#               [5, 8],
#               [8, 8],
#               [1, 0.6],
#               [9, 11],
#               [1, 3],
#               [8, 9],
#               [0, 3],
#               [5, 4],
#               [6, 4]])

# colors = 10 * ["g", "r", "c", "b", "k"]
# clf = Kmeans(X, 3)
# classifications, centroids = clf.get_best_fit()

# for centroid in centroids:
#     plt.scatter(centroids[centroid][0], centroids[centroid][1],
#                 marker="o", color="k", linewidths=5)

# for classification in classifications:
#     color = colors[classification]
#     for featureset in classifications[classification]:
#         plt.scatter(featureset[0], featureset[1], marker="x",
#                     color=color, linewidths=5)
# plt.show()
# to normalizate the data