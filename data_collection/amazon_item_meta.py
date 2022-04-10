# Using meta_Cell_Phones_and_Accessories.json and meta_Electronics.json from http://deepyeti.ucsd.edu/jianmo/amazon/categoryFiles as baseline
import nltk,json,pickle,random
from nltk.tokenize import word_tokenize

nltk.download('punkt')
def token_clean(title):
	tokens= word_tokenize(title)
	res = []
	for t in tokens:
		
		if len(t) ==1: # remove single symbol/char
			continue
		tar = t.lower().replace('-','')
		if not tar in res and not tar=='amp' and not tar =='sww' and not tar=='swi': # remove 'amp', 'sww', 'swi' 3 unknown error chars 
			res.append(tar)
	return res


def json_convert():
	target_cp_meta = 'meta_Cell_Phones_and_Accessories.json'
	target_ele_meta = 'meta_Electronics.json'

	cate_ng_word = ['cases', 'protector', 'cable']
	# manually pick out words not connecting to electronic device in electronic.json.
    	 
	asin_2_title_brand_categories = {}
	asin_list = []
	duplications = []
	for line in open(target_ele_meta, 'r', encoding = 'utf-8'):
		data_dict = json.loads(line)
		categories = data_dict['category']

		keep = True

		for c in categories:
			for ng in cate_ng_word:
				if ng in c.lower():
					keep = False
		if not keep:
			continue	
		asin = data_dict['asin']
		title = ' '.join(token_clean(data_dict['title']))
		brand = data_dict['brand']
		
		
		asin_2_title_brand_categories[asin] = (title, brand, categories)
		asin_list.append(asin)

	print("*************** Electronic Meta Done, collected items:" + str(len(asin_list)) )
	for line in open(target_cp_meta, 'r', encoding = 'utf-8'):
		data_dict = json.loads(line)
		categories = data_dict['category']

		if not 'Cell Phones' in categories:
			continue	
		asin = data_dict['asin']
		title = ' '.join(token_clean(data_dict['title']))
		brand = data_dict['brand']
		
		asin_2_title_brand_categories[asin] = (title, brand, categories)
		if asin in asin_list:
			duplications.append(asin)
			# duplication means electronic.json and cell phone.json have items with the same asin for unknown reasons.
			continue
		asin_list.append(asin)

	print("*************** Cell Phone Meta Done, collected items:" + str(len(asin_list)) )
	with open('amazon_process_cate.pkl', 'wb') as f:
		pickle.dump(asin_2_title_brand_categories, f, pickle.HIGHEST_PROTOCOL)

    # Saved pkl will be used for training.

training_targets = {
	'apple':[{'key_word':'iphone','cate':'Cell Phones'}, {'key_word':'ipad','cate':'Tablets'},{'key_word':'macbook','cate':'Laptops'},{'key_word':'apple watch','cate':'Smartwatches'}],
	'samsung':[{'key_word':'galaxy note','cate':'Cell Phones'},{'key_word':'galaxy tab','cate':'Tablets'}],
	'huawei':[{'key_word':'huawei mate', 'cate':'Cell Phones'}, {'key_word':'huawei honor', 'cate':'Cell Phones'}],
	'microsoft':[{'key_word':'microsoft surface','cate':'Tablets'}],
	'sony':[{'key_word':'xperia', 'cate':'Cell Phones'}],
	'others':[{'key_word':'smart watch','cate':'Smartwatches'}, {'key_word':'digital camera','cate':'Digital Cameras'}]
}
# Training_targets is a dict manually created listing down the mostly requently searched electronic items.

def get_training_pairs(): # generate training data for summarization.
	target_pkl = 'amazon_process_cate.pkl'
	with open(target_pkl, 'rb') as f:
		asin_2_title_brand_categories = pickle.load(f) # {ID : (title, brand, categories)}, where "categories" is a list, others are strings.

	train_num = 150

	datasets = []
	for brand in training_targets:
		datasets.extend(training_targets[brand])

	training_items = []
	unique_asin = []

	for pair in datasets:
		target_count = 0
		against_count = 0
		key_word = pair['key_word']
		print("current cate: ", pair)
		for asin in asin_2_title_brand_categories.keys():
			title_brand_categories = asin_2_title_brand_categories[asin]
			title = title_brand_categories[0]
			if not asin in unique_asin:				
				if key_word in title.lower():
					if pair['cate'] in title_brand_categories[2]:
						if target_count < train_num:
							# find out the precise cate:
							if title_brand_categories[2][-1].lower() in title_brand_categories[2][-2].lower():
								cate = title_brand_categories[2][-1].lower()
							elif title_brand_categories[2][-2].lower() in title_brand_categories[2][-1].lower():
								cate = title_brand_categories[2][-2].lower()
							else:
								if len(title_brand_categories[2][-1].lower())>len(title_brand_categories[2][-2].lower()):
									cate = title_brand_categories[2][-2].lower()
								else:
									cate = title_brand_categories[2][-1].lower()
							
							t = title + ' '+cate
							if not title_brand_categories[1] in title.lower():
								t = title_brand_categories[1] + ' ' + t
							training_items.append({'id':asin,'document':" ".join(token_clean(t)),'summary':key_word})
							target_count+=1
							unique_asin.append(asin)
					else:
						if against_count <train_num:
							if title_brand_categories[2][-1].lower() in title_brand_categories[2][-2].lower():
									cate = title_brand_categories[2][-1].lower()
							elif title_brand_categories[2][-2].lower() in title_brand_categories[2][-1].lower():
								cate = title_brand_categories[2][-2].lower()
							else:
								if len(title_brand_categories[2][-1].lower())>len(title_brand_categories[2][-2].lower()):
									cate = title_brand_categories[2][-2].lower()
								else:
									cate = title_brand_categories[2][-1].lower()
							t = title + ' '+cate
							if not title_brand_categories[1] in title.lower():
								t = title_brand_categories[1] + ' ' + t
							training_items.append({'id':asin,'document':" ".join(token_clean(t)),'summary':key_word + ' ' +  cate})
							against_count+=1
							unique_asin.append(asin)
		print('target_count: '+str(target_count), 'against_count: '+str(against_count))
	random.shuffle(training_items)
	l = len(training_items)
	print('total nums here ************************************************************')
	print(l)
	vali_items =training_items[0:int(l/4)]	
	test_items = training_items[int(l/4):int(l/2)]
	training_items = training_items[int(l/2):l-1]


	with open('devices_train.json', 'w') as file_obj:
		json.dump({'data':training_items}, file_obj)

	with open('devices_vali.json', 'w') as file_obj:
		json.dump({'data':vali_items}, file_obj)

	with open('devices_test.json', 'w') as file_obj:
		json.dump({'data':test_items}, file_obj)

	# json saved to suit the huggingface datasets format.

    # training will be done in a notebook and running on Google Colab, see: ./summarization/Summarization_FineTuning.ipynb

