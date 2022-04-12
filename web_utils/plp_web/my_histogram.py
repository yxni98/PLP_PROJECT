import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
 
plt.rcParams['font.sans-serif'] = ['SimHei']

def draw_histogram(positive, neutral, negative, labels, product, platform):
	x = np.arange(len(labels))  # the label locations
	width = 0.3  # the width of the bars
	 
	fig, ax = plt.subplots()
	rects1 = ax.bar(x - 0.3, positive, width, label='positive')
	rects2 = ax.bar(x , neutral, width, label='neutral')
	rects3 = ax.bar(x + 0.3, negative, width, label='negative')
	 
	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Percentage')
	ax.set_title('Sentiment Aggregation By Category')
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	ax.legend()
	 
	 
	def autolabel(rects):
	    """Attach a text label above each bar in *rects*, displaying its height."""
	    for rect in rects:
	        height = rect.get_height()
	        ax.annotate('{}'.format(height),
	                    xy=(rect.get_x() + rect.get_width() / 3, height),
	                    xytext=(0, 3),  # 3 points vertical offset
	                    textcoords="offset points",
	                    ha='center', va='bottom')
	 
	 
	autolabel(rects1)
	autolabel(rects2)
	autolabel(rects3)
	 
	fig.tight_layout()
	 
	plt.savefig('../app/static/images/'+product+'_'+platform+'_histogram.jpg')