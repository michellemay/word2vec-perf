# word2vec-perf
Compare words/s for spark, gensim and original word2vec.


# Setup
- Windows 7, dual opteron 6272 (2x 16 cores), 32 GB ram.

# Dataset
http://mattmahoney.net/dc/enwik9.zip

# word2vec
Running: `word2vec -threads 16 -train enwik9 -iter 10 -min-count 10 -output testvecs.txt --cbow 0`

```
```


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
...
2016-10-26 14:44:29,252 : INFO : PROGRESS: at 12.37% examples, 101454 words/s, in_qsize 0, out_qsize 0
...
2016-10-26 15:05:46,543 : INFO : PROGRESS: at 26.08% examples, 102286 words/s, in_qsize 0, out_qsize 0
~~~~

As seen in the logs, speed is **102 kwords/s**


# Spark
Running Spark 2.0.1: `spark-shell.cmd --master local[16] --driver-memory 20G`

Sample output:
~~~~
16/10/26 15:08:09 INFO Word2Vec: vocabSize = 458191, trainWordsCount = 138847698
16/10/26 15:10:06 INFO Word2Vec: wordCount = 10018, alpha = 0.024971139600952263
...
16/10/26 15:15:18 INFO Word2Vec: wordCount = 993069, alpha = 0.022139112834703874
16/10/26 15:15:18 INFO Word2Vec: wordCount = 1004216, alpha = 0.02210699995107589
16/10/26 15:15:18 INFO Word2Vec: wordCount = 1003880, alpha = 0.022107967918143175
16/10/26 15:15:19 INFO Word2Vec: wordCount = 1003081, alpha = 0.02211026972078234
16/10/26 15:15:19 INFO Word2Vec: wordCount = 993076, alpha = 0.022139092668723305
~~~~

Interesting to see that gensim and spark does not see the same number of words!
Since I'm using with 16 partitions, each one sees about 8.7M words.

Approximate speed is 16 threads * 3208 w/s ~= **51 kwords/s**

# Results

|          | kwords/s | total time |
| ---      | ---:     | ---:       |
|word2vec  |          |            |
|gensim    | 102      |            |
|spark     | 51       |            |
