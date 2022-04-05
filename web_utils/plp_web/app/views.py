from django.shortcuts import render
from django.utils.html import escape
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def analyse_result(request):
	product = escape(request.GET["product"])
	platform = escape(request.GET["platform"])
	match_product_name = 'ipad pro mini'
	# python manage.py migrate
	request.session["match_product_name2"] = match_product_name
	request.session["match_product_name3"] = match_product_name
	if platform.lower() == 'amazon':
		return render(request, 'amazon_result1.html', {'product_name':match_product_name})
	else:
		return render(request, 'reddit_result.html', {'product_name':match_product_name})

def result_jump2(request):
	match_product_name2 = request.session.get("match_product_name2", default="null")
	return render(request, 'amazon_result2.html', {'product_name':match_product_name2})

def result_jump3(request):
	match_product_name3 = request.session.get("match_product_name3", default="null")
	return render(request, 'amazon_result3.html', {'product_name':match_product_name3})
