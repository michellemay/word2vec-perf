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
As seen in the logs, speed is **1330 kwords/s**
*Note, word2vec seems to be running all iterations in the same progress bar.*

# gensim
Running python 2.7 on Anaconda (gensim 0.13.3)

Sample output:
~~~~
2016-10-26 14:17:59,470 : INFO : collecting all words and their counts
2016-10-26 14:17:59,471 : INFO : PROGRESS: at sentence #0, processed 0 words, keeping 0 word types
2016-10-26 14:17:59,586 : INFO : PROGRESS: at sentence #10000, processed 113372 words, keeping 31659 word types
...
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
...
2016-10-26 16:22:48,619 : INFO : PROGRESS: at 77.75% examples, 104303 words/s, in_qsize 0, out_qsize 1
...
2016-10-26 16:55:01,194 : INFO : PROGRESS: at 99.98% examples, 104921 words/s, in_qsize 0, out_qsize 0
2016-10-26 16:55:01,990 : INFO : training on 1293478590 raw words (946227620 effective words) took 9018.1s, 104926 effective words/s
~~~~

As seen in the logs, speed is **104 kwords/s**.  (946227620 effective words after downsampling and multiple iterations)

# Spark
Running Spark 2.0.1: `spark-shell.cmd --master local[16] --driver-memory 20G --conf spark.kryoserializer.buffer.max=1G`

Sample output:
~~~~
16/10/26 19:42:25 INFO Word2Vec: vocabSize = 458191, trainWordsCount = 138847698
16/10/26 19:44:16 INFO Word2Vec: wordCount = 10016, alpha = 0.024942290725321996
16/10/26 19:44:16 INFO Word2Vec: wordCount = 10001, alpha = 0.024942377150953002
...
16/10/26 19:48:22 INFO Word2Vec: wordCount = 1003098, alpha = 0.0192204414925162
16/10/26 19:48:22 INFO Word2Vec: wordCount = 1003704, alpha = 0.0192169498970235
16/10/26 19:48:22 INFO Word2Vec: wordCount = 1003059, alpha = 0.01922066619915682
16/10/26 19:48:22 INFO Word2Vec: wordCount = 1003422, alpha = 0.01921857469888644
16/10/26 19:48:22 INFO Word2Vec: wordCount = 1003882, alpha = 0.01921592431286888
16/10/26 19:48:22 INFO Word2Vec: wordCount = 1003653, alpha = 0.01921724374416893
...
~~~~

Since I'm using with 32 partitions, each one sees about 4.3M words.

Approximate speed is 16 threads * 4077 w/s ~= **65 kwords/s**

# Results

|          | kwords/s | training time | total words |
| ---      | ---:     | ---:          | ---:        |
|word2vec  | 1330     | 16:20         | 129756040   | * unfair advange of data being already in memory
|gensim    | 104      |               | 129347859   |
|spark     | 65       |               | 138847698   |

** Interesting to see that none of the tools sees the same number of words with spark being way out!**
