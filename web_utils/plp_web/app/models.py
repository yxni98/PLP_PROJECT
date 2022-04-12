from django.db import models

# Create your models here.
class Product(models.Model):
	_name = models.CharField(max_length=30)
	_time = models.IntegerField()
	_amazon_term_list_1D = models.TextField(blank=True)
	_amazon_category_list_1D = models.TextField(blank=True)
	_amazon_sentiment_list_1D = models.TextField(blank=True)
	_reddit_term_list_1D = models.TextField(blank=True)
	_reddit_category_list_1D = models.TextField(blank=True)
	_reddit_sentiment_list_1D = models.TextField(blank=True)

	def get_attributes(self):
		return (self._name, self._time, self._amazon_term_list_1D, self._amazon_category_list_1D, self._amazon_sentiment_list_1D, self.\
			_reddit_term_list_1D, self._reddit_category_list_1D, self._reddit_sentiment_list_1D)