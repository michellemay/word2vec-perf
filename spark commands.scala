import org.apache.spark.mllib.feature._
val inputText = "enwik9"
val input = sc.textFile(inputText).map(line => line.split(" ").toSeq)
val word2vec = new Word2Vec().setMinCount(10).setNumIterations(10).setVectorSize(300).setNumPartitions(32)
val model = word2vec.fit(input)
