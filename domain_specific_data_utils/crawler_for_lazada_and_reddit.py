import requests, re, json, random
import xlwt
from bs4 import BeautifulSoup

user_agent_list = ['Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
                   'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
                   'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR '
                   '3.5.30729)',
                   'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                   'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)',
                   'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
                   "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                   "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
                   "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
                   "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
                   "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
                   "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
                   "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
                   "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
                   "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
                   "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
                   "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
                   "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
                   "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
                   "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
                   "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
                   "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
                   "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
                   "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
                   "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
                   "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                   "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
                   "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
                   ]

# # ************* SETTINGS CONFIGURATION *************
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# No_Image_loading = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", No_Image_loading)
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# proxies_list = []

# # ************* IP COLLECTION AND PROXIES CONFIGURATION *************
# ip_url = "https://www.proxydocker.com/zh/proxylist/country/Hong%20Kong"
# browser = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
# browser.get(ip_url)
# ip_content = browser.page_source
# browser.quit()
# soup = BeautifulSoup(ip_content, "html.parser")
# ip_table = soup.findAll("tbody", id = "proxylist_table")[0]
# for tr in ip_table.findAll("tr"):
# 	detail_list = [td.get_text() for td in tr.findAll("td")] # e.g., ['223.255.133.34:8080', 'CON25', 'Lvl3', '', ' Hong Kong', 'Central', '', '44m']
# 	if detail_list[1] == 'HTTP':
# 		proxies = {"http" : detail_list[0]} # e.g., proxies = {"http" : "103.97.201.119:80"}
# 		proxies_list.append(proxies)
# 	elif detail_list[1] == 'HTTPS':
# 		proxies = {"https" : detail_list[0]}
# 		proxies_list.append(proxies)
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
url = 'https://www.kuaidaili.com/free/inha/'
r = requests.get(url, headers = headers)
data = r.text
proxies_list = []
soup =  BeautifulSoup(data, "html.parser")
tbody = soup.findAll('tbody')[0]
for tr in tbody.findAll('tr'):
	ip_info = tr.findAll('td')
	ip = ip_info[0].get_text()
	port = ip_info[1].get_text()
	http_way = ip_info[3].get_text()
	proxies_list.append({http_way : ip+':'+port})

def scrape_lazada(product, item_id):
	headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "x-requested-with": "XMLHttpRequest",
    }
	cookies = {
    	"user": "en"
    }
	for proxies in proxies_list:
		try:
			# ************* LAZADA COMMENTS COLLECTION *************
			host = "lazada.sg"
			page_records = "500" # how many reviews we retrieve for each page
			page_no = "1" # default setting, page 1 will return [page_records] reviews
			product_url = "https://my.{}/pdp/review/getReviewList?itemId={}&pageSize={}&filter=0&sort=1&pageNo={}".format(host, item_id, page_records, page_no)
			r = requests.get(product_url, headers=headers, cookies=cookies, proxies=proxies, verify=False)
			respone = json.loads(r.text)
			js = json.dumps(respone["model"]["items"])
			file = open("full reviews for "+product+".txt", "w+")
			file.write(js)
			file.close()

			print("success")
			break
		except Exception as e:
			continue

	workbook = xlwt.Workbook(encoding = 'utf-8')

	file = open("full reviews for "+product+".txt", "r") 
	js = file.read()
	dic = json.loads(js)
	file.close()

	row = 0
	worksheet = workbook.add_sheet("sheet1")
	for pair in dic:
		if pair["reviewContent"] == None:
			continue
		if pair["rating"] == None:
			pair["rating"] = " "
		worksheet.write(row, 0, label = str(pair["rating"]))
		worksheet.write(row, 1, label = str(pair["reviewContent"]))
		row += 1

	workbook.save("reviews for "+product+" from lazada.xls")

# product = "logitech wireless mouse" # search keyword
# item_id = "795246748"
# scrape_lazada(product, item_id)


