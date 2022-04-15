import spacy, json, pickle
from pprint import pprint
from spacy import displacy
from collections import Counter
from summarizer import Summarizer, TransformerSummarizer
import numpy as np
import networkx as nx
import en_core_web_lg
nlp = en_core_web_lg.load()

# rendering
asin_2_title_brand_categories = {} # "title" is the specific name of product
for line in open('meta_Electronics.json', 'r', encoding = 'utf-8'):
	data_dict = json.loads(line)
	asin = data_dict['asin']
	title = data_dict['title']
	brand = data_dict['brand']
	categories = data_dict['category']
	asin_2_title_brand_categories[asin] = (title, brand, categories)

asin_2_rating_review = {}
for line in open('Electronics.json', 'r', encoding = 'utf-8'):
	data_dict = json.loads(line)
	asin = data_dict['asin']
	try:
		rating = data_dict['overall']
		review = data_dict['reviewText']
		if asin not in asin_2_rating_review.keys():
			asin_2_rating_review[asin] = [(rating, review)]
		else:
			asin_2_rating_review[asin].append((rating, review))
	except Exception as e:
		continue

with open('amazon_process_pairs.pkl', 'wb') as f:
	pickle.dump(asin_2_title_brand_categories, f, pickle.HIGHEST_PROTOCOL)
	pickle.dump(asin_2_rating_review, f, pickle.HIGHEST_PROTOCOL)

# reading
with open('amazon_process_pairs.pkl', 'rb') as f:
	asin_2_title_brand_categories = pickle.load(f) # {ID : (title, brand, categories)}, where "categories" is a list, others are strings.
	asin_2_rating_review = pickle.load(f) # {ID : [(rating1, review1), (rating2, review2), ...]}

# bert_model = Summarizer()

# test for one product
for asin in asin_2_rating_review.keys():
	title_brand_categories = asin_2_title_brand_categories[asin]
	categories = title_brand_categories[-1]
	digital_tag = 0
	for category in categories:
		if 'digital' in category.lower():
			digital_tag = 1
	if digital_tag == 1:
		print('title brand categories')
		print(title_brand_categories)
		for rating_review in asin_2_rating_review[asin]:
			rating = rating_review[0]
			review = rating_review[1]
			print('********************************')
			print(rating)
			print(review)
			# summary = ''.join(bert_model(review, min_length=2))
			# print(summary)
			doc = nlp(review)
			pprint([(X.text, X.label_) for X in doc.ents])
		break



# result (the targeted product is the CANON camera)
'''
title brand categories
('Canon EF 24-105mm f/4L IS USM Lens Bundle International Version (No Warranty)', 'Canon', ['Electronics', 'Camera & Photo', 'Accessories', 'Digital Camera Accessories', 'Accessory Kits'])
********************************
5.0
Outstanding pictures...
A kind of heavy but the pictures are unique.
[]
********************************
5.0
This lens is versatile and fast. I used it successfully indoors and outdoors to get great shots.
[]
********************************
5.0
Got everything as advertised. Lens works fine. Good value.
[('Lens', 'PERSON')]
********************************
5.0
I've been really enjoying this lens for both photo and video work. The glass is exceptional and it works like a dream. I appreciated all the extra items included in the kit, as well.
[]
********************************
5.0
This is an excellent all around lens.  Sharp and fast enough for most situations.
[]
********************************
5.0
Very good lens recommended!!
[]
********************************
5.0
Just open, looks great! Looking forward to the pictures I will take
[]
********************************
5.0
I am not a pro by any stretch of the imagination.  I do have a number of other lenses, including some Canon primes.  I purchased this to see if it would outdo my Tamron zoom.  Conclusively the answer is Yes.  I am completely satisfied with the image sharpness and I believe the best feature is the Image Stablization.  The IS feature alone improved my shots immensely at a wide range of apertures, and gives me a far higher percentage of "keepers" than I ever had before.  I am completely satisfied with the effects possible on my 60D body and it is full frame ready for when I upgrade.  Recommended if you can afford it.
[('Canon', 'PRODUCT'), ('Tamron', 'ORG'), ('the Image Stablization', 'ORG')]
********************************
5.0
I matched this lens with my L glass canon 100-400 and it represents a travel kit that will provide high quality images.
[('100-400', 'CARDINAL')]
********************************
5.0
This was a gift for my son.  He was very excited to get it and appreciated all the extras that came with it. It was a good price compared to some of the other options on Amazon.
[('Amazon', 'ORG')]
********************************
4.0
Great lens--it lives up to the Canon "L" lens hype. .The image stabilization feature on the 24-105 allows you to shoot photos at a slower shutter speed in dark situations since the fastest this lens goes is F4. The IS feature  is really amazing and incredibly useful for shooting video. Adobe Lightroom helps fix some of the distortion on the wide end. The extras included in this package are okay but should not be the deciding factor in getting the lens. The bonus Digital Ultraviolet HD UV filter I received seemed really low-quality in terms of construction as I was never able to mount it on the lens since I was afraid to damage the threads on the lens.
[('Canon', 'PRODUCT'),
 ('24', 'CARDINAL'),
 ('Adobe', 'ORG'),
 ('Digital Ultraviolet HD UV', 'ORG')]
********************************
5.0
This lens is highly recommended for anyone who wants a great quality lens and ease of use for portrait photography. I have other lenses for my Canon camera, but this is my go to lens.
[('Canon', 'PRODUCT')]
********************************
5.0
I love this lense!
[]
********************************
5.0
This lens is the perfect all purpose lens for my Canon 5D Mark II camera. The detail and functioning ...perfect!
[('Mark II', 'PERSON')]
********************************
5.0
Excellent
[]
********************************
5.0
I am so thankful I made this purchase and so are my portrait clients who are benefiting!!!
[]
********************************
5.0
Very sharp lens
[]
********************************
5.0
I have taken some great pics with this lens, so clear, it is a bit heavy, but I kinda like it, because I seem to steady it better. I would recommend this lens.
[]
********************************
5.0
I need to use it a bit more, but so far so good. My lens did not include a warranty card, so I'm guessing the warranty is through the manufacturer, which does not appear to be Canon.
[('Canon', 'PRODUCT')]
********************************
5.0
This is a great lens! It has become my "workhorse". We shoot indie films, corporate videos and PSAs and this has been my go-to piece of glass. It gives a very sharp picture and we're able to get very wide shots in smaller areas. Definitely glad I purchased it!
[]
********************************
1.0
Originally the lens worked well. It hasn't been even a year though, and it stopped working. I don't think it's an issue with Canon, I think it's an issue with this specific seller. The issue I'm having is that one day it was perfect then the next day it won't focus and it feels as if something is loose. I think one of the pieces of glass feel out in the lens which shouldn't happen. It was never dropped and was always left in good conditions. Spending that much money should guarantee that the product will last more than a year, a lot more.
[('Canon', 'PRODUCT'), ('the next day', 'DATE'), ('more than a year', 'DATE')]
'''
