import requests, re, json, random, time, os
from bs4 import BeautifulSoup
from selenium import webdriver
browser = webdriver.Firefox()

def delete_emoji(text):
	emoji_pattern = re.compile("["
		u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U00010000-\U0010ffff"
	                           "]+", flags=re.UNICODE)
	return(emoji_pattern.sub(r'', text))

def match_reviews_from_reddit(product, page_count):
	

	product_url = 'https://www.reddit.com/r/'+product+'/comments/'
	browser.get(product_url)
	data = browser.page_source
	soup =  BeautifulSoup(data, "html.parser")
	post_titles = [post.get_text() for post in soup.findAll("a", class_ = "title")]
	post_comment = [post.get_text() for post in soup.findAll("div", class_ = "md")][-len(post_titles):]

	current_count = 1
	while current_count < page_count:
		next_link = soup.findAll("span", class_ = "next-button")[-1].find('a').attrs['href']
		print(str(next_link))
		browser.get(str(next_link))
		soup =  BeautifulSoup(data, "html.parser")
		post_titles += [post.get_text() for post in soup.findAll("a", class_ = "title")]
		post_comment += [post.get_text() for post in soup.findAll("div", class_ = "md")][-len(post_titles):]
		print('next page!')
		current_count += 1
		
	

	reviews = []
	for i in range(len(post_titles)):
		reviews.append((delete_emoji(post_titles[i]), delete_emoji(post_comment[i])))

	return reviews

def return_review_from_reddit(product):
	all_reviews = []
	page_count = 5
	reviews = match_reviews_from_reddit(product, page_count)
	all_reviews += reviews

	comment_title_dict = {}
	for review in all_reviews:
		if 'I am a bot' not in review[0] and 'I am a bot' not in review[1]:
			comment_title_dict[review[1]] = review[0]

	return_reviews = []
	for key in comment_title_dict.keys():
		return_reviews.append(comment_title_dict[key]+' '+key)

	return return_reviews

