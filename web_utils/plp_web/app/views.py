from django.shortcuts import render
from django.utils.html import escape
from django.http import HttpResponse
from app.models import Product
import time
import os
import shutil
import json

from amazon_search import return_amazon_reviews
from match_reviews_reddit import return_review_from_reddit
from Terms_cluster.Kmeans_W2V import k_Cluster
from Aspect_Term_Extraction.updateterm import get_terms
from core_model.sentiment_output import return_sentiment_output
from my_wordcloud import save_wordcloud
from my_histogram import draw_histogram
from my_report import statistics

def get_sorted_terms(term_list_1D):
	term_count = {}
	for term in term_list_1D:
		if term not in term_count.keys():
			term_count[term] = 1
		else:
			term_count[term] += 1
	sorted_terms = sorted(term_count.items(), key=lambda x: x[1], reverse=True)
	return sorted_terms

# Create your views here.
def index(request):
    return render(request, 'index.html')

def generate_result(platform, product, reviews, customed_category, products, timestamp):
		
	for i in range(len(reviews)):
		reviews[i] = reviews[i].lower()
	terms = get_terms(reviews)
	sentiment_list_1D = return_sentiment_output(platform, reviews, terms)
	term_list_1D = []
	for _list in terms:
		for term in _list:
			term_list_1D.append(term)
	if customed_category != 'customed_category' and len(customed_category)>0:
		category_list_1D  = k_Cluster(term_list_1D, customed_category)
	else:
		category_list_1D  = k_Cluster(term_list_1D)

	sorted_terms = get_sorted_terms(term_list_1D)
	top_terms = [x[0] for x in sorted_terms[:16]]
	save_wordcloud(top_terms, product, platform) 

	categories = list(set(category_list_1D))
	positive = [0]*len(categories)
	neutral = [0]*len(categories)
	negative = [0]*len(categories)
	print(len(category_list_1D))
	print(len(sentiment_list_1D))
	for i in range(len(category_list_1D)):
		try:
			sentiment = sentiment_list_1D[i]
			category = category_list_1D[i]
			index = categories.index(category)
			if sentiment == 0:
				positive[index] += 1
			elif sentiment == 1:
				negative[index] += 1
			elif sentiment == 2:
				neutral[index] += 1
		except Exception as e:
			continue
		
	draw_histogram(positive, neutral, negative, categories, product, platform)

	if len(products)== 0:
		if platform == 'amazon':
			Product.objects.create(_name=product, _time=timestamp, _amazon_term_list_1D='-**-'.join(term_list_1D), \
			 _amazon_category_list_1D='-**-'.join(category_list_1D), _amazon_sentiment_list_1D='-**-'.join([str(x) for x in sentiment_list_1D]), \
			 _reddit_term_list_1D=' ', _reddit_category_list_1D=' ', \
			 _reddit_sentiment_list_1D=' ') 
		else:
			Product.objects.create(_name=product, _time=timestamp, _amazon_term_list_1D=' ', \
			 _amazon_category_list_1D=' ', _amazon_sentiment_list_1D=' ', \
			 _reddit_term_list_1D='-**-'.join(term_list_1D), _reddit_category_list_1D='-**-'.join(category_list_1D), \
			 _reddit_sentiment_list_1D='-**-'.join([str(x) for x in sentiment_list_1D])) 
	else:
		products[0]._name = product
		products[0]._time = timestamp
		if platform == 'amazon':
			products[0]._amazon_term_list_1D = '-**-'.join(term_list_1D)
			products[0]._amazon_category_list_1D = '-**-'.join(category_list_1D)
			products[0]._amazon_sentiment_list_1D = '-**-'.join([str(x) for x in sentiment_list_1D]) 
		else:	
			products[0]._reddit_term_list_1D = '-**-'.join(term_list_1D)
			products[0]._reddit_category_list_1D = '-**-'.join(category_list_1D)
			products[0]._reddit_sentiment_list_1D = '-**-'.join([str(x) for x in sentiment_list_1D])
		products[0].save()

	if platform == 'amazon':
		shutil.copyfile('D:/plp_project/web_utils/plp_web/app/static/images/'+product+'_'+platform+'_wordcloud.jpg', 'D:/plp_project/web_utils/plp_web/app/static/images/1.jpg')
		shutil.copyfile('D:/plp_project/web_utils/plp_web/app/static/images/'+product+'_'+platform+'_histogram.jpg', 'D:/plp_project/web_utils/plp_web/app/static/images/2.jpg')
	else:
		shutil.copyfile('D:/plp_project/web_utils/plp_web/app/static/images/'+product+'_'+platform+'_wordcloud.jpg', 'D:/plp_project/web_utils/plp_web/app/static/images/3.jpg')
		shutil.copyfile('D:/plp_project/web_utils/plp_web/app/static/images/'+product+'_'+platform+'_histogram.jpg', 'D:/plp_project/web_utils/plp_web/app/static/images/4.jpg')

	return term_list_1D, category_list_1D, sentiment_list_1D

