# word2vec-perf
Compare kwords/s speed for spark, gensim and original word2vec. (Quick and dirty benchmark)


# Setup
- Windows 7, dual opteron 6272 (2x 16 cores), 32 GB ram
  - NOT using GPU
  - *I'm using only 16 threads in my tests to allow my workstation to still be responsive.*
- Settings: skipgram, window=5, iter=10, min_count=10, 16 threads

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
As seen in the logs, speed is **1330 kwords/s.**

*Note, word2vec is running all the iterations in the same progress bar.*

### word2vec-fastload ###
Reading file and building vocabulary is unexpectedly slow here (~38m). Due to the inneficiencies of fgetc and ungetc on Windows.

A modified version with simple buffering leads to significant performance gain: 35s instead of 38 minutes!

See word2vec.c and word2vec-fastload.exe

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
Running Spark 2.0.1: 
`spark-shell.cmd --master local[16] --driver-memory 20G --conf spark.kryoserializer.buffer.max=1G  --conf spark.driver.maxResultSize=2G`

Sample output:
~~~~
Start at 20:37:00
16/10/26 20:38:24 INFO Word2Vec: vocabSize = 458191, trainWordsCount = 138847698
16/10/26 20:40:09 INFO Word2Vec: wordCount = 10016, alpha = 0.024942290725321996
16/10/26 20:40:09 INFO Word2Vec: wordCount = 10016, alpha = 0.024942290725321996
16/10/26 20:40:09 INFO Word2Vec: wordCount = 10007, alpha = 0.0249423425807006
16/10/26 20:40:09 INFO Word2Vec: wordCount = 10095, alpha = 0.024941835550332025
16/10/26 20:40:09 INFO Word2Vec: wordCount = 10010, alpha = 0.0249423252955744
...
16/10/26 20:44:16 INFO Word2Vec: wordCount = 1013061, alpha = 0.01916303758840109
16/10/26 20:44:16 INFO Word2Vec: wordCount = 1003254, alpha = 0.019219542665953725
16/10/26 20:44:16 INFO Word2Vec: wordCount = 1013469, alpha = 0.019160686811237688
16/10/26 20:44:17 INFO Word2Vec: wordCount = 1014371, alpha = 0.019155489749959776
16/10/26 20:44:17 INFO Word2Vec: wordCount = 1003549, alpha = 0.019217842961877243
16/10/26 20:44:17 INFO Word2Vec: wordCount = 1023743, alpha = 0.019101491015706355
...
16/10/27 00:38:48 INFO Word2Vec: wordCount = 4334069, alpha = 2.8356789693720352E-5
model: org.apache.spark.mllib.feature.Word2VecModel = org.apache.spark.mllib.feature.Word2VecModel@778e3cfb
Done at 00:54:08
~~~~

Since I'm using with 32 partitions, each one sees about 4.3M words.

Approximate [spontaneous] speed is 16 threads * 4077 w/s ~= **65 kwords/s**

# Results

|          | kwords/s | training time   | total time     | total words |
| ---      | ---:     | ---:            | ---:           | ---:        |
|word2vec  | 1330     | 980s (0.27h)    | 1015s (0.28h)  | 129756040   |
|gensim    | 104      | 9016s (2.50h)   | 9422s (2.62h)  | 129347859   |
|spark     | 65       | 14424s (4.00h)  | 15428s (4.29h) | 138847698   |

** Interesting to see that none of the tools sees the same number of words with spark being way out!**
