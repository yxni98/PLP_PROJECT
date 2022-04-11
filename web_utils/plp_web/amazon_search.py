from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

def token_clean(title, is_search=False):
	tokens= word_tokenize(title)
	res = []
	for t in tokens:
		if len(t) ==1 and not is_search: # remove single symbol/char
			continue
		tar = t.lower().replace('-','')
		if not tar in res and not tar=='amp' and not tar =='sww' and not tar=='swi': # remove 'amp', an unknown error char 
			res.append(tar)
	return res


# query: the user's input string; product_list:{ID : (title, brand, categories->list[],tokenized_title,summary)->list[]}; Top N: the num of items for selection
def search(query, product_list, reviews, topN = 3):
	max_review = 0  
	qs = token_clean(query, True)
	res = []
	expected = max(int(len(qs)/2),1)
	for asin in product_list.keys():
		flag = 0
		for q in qs:
			if not q in product_list[asin][0].lower():
				flag += 1
		if flag > len(qs)-expected: # eliminate if hits less than half
			continue
		else:
			f_score = 0
			s_score = 0
			t_score = len(qs)/len(product_list[asin][0].split(' '))
			search_criteria = token_clean(product_list[asin][-1])
			l = len(search_criteria)
			for q in qs:
				if q in search_criteria:
					f_score+=1
				else:
					if q in product_list[asin][-2]:
						f_score+=0.2 *t_score
			# if not product_list[asin][1].lower() in qs and product_list[asin][1].lower() in search_criteria:
			# 	f_score+=1
			try:
				s_score = (f_score/l) *10
			except:
				print(product_list[asin])
				s_score = 0
			f_score = f_score*10
			try:
				review_num = len(reviews[asin])
			except:
				review_num = 0
			max_review = max(review_num, max_review)
			# res.append({'asin':asin, 'score':s_score+f_score+t_score, 'title':product_list[asin][0], 'sum':product_list[asin][-1], 'cate':product_list[asin][2][-1], 'brand':product_list[asin][1]})
			res.append({'asin':asin, 'score':s_score+f_score+t_score, 'title':product_list[asin][0], 'reviews':review_num, 'sum':product_list[asin][-1]})

	if len(res) < topN:
		return res
	else:
		res = sorted(res, key = lambda x: x['reviews'], reverse=True)
		res1 = res[0:min(int(len(res)/10),200)]
		res1 = sorted(res1, key = lambda x: x['score'], reverse=True)
		print('max_review nums:'+str(max_review))
		print(len(res1))
		return res1[0: topN]


if __name__ == "__main__":
    import pickle
    target_pkl = 'amazon_electronics_meta.pkl'
    review_pkl = 'all_matched_reviews.pkl'
    with open(target_pkl, 'rb') as f:
        asin_2_title_brand_categories = pickle.load(f) # {ID : (title, brand, categories, tokenized title, summarization)}, where "categories" is a list, others are strings.

    with open(review_pkl, 'rb') as f:
       reviews = pickle.load(f) # {ID : (title, brand, categories, tokenized title, summarization)}, where "categories" is a list, others are strings.

    while True:
        s = input('search item, end with 0:')
        if s == '0':
            break

        else:
            print(search(s, asin_2_title_brand_categories,reviews))
