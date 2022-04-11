import spacy
import pickle5
import extract
import numpy as np

import re
from string import punctuation
def preprocess_English(content):
    train_data = []
    for word in content:
        word = re.sub(r'[{}]+'.format(punctuation),' ',word)
        train_data.append(word)
    return train_data



def get_dataset(filename='select_reviews.pkl'):
	with open(filename, 'rb') as f:
		re_dict=pickle5.load(f)
		reviews=re_dict['reviews']

	nlp = spacy.load("en_core_web_sm")
	dataset=[]
	print("start data process!!")

	reviews=preprocess_English(reviews)
	print("preprocess ready!!")

	for i,rev in enumerate(reviews):
		print(i)
		if i%10000==0:
			print(i)
		temp1=[]
		doc=nlp(rev)
		for ent in doc.ents:
			temp1.append(ent.text)
		#print("NER:	",temp1)
		try:
			ners=extract.output_sentence( rev, temp1 )
			dataset.append( ners )
			#print("check No. :  ", i)
			#print(ners)
			#print()
		except IndexError:
			print("The sent ",i," does not work")
			#print()
	print("dataset ready!!")
	ddd=np.array(dataset)
	np.save("ddd.npy",ddd)
	print("saved!!")
	return dataset