def analyse_result(request):
	try:
		os.remove('D:/plp_project/web_utils/plp_web/app/static/images/1.jpg')
		os.remove('D:/plp_project/web_utils/plp_web/app/static/images/2.jpg')
		os.remove('D:/plp_project/web_utils/plp_web/app/static/images/3.jpg')
		os.remove('D:/plp_project/web_utils/plp_web/app/static/images/4.jpg')
		os.remove('D:/plp_project/web_utils/plp_web/app/static/images/5.jpg')
	except Exception as e:
		pass
	
	product = escape(request.GET["product"])
	customed_category = escape(request.GET["customed_category"])

	product = product.lower()

	timestamp = int(time.time())
	
	match_product_name = product
	products = Product.objects.filter(_name=match_product_name)
	query_tag = 0
	if len(products) > 0:
		query_result = products[0].get_attributes()
		last_time = query_result[1]
		if (last_time - timestamp) <= 86400: # no more that 1 day
			query_tag = 1
	
	for i in Product.objects.all():
		if i.get_attributes()[0] == 'sony headphone':
			print('delete')
			i.delete()


	platform = 'amazon'
	if query_tag == 1:
		shutil.copyfile('D:/plp_project/web_utils/plp_web/app/static/images/'+product+'_'+platform+'_wordcloud.jpg', 'D:/plp_project/web_utils/plp_web/app/static/images/1.jpg')
		shutil.copyfile('D:/plp_project/web_utils/plp_web/app/static/images/'+product+'_'+platform+'_histogram.jpg', 'D:/plp_project/web_utils/plp_web/app/static/images/2.jpg')
	else:
		reviews = return_amazon_reviews(product)
		for i in range(len(reviews)):
			reviews[i] = reviews[i].replace('<','').replace('>','')
		amazon_reviews = reviews
		amazon_term_list, amazon_category_list, amazon_sentiment_list = generate_result(platform, product, reviews, customed_category, products, timestamp)

	platform = 'reddit'
	if query_tag == 1:
		shutil.copyfile('D:/plp_project/web_utils/plp_web/app/static/images/'+product+'_'+platform+'_wordcloud.jpg', 'D:/plp_project/web_utils/plp_web/app/static/images/3.jpg')
		shutil.copyfile('D:/plp_project/web_utils/plp_web/app/static/images/'+product+'_'+platform+'_histogram.jpg', 'D:/plp_project/web_utils/plp_web/app/static/images/4.jpg')
	else:
		reviews = return_review_from_reddit(product)
		for i in range(len(reviews)):
			reviews[i] = reviews[i].replace('<','').replace('>','')
		reddit_reviews = reviews
		reddit_term_list, reddit_category_list, reddit_sentiment_list = generate_result(platform, product, reviews, customed_category, products, timestamp)
	
	if query_tag == 0:
		write_dict = {'amazon_reviews':amazon_reviews,'reddit_reviews':reddit_reviews,'amazon_term_list':amazon_term_list,'amazon_category_list':amazon_category_list,'amazon_sentiment_list':amazon_sentiment_list,'reddit_term_list':reddit_term_list,'reddit_category_list':reddit_category_list,'reddit_sentiment_list':reddit_sentiment_list}
		js = json.dumps(write_dict)
		file = open(product+'.txt', 'w+')
		file.write(js)
		file.close()
		statistics(product, amazon_term_list, amazon_category_list, amazon_sentiment_list, reddit_term_list, reddit_category_list, reddit_sentiment_list)

	shutil.copyfile('D:/plp_project/web_utils/plp_web/app/static/images/'+product+'_platform_comparison.jpg', 'D:/plp_project/web_utils/plp_web/app/static/images/5.jpg')

	return render(request, 'result.html', {'product_name':match_product_name})