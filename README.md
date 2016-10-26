# word2vec-perf
Compare kwords/s speed for spark, gensim and original word2vec. (Quick and dirty benchmark)


# Setup
- Windows 7, dual opteron 6272 (2x 16 cores), 32 GB ram
  - NOT using GPU
  - *I'm using only 16 threads in my tests to allow my workstation to still be responsive.*
- Settings: skipgram, window=5, iter=10, min_count=10, 16 threads
- Time to read file is not taken into account.
  - spark and gensim reprocess text content at each iteration. (I assume the content will eventually be bigger than memory)
  - spark takes about 13 GB of memory to cache enwik9 content in RDD (!!!)
  - word2vec cache the content in memory giving it an unfair advantage over the others.

# Dataset
http://mattmahoney.net/dc/enwik9.zip

# word2vec
Running: `word2vec -threads 16 -train enwik9 -iter 10 -min-count 10 -output testvecs.txt --cbow 0`

```
Starting training using file enwik9
Vocab size: 458277
Words in train file: 129756040
Alpha: 0.047401  Progress: 5.20%  Words/thread/sec: 1301.62k
...
Alpha: 0.037308  Progress: 25.39%  Words/thread/sec: 1329.74k
```
As seen in the logs, speed is should be 16 threads * 1329.74k ~= **21275** kwords/s.
However, this number does not add up with percentages and total number of words!

More realistic timing is: 5% * 129756040 words takes about 47 seconds ~= **138 kwords/s**

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
...
2016-10-26 15:45:09,621 : INFO : PROGRESS: at 52.53% examples, 103708 words/s, in_qsize 0, out_qsize 0
~~~~

As seen in the logs, speed is **103 kwords/s**. However, this does not add up.
According to percentages, this should be 5% * 129347859 words takes about 460 seconds ~= **14 kwords/s**


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

Since I'm using with 16 partitions, each one sees about 8.7M words.

Approximate speed is 16 threads * 3208 w/s ~= **51 kwords/s**

# Results

|          | kwords/s | total time | total words |
| ---      | ---:     | ---:       | ---:        |
|word2vec  | 138      |            | 129756040   | * unfair advange of data being already in memory
|gensim    | 14       |            | 129347859   |
|spark     | 51       |            | 138847698   |

** Interesting to see that none of the tools sees the same number of words with spark being way out!**
