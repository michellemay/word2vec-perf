# word2vec-perf
Compare words/s for spark, gensim and original word2vec.


# Setup
- Windows 7, dual opteron 6272 (2x 16 cores), 32 GB ram.

# Dataset
http://mattmahoney.net/dc/enwik9.zip

# Spark
Running Spark 2.0.1: `spark-shell.cmd --master local[16] --driver-memory 20G`

Sample output:
~~~~
16/10/26 14:10:08 INFO Word2Vec: wordCount = 10023, alpha = 0.02495488311981317
...
16/10/26 14:14:08 INFO Word2Vec: wordCount = 1003170, alpha = 0.020484395819912005
...
16/10/26 14:34:59 INFO Word2Vec: wordCount = 5565869, alpha = 2.5E-6
~~~~

# gensim
Running python 2.7 on Anaconda (gensim 0.13.3)

Sample output:
~~~~
2016-10-26 14:23:35,756 : INFO : collected 8859143 word types from a corpus of 129347859 raw words and 13147026 sentences
2016-10-26 14:23:35,756 : INFO : Loading a fresh vocabulary
2016-10-26 14:24:12,579 : INFO : min_count=10 retains 458259 unique words (5% of original 8859143, drops 8400884)
2016-10-26 14:24:12,581 : INFO : min_count=10 leaves 116608081 word corpus (90% of original 129347859, drops 12739778)
2016-10-26 14:24:16,654 : INFO : deleting the raw counts dictionary of 8859143 items
2016-10-26 14:24:18,130 : INFO : sample=0.001 downsamples 30 most-common words
2016-10-26 14:24:18,130 : INFO : downsampling leaves estimated 94622432 word corpus (81.1% of prior 116608081)
2016-10-26 14:24:18,131 : INFO : estimated required memory for 458259 words and 300 dimensions: 1328951100 bytes
2016-10-26 14:24:21,825 : INFO : resetting layer weights
2016-10-26 14:24:44,115 : INFO : training model with 16 workers on 458259 vocabulary and 300 features, using sg=1 hs=0 sample=0.001 negative=5 window=5
2016-10-26 14:24:44,115 : INFO : expecting 13147026 sentences, matching count from corpus used for vocabulary survey
2016-10-26 14:24:45,427 : INFO : PROGRESS: at 0.00% examples, 5933 words/s, in_qsize 24, out_qsize 0
2016-10-26 14:24:46,569 : INFO : PROGRESS: at 0.01% examples, 61154 words/s, in_qsize 14, out_qsize 1
2016-10-26 14:24:47,568 : INFO : PROGRESS: at 0.02% examples, 76068 words/s, in_qsize 10, out_qsize 0
2016-10-26 14:24:48,608 : INFO : PROGRESS: at 0.03% examples, 80037 words/s, in_qsize 13, out_qsize 2
2016-10-26 14:24:49,691 : INFO : PROGRESS: at 0.04% examples, 84316 words/s, in_qsize 5, out_qsize 1
2016-10-26 14:24:50,667 : INFO : PROGRESS: at 0.05% examples, 85619 words/s, in_qsize 0, out_qsize 1
2016-10-26 14:24:52,029 : INFO : PROGRESS: at 0.06% examples, 86184 words/s, in_qsize 0, out_qsize 0
2016-10-26 14:24:53,124 : INFO : PROGRESS: at 0.07% examples, 88264 words/s, in_qsize 0, out_qsize 0
2016-10-26 14:24:54,104 : INFO : PROGRESS: at 0.08% examples, 90871 words/s, in_qsize 0, out_qsize 0
...
2016-10-26 14:44:29,252 : INFO : PROGRESS: at 12.37% examples, 101454 words/s, in_qsize 0, out_qsize 0
~~~~
