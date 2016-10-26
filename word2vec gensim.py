import gensim, logging, os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

sentences = MySentences('F:\\Corpus\\TextCorpus\\subset\\') # a memory-friendly iterator
model = gensim.models.Word2Vec(sentences, size=300, sg=1, min_count=10, iter=10, window=5, workers=16)
