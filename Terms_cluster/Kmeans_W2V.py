import numpy as np
import re
import Kmeans_Algo
import gensim.downloader as api
from gensim.models import KeyedVectors



def k_Cluster(orig_terms=[],added_attr=None):

	pre_attr=["power","screen","look","system","quality"]
	word_cluster={}			#词典

	''' '''
	#wv = api.load('word2vec-google-news-300')
	wv=KeyedVectors.load('word_vector', mmap='r')

	terms=list(set(orig_terms))

	embeddings=[]		#词向量
	words=[]			#去重后的词列表
	pre_attr_vec=[]		#预定义类别的词向量

	for attr in pre_attr:		#词映射
		try:
			vec_t = wv[attr]
			pre_attr_vec.append(vec_t)
		except KeyError:
			print("The word '",attr,"' does not appear in this model")

	for word in terms:
		try:
			vec_t = wv[word]
			embeddings.append(vec_t)
			words.append(word)
		except KeyError:
			print("The word '",word,"' does not appear in this model")
			word_cluster[word]="Invalid"

	#------------------------------------------------------------
	#处理用户自定义输入 added_attr
	if added_attr!=None:
		try:
			vec_a = wv[added_attr]
			mind=float("inf")
			maxd=-1
			tar=None
			for i,p in enumerate(pre_attr):
				if Kmeans_Algo.distEclud(vec_a, wv[p])<mind:
					mind=Kmeans_Algo.distEclud(vec_a, wv[p])
					tar=i
				if Kmeans_Algo.distEclud(vec_a, wv[p])>maxd:
					maxd=Kmeans_Algo.distEclud(vec_a, wv[p])

			if mind*2<maxd:		#距离太近则合并b
				pre_attr[tar]+=str("("+added_attr+")")

			else:				#距离够远则单独成一类
				pre_attr.append(added_attr)
				pre_attr_vec.append(vec_a)
			#pre_attr_vec.append(vec_t)
		except KeyError:
			print("The word '",added_attr,"' does not appear in this model")	
			return str("UNDEFINED")	
	#------------------------------------------------------------

	#print(len(embeddings))
	np.save("embeddings.npy",embeddings)
	np.save("words.npy",words)
	np.save("pre_attr_vec.npy",pre_attr_vec)

	''' '''

	embeddings=np.load("embeddings.npy")
	words=np.load("words.npy")
	pre_attr_vec=np.load("pre_attr_vec.npy")

	#print(len(pre_attr_vec))

	centroids, y=Kmeans_Algo.kMeans(embeddings,len(pre_attr),pre_attr_vec)		#聚类核心函数，以pre_attr_vec为初始聚类核心

	y=y[:,0]		#不需要最小距离
	y=y.astype(int)

	f = open('clusters-6_W2V.txt', 'w', encoding = 'utf-8')
	z=list(zip(y,words))
	z.sort(key=lambda x: x[0], reverse=False)		#按类排序，方便看效果

	y,words=zip(*z)


	mapp=np.empty( len(pre_attr)+1 )		#聚类中心与属性词的对应关系
	for n,m in enumerate(mapp):
		mapp[n]=-2

	for i,vec in enumerate(pre_attr_vec):
		#print(i)
		min_index=-1
		min_dis=float("inf")
		for j,cent in enumerate(centroids):
			dis=Kmeans_Algo.distEclud(vec,cent)
			if(dis<min_dis and mapp[j]==-2):
				min_dis=dis
				min_index=j
		mapp[min_index]=i
		#print(min_index)


	for a,b in zip(words,y):
		f.write(str(a))
		f.write("	:			")
		f.write(str( pre_attr[ int(mapp[b]) ] ))
		f.write('\n')
		word_cluster[str(a)]=str( pre_attr[ int(mapp[b]) ] )
	f.close()

	cluster_list=[]			#按原顺序返回
	for t in orig_terms:
		cluster_list.append( word_cluster[t] )

	return cluster_list


#---------------------------------------------------------------------------------------