def scrape_reddit(product, page_count):
	headers = {
		'authority': 'www.reddit.com',
		'method': 'GET',
		'path': '/r/'+product+'/comments/',
		'scheme': 'https',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9',
		'cookie': 'loid=0000000000jtbzvqtq.2.1645161017338.Z0FBQUFBQmlEeW81T3dtemRXRVhIOVpkYVRURlNXcHNaVUREaVhMZFJaNUMxOU9IVG9rRkszSFg3c3BsZXYtMVZnNXVjZmRnWkU4OXdzcWZtWXVyRngtSDFmNE1wRHBuU0xaZXJmandSTjc5d2trOGNWYWdkX3NYUkxlUnk3WUs2b3JPckU3VVVDOWQ; csv=2; edgebucket=uYzC7uYrwsGOEYsD6T; pc=dj; g_state={"i_l":0}; reddit_session=1552771201166%2C2022-02-18T05%3A16%3A51%2C6178d678352486bde87f25e39b5d73e13446bd45; session=047c55ed29fdb06b6f95f2faf6b869a97a970b63gASVSQAAAAAAAABKwSsPYkdB2IPKnTi5L32UjAdfY3NyZnRflIwoMWVhMTlkNzc4ZDllNjVkNTUzNTVmOGJmNTdiNWVmM2M4NmM4OGUwMZRzh5Qu; token_v2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDUxNjQ4OTMsInN1YiI6IjE1NTI3NzEyMDExNjYtMWs3UFdvMHFQLWFtRk5ETHlIYXlxS2V4V0hTUWZ3IiwibG9nZ2VkSW4iOnRydWUsInNjb3BlcyI6WyIqIiwiZW1haWwiLCJwaWkiXX0.qAPIAsPS8i59xq9fQkSv4t7e5ax0mKjDpKilHPia83c; recent_srs=t5_2qizd%2Ct5_3k8y7%2Ct5_2eodkd%2Ct5_2qh2b%2Ct5_36wgwm%2C; datadome=2NX4keXCuB0Tco2f0YtkpLFFAUnJYJRMm_h.cEKT238Ad4yEH9GUaMk.4yXES1zYvm-Bt335z.rxU2xSkRptzVQBz5pSJhodrD90WMzH2y~hg2f92KCJvwYq68~3ebg; session_tracker=rmikhjnqkjrmaalrgj.0.1645162898530.Z0FBQUFBQmlEekdTVlc1ODhvUVJuSGp4X2p3ZHhtS0JvTDgyR0taMlZLMFlleWxESzFISEdoQlZxNGdOcUpoc1hMZ1RDSGJnYWRnaGNURkQ2Z2VHWnNjU2dFNVhHUU5LdnBaTk9qUmc4WWNERmd3U1MwelZYb044dmVLbklRVmJITXB1T0ltWUFmT1I',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': 'Windows',
		'sec-fetch-dest': 'document',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'none',
		'sec-fetch-user': '?1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
	}
	for proxies in proxies_list:
		try:
			headers = {'user-agent': random.choice(user_agent_list)}
			product_url = 'https://www.reddit.com/r/'+product+'/comments/'
			r = requests.get(product_url, headers=headers,  proxies=proxies, verify=False)
			data = r.text
			break
		except Exception as e:
			continue
	soup =  BeautifulSoup(data, "html.parser")
	post_titles = [post.get_text() for post in soup.findAll("a", class_ = "title")]
	post_comment = [post.get_text() for post in soup.findAll("div", class_ = "md")][-len(post_titles):]

	current_count = 1
	while current_count < page_count:
		for proxies in proxies_list:
			try:
				headers = {'user-agent': random.choice(user_agent_list)}
				next_link = soup.findAll("span", class_ = "next-button")[-1].find('a').attrs['href']
				print(str(next_link))
				r = requests.get(str(next_link), headers=headers,  proxies=proxies, verify=False)
				soup =  BeautifulSoup(data, "html.parser")
				post_titles += [post.get_text() for post in soup.findAll("a", class_ = "title")]
				post_comment += [post.get_text() for post in soup.findAll("div", class_ = "md")][-len(post_titles):]
				print('next page!')
				break
			except Exception as e:
				continue
		current_count += 1

	workbook = xlwt.Workbook(encoding = 'utf-8')

	worksheet = workbook.add_sheet("sheet1")
	worksheet.write(0, 0, label = "post_title")
	worksheet.write(0, 1, label = "comment_under_this_post")

	row = 1
	for i in range(len(post_titles)):
		worksheet.write(row, 0, label = post_titles[i])
		worksheet.write(row, 1, label = post_comment[i])
		row += 1

	workbook.save("reviews for "+product+" from reddit.xls")

product = 'iphone13pro'
page_count = 20
scrape_reddit(product, page_count)

# product = 'ipadpro'
# scrape_reddit(product)

# product = 'airpodspro'
# scrape_reddit(product)

# product = 'huawei'
# scrape_reddit(product)