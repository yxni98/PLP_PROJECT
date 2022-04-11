import logging
import gensim.downloader as api
from gensim.models.word2vec import Word2Vec
import re
import taining_data_generate as dg

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


#corpus = api.load('text8')


#model = Word2Vec(corpus, min_count=3, vector_size=300)

#model.save('word2vec_text8.model')  # 保存模型


#model = Word2Vec.load('word2vec_text8.model')  # 加载模型
#print("model loaded!!")

dataset=dg.get_dataset()

model = Word2Vec(dataset, min_count=1, vector_size=300)

#model.train(dataset, total_examples=len(dataset), epochs=3)

f = open('val.xml', 'r', encoding = 'utf-8')
data = f.read()
f.close()

orig_terms = re.findall(r'term=\"(.*?)\"', data)
i=0
j=0
for t in orig_terms:
	try:
		vec_t = model.wv[t]
		i=i+1
	except KeyError:
		#print("The word '",t,"' does not appear in this model")
		j=j+1
print("valid:	",i)
print("invalid:	",j)

model.save('word2vec_1w.model')
