import re
from PIL import Image, ImageDraw, ImageFont
from collections import Counter

def statistics(product, a_term_list, a_cat_list, a_senti_list, r_term_list, r_cat_list, r_senti_list):

	a_term_dic={}
	a_term_pos_dic={}
	a_term_neg_dic={}
	r_term_dic={}
	r_term_pos_dic={}
	r_term_neg_dic={}

	a_cat={}
	r_cat={}

	a_pos_count=0
	a_neg_count=0

	r_pos_count=0
	r_neg_count=0

#---------------------------Amazon------------------------------------------
	for i,a_term in enumerate(a_term_list):
		a_term_dic[a_term] = a_term_dic.get(a_term, 0) + 1
		if(a_senti_list[i]==0):
			a_term_pos_dic[a_term] = a_term_pos_dic.get(a_term, 0) + 1
			a_pos_count+=1
			a_cat[a_cat_list[i]] = a_cat.get(a_cat_list[i], 0) + 1

		if(a_senti_list[i]==1):
			a_term_neg_dic[a_term] = a_term_neg_dic.get(a_term, 0) + 1
			a_neg_count+=1

	terms_A=""
	a_term_dic=sorted(a_term_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
	for d in a_term_dic[:3]:
		terms_A += str(d[0])+"; "

	terms_A_pos=""
	a_term_pos_dic=sorted(a_term_pos_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
	for d in a_term_pos_dic[:1]:
		terms_A_pos = str(d[0])

	terms_A_neg=""
	a_term_neg_dic=sorted(a_term_neg_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
	for d in a_term_neg_dic[:1]:
		terms_A_neg = str(d[0])

	Cat_A=""
	a_cat=sorted(a_cat.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
	for d in a_cat[:1]:
		Cat_A = str(d[0])

	Rate_A = 1.0 * a_pos_count / len(a_term_list)
	Rate_A = round(Rate_A, 2)
	Rate_A = str(Rate_A)
	Eff_A = 1.0 * (a_pos_count+a_neg_count) / len(a_term_list)


#---------------------------Reddit------------------------------------------
	for i,r_term in enumerate(r_term_list):
		r_term_dic[r_term] = r_term_dic.get(r_term, 0) + 1
		if(r_senti_list[i]==0):
			r_term_pos_dic[r_term] = r_term_pos_dic.get(r_term, 0) + 1
			r_pos_count+=1
			r_cat[r_cat_list[i]] = r_cat.get(r_cat_list[i], 0) + 1

		if(r_senti_list[i]==1):
			r_term_neg_dic[r_term] = r_term_neg_dic.get(r_term, 0) + 1
			r_neg_count+=1

	terms_R=""
	r_term_dic=sorted(r_term_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
	#print(r_term_dic)
	for d in r_term_dic[:3]:
		terms_R += str(d[0])+"; "

	terms_R_pos=""
	r_term_pos_dic=sorted(r_term_pos_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
	for d in r_term_pos_dic[:1]:
		terms_R_pos = str(d[0])

	terms_R_neg=""
	r_term_neg_dic=sorted(r_term_neg_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
	for d in r_term_neg_dic[:1]:
		terms_R_neg = str(d[0])

	Cat_R=""
	r_cat=sorted(r_cat.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
	for d in r_cat[:1]:
		Cat_R = str(d[0])

	Rate_R = 1.0 * r_pos_count / len(r_term_list)
	Rate_R = round(Rate_R, 2)
	Rate_R = str(Rate_R)
	Eff_R = 1.0 * (r_pos_count+r_neg_count) / len(r_term_list)

	if Eff_R > Eff_A:
		Effective_op = "Reddit"
	else:
		Effective_op = "Amazon"

	value_list = [terms_A, terms_R, terms_A_pos, terms_R_pos, \
				terms_A_neg, terms_R_neg, Cat_A, Cat_R, \
				Rate_A, Rate_R, Effective_op]

	collection_words = Counter(a_cat_list)
	most_concerned_asp1 = collection_words.most_common(1)[0][0]
	most_concerned_rate1 = '{:.2%}'.format(collection_words.most_common(1)[0][1] / sum(collection_words.values()))

	collection_words = Counter(r_cat_list)
	most_concerned_asp2 = collection_words.most_common(1)[0][0]
	most_concerned_rate2 = '{:.2%}'.format(collection_words.most_common(1)[0][1] / sum(collection_words.values()))

	a_cat_senti_dict = {}
	for i in range(len(a_cat_list)):
		if a_cat_list[i] not in a_cat_senti_dict.keys():
			a_cat_senti_dict[a_cat_list[i]] = 1 if a_senti_list[i]==0 else 0
		else:
			a_cat_senti_dict[a_cat_list[i]] += 1 if a_senti_list[i]==0 else 0
	a_cat_senti_dict = Counter(a_cat_senti_dict)
	most_good_asp1, most_bad_asp1 = a_cat_senti_dict.most_common()[0][0], a_cat_senti_dict.most_common()[-1][0]

	r_cat_senti_dict = {}
	for i in range(len(r_cat_list)):
		if r_cat_list[i] not in r_cat_senti_dict.keys():
			r_cat_senti_dict[r_cat_list[i]] = 1 if r_senti_list[i]==0 else 0
		else:
			r_cat_senti_dict[r_cat_list[i]] += 1 if r_senti_list[i]==0 else 0
	r_cat_senti_dict = Counter(r_cat_senti_dict)
	most_good_asp2, most_bad_asp2 = r_cat_senti_dict.most_common()[0][0], r_cat_senti_dict.most_common()[-1][0]

	agree_diff_dict = {}
	a_cat_sum, r_cat_sum = 0.0, 0.0
	for key in a_cat_senti_dict.keys():
		if key in r_cat_senti_dict.keys():
			a_cat_sum += a_cat_senti_dict[key]
			r_cat_sum += r_cat_senti_dict[key]
	for key in a_cat_senti_dict.keys():
		if key in r_cat_senti_dict.keys():
			agree_diff_dict[key] = abs(a_cat_senti_dict[key]/a_cat_sum - r_cat_senti_dict[key]/r_cat_sum)
	agree_diff_dict = Counter(agree_diff_dict)
	most_good_agree = agree_diff_dict.most_common()[-1][0]
	most_good_agree_rate1, most_good_agree_rate2 =  '{:.2%}'.format(a_cat_senti_dict[most_good_agree]/sum(a_cat_senti_dict.values())), '{:.2%}'.format(r_cat_senti_dict[most_good_agree]/sum(r_cat_senti_dict.values()))

	most_good_contro = agree_diff_dict.most_common()[0][0]
	most_good_contro_rate1, most_good_contro_rate2 =  '{:.2%}'.format(a_cat_senti_dict[most_good_contro]/sum(a_cat_senti_dict.values())), '{:.2%}'.format(r_cat_senti_dict[most_good_contro]/sum(r_cat_senti_dict.values()))

	eff_a, eff_r, eff_plat = '{:.2%}'.format(Eff_A), '{:.2%}'.format(Eff_R), Effective_op

	Rate_A, Rate_R = float(Rate_A), float(Rate_R)
	if Rate_A > Rate_R:
		platform1, platform2 = 'Amazon', 'Reddit'
		pos_rate1, pos_rate2 = '{:.2%}'.format(Rate_A), '{:.2%}'.format(Rate_R)
	else:
		platform1, platform2 = 'Reddit', 'Amazon'
		pos_rate1, pos_rate2 = '{:.2%}'.format(Rate_R), '{:.2%}'.format(Rate_A)


	template = '''
                                 The Analysis Report of [$product$] on Amazon and Reddit                                          
                                                                                             
----------------------------------------------------------------------------------------------------------------------------------
                                                                                             
Q: I wonder what aspect of this product is most concerned about on two platforms.   
                                                                                             
A: Consumers on the Amazon platform are most concerned about its [$most_concerned_asp1$]     
(account for [$most_concerned_rate1$]), and those from Reddit are more interested in its     
[$most_concerned_asp2$], with [$most_concerned_rate2$] opinion terms mentioned on it.    
                                                                                             
----------------------------------------------------------------------------------------------------------------------------------
                                                                                             
Q: So what aspects do people like / dislike most about this product on these platforms?     
                                                                                             
A: The finding is that Amazon customers prefer its [$most_good_asp1$] and are dissatisfied   
with its [$most_bad_asp1$], while Reddit users mostly praise its [$most_good_asp2$], and     
criticize its [$most_bad_asp2$].
                                                                                             
----------------------------------------------------------------------------------------------------------------------------------
                                                                                              
Q: What aspect of this product receives unanimous praise from two platforms? And what aspect 
is the most controversial one from these two?                                             
                                                                                              
A: The [$most_good_agree$] of this product is praised by both platforms, since the favorable 
rates from Amazon ([$most_good_agree_rate1$]) and Reddit ([$most_good_agree_rate2$]) show    
minimal differences comparing to other aspects. And its [$most_good_contro$] is the most     
controversial one, given the maximal gap from Amazon ([$most_good_contro_rate1$])            
to Reddit ([$most_good_contro_rate2$]).                                                     
                                                                                             
----------------------------------------------------------------------------------------------------------------------------------
                                                                                              
Q: Which platform to choose if I need more effective (non-neutral) opinions?                
                                                                                                                                                                                          
A: The percentage of non-neutral sentiment terms from Amazon is [$eff_a$] and that from      
Reddit is [$eff_r$], thus we suggest you to search from [$eff_plat$] to save time.         
                                                                                             
----------------------------------------------------------------------------------------------------------------------------------
                                                                                             
Q: I want to know the potential defects of this product, which platform should I choose to   
obtain more valuable information?                                                           
                                                                                             
A: According to our analysis, customers from [$platform1$] give a higher overall praise rate 
([$pos_rate1$]) comparing to that from [$platform2$] ([$pos_rate2$]), we therefore recommend 
you to go to [$platform2$] for more information if you require a more complete understanding 
of its hidden shortcomings.
'''

	detect_vars = re.findall(r'\$(.*?)\$', template)
	for var in detect_vars:
		try:
			template = template.replace('$'+var+'$', eval(var))
		except:
			continue

	d_font = ImageFont.truetype('C:/Windows/Fonts/timesbd.ttf', 16)
	image = Image.new("L", (650, 16*55), "white")
	draw_table = ImageDraw.Draw(im=image)
	draw_table.text(xy=(0, 0), text=template, fill='#000000', font= d_font, spacing=4)

	image.save('../app/static/images/'+product+'_platform_comparison.jpg') 
	# image.save('_platform_comparison.jpg') 

# ----------------------------------------Test----------------------------------------
# product = 'ipad' 
# a_term_list = ['ipad', 'tablet', 'ipad', 'tablet', 'tablet', 'kindle', 'ipad', 'tablet', 'ipad', 'thumbs', 'gift', 'enjoyed', 'ipad', 'mini', 'packaged', 'pleased', 'ipad', 'arrived', 'apple', 'reliable', 'ipad', 'scratches', 'perfect', 'ipad', 'gps', 'excellent', 'quality', 'china', 'pleased', 'gift', 'scratchs', 'new', 'excellent', 'worked', 'product', 'ipad', 'downloads', 'projected', 'new', 'ipad', 'grandson', 'mini', 'heard', 'cable', 'missing', 'charge', 'battery', 'great', 'described', 'just', 'ipod', 'small', 'good', 'ipad', 'apple', 'ok', 'storage', 'space', 'read', 'clear', 'gift', 'wife', 'does', 'special', 'tool', 'recommend', 'fantastic', 'received', 'nice', 'ipad', 'refurbished', 'pad', 'mini', 'apple', 'fix', 'refund', 'died', 'arrived', 'year', 'phantom', 'dji', 'price', 'new', 'horizontal', 'position', 'year', 'old', 'pad', 'complaints', 'gift', 'pleased', 'international', 'use'] 
# a_cat_list = ['system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'screen', 'system', 'system', 'system', 'system', 'quality', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'power', 'power', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'power', 'power', 'look', 'quality', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'power', 'system', 'system', 'system', 'system', 'quality', 'system', 'screen', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system']
# a_senti_list = [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2] 
# r_term_list = ['wallpapers', 'paperlike', 'ipad', 'os', 'macos', 'ipados', 'ipad', 'protectors', 'ipad', 'student', 'wallpapers', 'resolution', 'wallpapers', 'macos', 'ipad', 'macos', 'ipad', 'touchscreen', 'ipad', 'wifi', 'ipad', 'protectors', 'ipad', 'protectors', 'ipad', 'protectors', 'ipad', 'ios', 'ipad', 'kindle', 'ipad', 'protectors', 'ipad', 'protectors', 'ipad', 'protector', 'scratches', 'protectors', 'ipad', 'protector', 'ipad', 'protector', 'icons', 'icon', 'screenprotector', 'icons', 'icons', 'icon', 'ipad', 'protectors', 'ipads', 'apple'] 
# r_cat_list = ['system', 'system', 'system', 'system', 'Invalid', 'Invalid', 'system', 'system', 'system', 'system', 'system', 'quality', 'system', 'Invalid', 'system', 'Invalid', 'system', 'screen', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'screen', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system', 'system']
# r_senti_list = [0, 1, 2, 2, 2, 0, 2, 0, 2, 0, 0, 1, 0, 2, 2, 2, 2, 0, 2, 2, 2, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 2, 2, 0, 2, 0, 2, 2]
# statistics(product, a_term_list, a_cat_list, a_senti_list, r_term_list, r_cat_list, r_senti_list)