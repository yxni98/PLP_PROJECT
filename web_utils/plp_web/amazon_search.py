from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

def token_clean(title):
	tokens= word_tokenize(title)
	res = []
	for t in tokens:
		
		if len(t) ==1: # remove single symbol/char
			continue
		tar = t.lower().replace('-','')
		if not tar in res and not tar=='amp' and not tar =='sww' and not tar=='swi': # remove 'amp', an unknown error char 
			res.append(tar)
	return res


# query: the user's input string; product_list:{ID : (title, brand, categories->list[],tokenized_title,summary)->list[]}; Top N: the num of items for selection
def search(query, product_list, topN = 3):  
	qs = token_clean(query)
	res = []
	expected = max(int(len(qs)/2),1)
	for asin in product_list.keys():
		flag = 0
		for q in qs:
			if not q in product_list[asin][0]:
				flag += 1
		if flag > len(qs)-expected: # eliminate if hits less than half
			continue
		else:
			f_score = 0
			s_score = 0
			t_score = len(query)/len(product_list[asin][0])
			search_criteria = token_clean(product_list[asin][-1])
			l = len(search_criteria)
			for q in qs:
				if q in search_criteria:
					f_score+=1 
			s_score = (f_score/l) *10
			f_score = f_score*10
			res.append({'asin':asin, 'score':s_score+f_score+t_score, 'title':product_list[asin][0]})
	sorted(res, key = lambda x: x['score'], reverse=True)
	if len(res) < topN:
		return res
	else:
		return res[0: topN]


if __name__ == "__main__":
    target_pkl = 'summarized_cate.pkl' # waiting for sum done.
    with open(target_pkl, 'rb') as f:
        asin_2_title_brand_categories = pickle.load(f) # {ID : (title, brand, categories)}, where "categories" is a list, others are strings.

    search('ipad', asin_2_title_brand_categories, 3)
